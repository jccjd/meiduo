import random
from venv import logger

from django import http
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from django_redis import get_redis_connection
# Create your views here.
from meiduo.utils.response_code import RETCODE
from verifications import constants
from verifications.libs.captcha.captcha import captcha
from verifications.libs.yuntongxun.ccp_sms import CCP
from meiduo.celery_tasks.sms.tasks import send_sms_code

class ImageCodeView(View):
    """图形验证码"""

    def get(self, reqeust, uuid):
        """
        :param reqeust: 
        :param uuid: 通用唯一识别码，用于唯一标识该图形验证码属于哪个用户的
        :return: image/jpg
        """
        # 实现主体业务逻辑：生成，保存，响应图形验证码
        # 生成图形验证码
        text, image = captcha.generate_captcha()

        # 保存图形验证码
        redis_conn = get_redis_connection('verify_code')
        # redis_conn.setex('key', 'expires', 'value')
        redis_conn.setex('img_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        # 响应图形验证码
        return http.HttpResponse(image, content_type='image/jpg')


class SMSCodeView(View):
    """短信验证码"""

    def get(self, reqeust, mobile):
        """
        :param reqeust: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        # 接收参数
        image_code_client = reqeust.GET.get('image_code')
        uuid = reqeust.GET.get('uuid')

        # 校验参数
        if not all([image_code_client, uuid]):
            return http.JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少必传参数'})

        # 创建连接到redis的对象
        redis_conn = get_redis_connection('verify_code')
        # 提取图形验证码
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            # 图形验证码过期或者不存在
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码失效'})
        # 删除图形验证码，避免恶意测试图形验证码
        try:
            redis_conn.delete('img_%s' % uuid)
        except Exception as e:
            logger.error(e)

        image_code_server = image_code_server.decode()  # bytes转字符串
        if image_code_client.lower() != image_code_server.lower():  # 转小写后比较
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入图形验证码有误'})

        sms_code = '%06d' % random.randint(0, 999999)
        logger.info(sms_code)

        # set a flag to block message sending request

        # send_flag = redis_conn.get("send_flag_%s" % mobile)
        # if send_flag:
        #     return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '短信发送过于频繁'})

        # redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # redis_conn.setex('send_flag_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, 1)

        # use pipeline version

        pipe = redis_conn.pipeline()
        pipe.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pipe.setex('send_flag_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, 1)
        pipe.execute()

        # 发送短信验证码
        # CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],
        #                         constants.SEND_SMS_TEMPLATE_ID)

        send_sms_code(mobile, sms_code)
        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信成功'})
