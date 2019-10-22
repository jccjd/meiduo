import json
from _decimal import Decimal
from venv import logger

from django import http
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
# Create your views here.
from django.utils import timezone
from django.views import View
from django_redis import get_redis_connection

from goods.models import SKU
from orders.models import OrderInfo, OrderGoods
from users.models import Address
from users.views import LoginRequiredMixin
from meiduo.utils.response_code import RETCODE
from django.db import transaction

from verifications import constants


class OrderSettlementView(LoginRequiredMixin, View):
    """结算订单"""

    def get(self, request):
        """提供订单结算页面"""
        user = request.user
        try:
            addresses = Address.objects.filter(user=request.user, is_deleted=False)
        except Address.DoesNotExist:
            addresses = None

        redis_conn = get_redis_connection('carts')
        redis_cart = redis_conn.hgetall('carts_%s' % user.id)
        cart_selected = redis_conn.smembers('selected_%s' % user.id)

        cart = {}
        for sku_id in cart_selected:
            cart[int(sku_id)] = int(redis_cart[sku_id])

        total_count = 0
        total_amount = Decimal(0.00)
        skus = SKU.objects.filter(id__in=cart.keys())
        for sku in skus:
            sku.count = cart[sku.id]
            sku.amount = sku.count * sku.price
            total_count += sku.count
            total_amount += sku.count * sku.price
        freight = Decimal('10.00')

        context = {

            'addresses': addresses,
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'freight': freight,
            'payment_amount': total_amount + freight

        }

        return render(request, 'place_order.html', context)


class OrderCommitView(LoginRequiredMixin, View):
    """docstring for OrderCommitView."""

    def post(self, request):

        json_dict = json.loads(request.body.decode())
        address_id = json_dict.get('address_id')
        pay_method = json_dict.get('pay_method')

        if not all([address_id, pay_method]):
            return http.HttpResponseForbidden('缺少必要参数')

        try:
            address = Address.objects.get(id=address_id)
        except Exception:
            return http.HttpResponseForbidden('参数id错误')

        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'], OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return http.HttpResponseForbidden('参数pay_method错误')
        user = request.user
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)

        with transaction.atomic():
            save_id = transaction.savepoint()

            try:
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_amount=Decimal('0'),
                    freight=Decimal('10.00'),
                    pay_method=pay_method,
                    status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if pay_method == OrderInfo.PAY_METHODS_ENUM[
                        'ALIPAY'] else
                    OrderInfo.PAY_METHODS_ENUM['']
                )

                redis_conn = get_redis_connection('carts')
                redis_cart = redis_conn.hgetall('carts_%s' % user.id)
                selected = redis_conn.smembers('selected_%s' % user.id)
                carts = {}
                for sku_id in selected:
                    carts[int(sku_id)] = int(redis_cart[sku_id])
                sku_ids = carts.keys()

                for sku_id in sku_ids:
                    while True:
                        sku = SKU.objects.get(id=sku_id)
                        origin_stock = sku.stock
                        origin_sales = sku.sales

                        sku_count = carts[sku_id]
                        if sku_count > sku.stock:
                            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '库存不足'})

                        new_stock = origin_stock - sku_count
                        new_sales = origin_sales + sku_count
                        result = SKU.objects.filter(id=sku_id, stock=origin_stock).update(stock=new_stock,
                                                                                          sales=new_sales)

                        if result == 0:
                            continue

                        sku.spu.sales += sku_count
                        sku.spu.save()

                        OrderGoods.objects.create(

                            order=order,
                            sku=sku,
                            count=sku_count,
                            price=sku.price,
                        )
                        order.total_count += sku_count
                        order.total_amount += (sku_count * sku.price)
                        break

                order.total_amount += order.freight
                order.save()
            except Exception as e:
                logger.error(e)
                transaction.savepoint_rollback(save_id)
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '下单失败'})

        transaction.savepoint_commit(save_id)

        p1 = redis_conn.pipeline()
        p1.hdel('carts_%s' % user.id, *selected)
        p1.srem('selected_%s' % user.id, *selected)
        p1.execute()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '下单成功', 'order_id': order.order_id})


class OrdersSuccessView(LoginRequiredMixin, View):

    def get(self, request):
        order_id = request.GET.get('order_id')
        payment_amount = request.GET.get('payment_amount')
        pay_method = request.GET.get('pay_method')
        context = {
            'order_id': order_id,
            'payment_amount': payment_amount,
            'pay_method': pay_method,

        }

        return render(request, 'order_success.html', context)


class UserOrderInfoView(LoginRequiredMixin, View):
    def get(self, request, page_num):
        """提供我的订单页面"""
        user = request.user
        # 查询订单
        orders = user.orderinfo_set.all().order_by("-create_time")
        # 遍历所有订单
        for order in orders:
            # 绑定订单状态
            order.status_name = OrderInfo.ORDER_STATUS_CHOICES[order.status-1][1]
            # 绑定支付方式
            order.pay_method_name = OrderInfo.PAY_METHOD_CHOICES[order.pay_method-1][1]
            order.sku_list = []
            # 查询订单商品
            order_goods = order.skus.all()
            # 遍历订单商品
            for order_good in order_goods:
                sku = order_good.sku
                sku.count = order_good.count
                sku.amount = sku.price * sku.count
                order.sku_list.append(sku)

        # 分页
        page_num = int(page_num)
        try:
            paginator = Paginator(orders, constants.ORDERS_LIST_LIMIT)
            page_orders = paginator.page(page_num)
            total_page = paginator.num_pages
        except EmptyPage:
            return http.HttpResponseNotFound('订单不存在')

        context = {
            "page_orders": page_orders,
            'total_page': total_page,
            'page_num': page_num,
        }
        return render(request, "user_center_order.html", context)


class OrderCommentView(LoginRequiredMixin, View):

    def get(self, request):

        order_id = request.GET.get('order_id')

        try:
            OrderInfo.objects.get(order_id=order_id, user=request.user)
        except OrderInfo.DoesNotExist:
            return http.HttpResponseForbidden('订单不存在')

        try:
            uncomment_goods = OrderGoods.objects.filter(order_id=order_id, is_commented=False)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('订单商品出错')

        uncomment_goods_list = []
        for goods in uncomment_goods:
            uncomment_goods_list.append({
                'order_id': goods.order.order_id,
                'sku_id': goods.sku.id,
                'name': goods.sku.name,
                'price': str(goods.price),
                'default_image_url': goods.sku.default_image.url,
                'comment': goods.comment,
                'score': goods.score,
                'is_anonymous': str(goods.is_anonymous),
            })

        context = {
            'uncomment_goods_list': uncomment_goods_list
        }

        return render(request, 'goods_judge.html', context)




