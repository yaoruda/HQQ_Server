# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/15
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from hqq_user import models

'''
要实现自定义身份验证方案，请继承 BaseAuthentication 并重写 .authenticate(self, request) 方法。
如果认证成功，该方法应返回 (hqq_user, auth) 的二元组，否则返回 None。
'''


class APIAuth(BaseAuthentication):
    '''
    自定义API调用权限："POST", "PUT", "DELETE" 验证用户Token
    '''
    def authenticate(self, request):
        if request.method in ["POST", "PUT", "DELETE", "GET"]:
            request_token = request.query_params.get("token", None)
            if not request_token:
                # 请求缺少Token字段
                raise AuthenticationFailed('缺少token')

            # 在Token表中看是否存在此Token
            # filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表。
            # .first(): Return the first object of a query or None if no match is found.
            token_obj = models.Token.objects.filter(token=request_token).first()
            if not token_obj:
                # 如果找不到一样的，那么Token是假的
                raise AuthenticationFailed('无效的token')
            # 如果找到了，则返回TokenLogin对象中代表用户的外键user指向的用户表的nickname字段
            else:
                print("token_obj_user_username=" + str(token_obj.user.nickname))
                return token_obj.user.nickname, None
        else:
            # 其他request method的情况
            return None, None
