import datetime
from venv import logger

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django import http
import re, json, logging
from django.db import DatabaseError
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django_redis import get_redis_connection

from carts.utils import merge_cart_cookie_to_redis
from contents.utils import get_categories
from goods import models
from goods.utils import get_breadcrumb
from meiduo.utils.response_code import RETCODE
from users.models import User, Address
from users.utils import login_required_json, generate_verify_email_url, chick_verify_email_token
from meiduo.celery_tasks.emails.tasks import send_verify_email
from verifications import constants


class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """提供用户注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """实现用户注册业务逻辑"""
        # 接收参数：表单参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        sms_code_client = request.POST.get('sms_code')
        allow = request.POST.get('allow')

        # 校验参数：前后端的校验需要分开，避免恶意用户越过前端逻辑发请求，要保证后端的安全，前后端的校验逻辑相同
        # 判断参数是否齐全:all([列表])：会去校验列表中的元素是否为空，只要有一个为空，返回false
        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 判断短信验证码是否输入正确
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)

        if sms_code_server is None:
            return render(request, 'register.html', {'sms_code_errmsg': '短信验证码已失效'})
        if sms_code_client != sms_code_server.decode():
            return render(request, 'register.html', {'sms_code_errmsg': '输入短信验证码有误'})
        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')

        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError as e:
            print(e)
            return render(request, 'register.html', {'register_errmsg': '注册失败'})

        # 实现状态保持
        login(request, user)

        # 响应结果:重定向到首页
        response = redirect(reverse('contents:index'))
        # return http.HttpResponse('注册成功，重定向到首页')
        # 为了实现在首页的右上角展示用户名信息，我们需要将用户名缓存到cookie中
        # response.set_cookie('key', 'val', 'expires')
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        # 响应结果:重定向到首页
        return response


# class

class UsernameCountView(View):
    def get(self, request, username):
        """

        :param request:
        :param username:
        :return: JSON
        """
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class MobileCountView(View):

    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class LoginView(View):
    """用户名登录"""

    def get(self, request):
        """
        提供登录界面
        :param request: 请求对象
        :return: 登录界面
        """

        return render(request, 'login.html')

    def post(self, request):
        """
        实现登录逻辑
        :param request: 请求对象
        :return: 登录结果
        """
        # 接受参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')

        # 校验参数
        # 判断参数是否齐全
        if not all([username, password]):
            return http.HttpResponseForbidden('缺少必传参数')

        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入正确的用户名或手机号')

        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('密码最少8位，最长20位')

        # 认证登录用户
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误'})

        # 实现状态保持
        login(request, user)
        # 设置状态保持的周期
        if remembered != 'on':
            # 没有记住用户：浏览器会话结束就过期
            request.session.set_expiry(0)
        else:
            # 记住用户：None表示两周后过期
            request.session.set_expiry(None)

        # 响应登录结果
        next = request.GET.get('next')
        if next:
            response = redirect(next)
        else:

            response = redirect(reverse('contents:index'))

        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        # when user login add  merge carts to the carts
        response = merge_cart_cookie_to_redis(request=request, user=user, response=response)
        return response


class LogoutView(View):

    def get(self, request):
        logout(request)
        response = redirect(reverse('contents:index'))
        response.delete_cookie('username')

        return response


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view()
        return login_required(view)


class UserInfoView(LoginRequiredMixin, View):

    def get(self, request):
        content = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,
        }

        return render(request, 'user_center_info.html', context=content)


class LoginRequired(View):

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequired, cls).as_view()
        return login_required(view)


class EmailView(View):
    def put(self, request):

        if not request.user.is_authenticated:
            return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})

        json_dict = json.loads(request.body.decode())
        email = json_dict.get('email')

        if not email:
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('参数email有误')

        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logging.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '添加邮箱失败'})

        return http.JsonResponse({'code': RETCODE.OK, 'errmg': '添加邮箱成功'})


class LoginRequiredJSONMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required_json(view)


class EmailView(LoginRequiredJSONMixin, View):
    """添加邮箱"""

    def put(self, request):
        """实现添加邮箱逻辑"""
        # 判断用户是否登录并返回JSON

        json_dict = json.loads(request.body.decode())
        email = json_dict.get('email')

        if not email:
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('参数email有误')

        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logging.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '添加邮箱失败'})
        verify_url = generate_verify_email_url(request.user)
        # send_verify_email.delay(email, verify_url)
        send_verify_email(email, verify_url)
        return http.JsonResponse({'code': RETCODE.OK, 'errmg': '添加邮箱成功'})


class VerifyEmailView(View):

    def get(self, request):
        token = request.GET.get('token')
        if not token:
            return http.HttpResponseBadRequest('缺少token')
        user = chick_verify_email_token(token)
        if not user:
            return http.HttpResponseForbidden('无效的token')
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('激活邮箱失败')

        return redirect(reverse('users:info'))


class AddressView(LoginRequiredMixin, View):

    def get(self, request):
        """查询并展示用户地址信息"""

        # 获取当前登录用户对象
        login_user = request.user
        # 使用当前登录用户和is_deleted=False作为条件查询地址数据
        addresses = Address.objects.filter(user=login_user, is_deleted=False)

        # 将用户地址模型列表转字典列表:因为JsonResponse和Vue.js不认识模型类型，只有Django和Jinja2模板引擎认识
        address_list = []
        for address in addresses:
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }
            address_list.append(address_dict)

        # 构造上下文
        context = {
            # 'default_address_id': login_user.default_address_id or '0',
            'default_address_id': login_user.default_address_id or '0',  # 没有默认地址 None
            'addresses': address_list
        }

        return render(request, 'user_center_site.html', context)


class AddressCreateView(LoginRequiredJSONMixin, View):
    """新增地址"""

    def post(self, reqeust):
        """实现新增地址逻辑"""

        # 判断用户地址数量是否超过上限：查询当前登录用户的地址数量
        # count = Address.objects.filter(user=reqeust.user).count()
        count = reqeust.user.addresses.count()  # 一查多，使用related_name查询
        if count > constants.USER_ADDRESS_COUNTS_LIMIT:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '超出用户地址上限'})

        # 接收参数
        json_str = reqeust.body.decode()
        json_dict = json.loads(json_str)
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('参数mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseForbidden('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseForbidden('参数email有误')

        # 保存用户传入的地址信息
        try:
            address = Address.objects.create(
                user=reqeust.user,
                title=receiver,  # 标题默认就是收货人
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email,
            )

            # 如果登录用户没有默认的地址，我们需要指定默认地址
            if not reqeust.user.default_address:
                reqeust.user.default_address = address
                reqeust.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '新增地址失败'})

        # 构造新增地址字典数据
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 响应新增地址结果：需要将新增的地址返回给前端渲染
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '新增地址成功', 'address': address_dict})


class DefaultAddressView(LoginRequiredJSONMixin, View):
    def put(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id)
            request.user.default_address = address
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '设置默认地址失败'})
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '设置默认地址成功'})


class UpdateDestroyAddressView(LoginRequiredMixin, View):

    def put(self, request, address_id):
        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        if not all([receiver, province_id, city_id, district_id,
                    place, mobile]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('参数mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7}(-[0-9]{1,4})?$)', tel):
                return http.HttpResponseForbidden('参数tel有误')
            if email:
                if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                    return http.HttpResponseForbidden('参数email有误')
        try:
            Address.objects.filter(id=address_id).update(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '修改地址失败'})

        address = Address.objects.get(id=address_id)
        address_dict = {
            "id": address.id,
            "tetiel": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '修改地址成功', 'address': address_dict})

    def delete(self, requset, address_id):
        try:
            address = Address.objects.get(id=address_id)
            address.is_deleted = True
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '删除地址失败'})
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '删除地址成功'})


class UpdateTitleAddressView(LoginRequiredMixin, View):

    def put(self, request, address_id):
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')

        if not title:
            return http.HttpResponseForbidden('缺少title')

        try:
            address = Address.objects.get(id=address_id)
            address.title = title
            address.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '更新标题失败'})
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '更新标题成功'})


class ChangePasswdView(View):

    def get(self, request):
        return render(request, 'user_center_pass.html')

    def post(self, request):
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')
        # if not all([old_password, new_password, new_password2]):
        #     return http.HttpResponseForbidden('缺少必要参数')
        try:
            request.user.check_password(old_password)
        except Exception as e:
            logger.error(e)
            return render(request, 'user_center_pass.html', {'origin_pwd_errmsg': '原始密码错误'})

        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password2):
            return http.HttpResponseForbidden('密码最少8位，最长20位')
        if new_password2 != new_password:
            return http.HttpResponseForbidden('两次输入的密码不一致')

        try:
            request.user.set_password(new_password)
            request.user.save()
        except Exception as e:
            logger.error(e)
            return render(request, 'user_center_pass.html', {'change_pwd_errmsg': '修改密码失败'})

        logout(request)
        response = redirect(reverse('users:login'))
        response.delete_cookie('username')

        return response


class UserBrowseHistory(LoginRequiredMixin, View):

    def get(self, request):

        """获取用户浏览记录"""
        # 获取Redis存储的sku_id列表信息
        redis_conn = get_redis_connection('history')
        sku_ids = redis_conn.lrange('history_%s' % request.user.id, 0, -1)

        # 根据sku_ids列表数据，查询出商品sku信息
        skus = []
        for sku_id in sku_ids:
            sku = models.SKU.objects.get(id=sku_id)
            skus.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price
            })

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'skus': skus})

    def post(self, request):
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')

        try:
            models.SKU.objects.get(id=sku_id)
        except models.SKU.DoesNotExist:
            return http.HttpResponseForbidden('sku不存在')

        redis_conn = get_redis_connection('history')
        p1 = redis_conn.pipeline()
        user_id = request.user.id
        p1.lrem('history_%s' % user_id, 0, sku_id)
        p1.lpush('history_%s' % user_id, sku_id)
        p1.ltrim('history_%s' % user_id, 0, 4)
        p1.execute()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})
