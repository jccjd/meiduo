# -*- coding:utf-8 -*-

# import ssl
# ssl._create_default_https_context =ssl._create_stdlib_context # 解决Mac开发环境下，网络错误的问题

from verifications.libs.yuntongxun.CCPRestSDK import REST

# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
_accountSid = '8a216da86d624ac4016daaee876b228a'

# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = 'a8e4ba087d644e0e8f6effd5f83c168f'

# 请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = '8a216da86d624ac4016daaee87c22291'

# 说明：请求地址，生产环境配置成app.cloopen.com
# _serverIP = 'sandboxapp.cloopen.com'
_serverIP = 'app.cloopen.com'

# 说明：请求端口 ，生产环境为8883
_serverPort = "8883"

# 说明：REST API版本号保持不变
_softVersion = '2013-12-26'

class CCP(object):
    """发送短信验证码的单例类"""

    def __new__(cls, *args, **kwargs):
        """
        定义单例的初始化方法
        :return: 单例
        """
        # 判断单例是否存在：_instance属性中存储的就是单例
        if not hasattr(cls, '_instance'):
            # 如果单例不存在，初始化单例
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)

            # 初始化REST SDK
            cls._instance.rest = REST(_serverIP, _serverPort, _softVersion)
            cls._instance.rest.setAccount(_accountSid, _accountToken)
            cls._instance.rest.setAppId(_appId)

        # 返回单例
        return cls._instance

    def send_template_sms(self, to, datas, tempId):
        """
        发送短信验证码单例方法
        :param to: 手机号
        :param datas: 内容数据
        :param tempId: 模板ID
        :return: 成功：0 失败：-1
        """
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        print(result)
        if result.get('statusCode') == '000000':
            return 0
        else:
            return -1



if __name__ == '__main__':
    # 注意： 测试的短信模板编号为1
    # sendTemplateSMS('17600992168', ['123456', 5], 1)

    # 单例类发送短信验证码
    CCP().send_template_sms('18336592633', ['123456', 5], 1)
