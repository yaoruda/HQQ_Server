# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/14

import hashlib
import time
import random

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from user import models
from user import serializers
from DRF import auth


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = models.MyUser.objects.all()
    serializer_class = serializers.MyUserSerializer
    authentication_classes = [auth.APIAuth, ]
    lookup_field = 'id'


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = models.Score.objects.all()
    serializer_class = serializers.ScoreSerializer
    authentication_classes = [auth.APIAuth, ]
    lookup_field = 'user'


class TokenViewSet(viewsets.ModelViewSet):
    queryset = models.Token.objects.all()
    serializer_class = serializers.TokenSerializer
    authentication_classes = [auth.APIAuth, ]
    lookup_field = 'user'

    # 创建=的时候，自动引用当前登录用户
    def perform_create(self, serializer):   # 重写：修改保存实例的方法，使之能够接收传递的更多消息
        serializer.save(operator=self.request.user) # 序列化器的create方法现在将被传递一个附加的operator字段以及来自请求的验证数据


def get_random_token(phone):
    """
    根据用户手机号和时间戳生成随机token
    :param phone:用户手机号
    :return 16进制md5码摘要信息
    """
    timestamp = str(time.time())
    m = hashlib.md5(bytes(phone, encoding="utf8"))  # 基于phone生成md5码
    m.update(bytes(timestamp, encoding="utf8"))  # 基于当前时间更新md5码
    '''
    hash.digest() 
    返回摘要，作为二进制数据字符串值
    hash.hexdigest() 
    返回摘要，作为十六进制数据字符串值
    '''
    return m.hexdigest()  # 返回生成md5码的摘要信息（保存的位置等）


class VerifyToken(APIView):
    """
    校验token
    :param phone:用户手机号
    :return
    """
    def post(self, request):
        # POST,data,在request里保存的都是空，只有query_params有东西，不知道为啥
        phone = request.query_params.get('phone')
        user = models.MyUser.objects.filter(phone=phone).first()
        if user:  # 存在用此手机号注册的用户
            token = get_random_token(phone)
            models.Token.objects.update_or_create(defaults={"token": token}, user=user)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(dict({'token': token}), status=status.HTTP_200_OK)


class SendVerifyCode(APIView):
    '''
    发送验证码
    '''
    def post(self, request):
        phone = request.query_params.get('phone')
        if not phone:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        code = random.randint(100, 999)
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # TODO:发送验证码...

        if True:  # 发送验证码成功
            models.VerifyCode.objects.update_or_create(defaults={"code": code, "phone": phone})
            return Response(dict({'code': code}), status=status.HTTP_200_OK)
        # else:
            # TODO:处理短信验证码发送失败的情况


def register_new_user(phone):  # 初始化一个用户
    # TODO: 类似这种地方的try和catch以后要加上
    new_user = models.MyUser(phone=phone, age=0)
    new_user.save()

    new_user_score = models.Score(score=12000, user=new_user)
    token = get_random_token(phone)  # 给用户下发访问Token
    new_user_token = models.Token(token=token, user=new_user)
    new_user_score.save()
    new_user_token.save()

    return new_user.pk

from rest_framework.exceptions import APIException
class RegisterAndLogin(APIView):
    '''
    （注册）并登录
    '''
    def post(self, request):
        response = {'code': 0}
        try:
            phone = request.query_params.get('phone')  # 不一定是已注册用户的手机号
        except APIException:
            response['code'] = 1
            response['error'] = "请求缺少字段:phone"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        code = request.query_params.get('code')
        if not code:
            response['code'] = 1
            response['error'] = "请求缺少字段:phone"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        is_registered = models.MyUser.objects.filter(phone=phone).first()  # 去用户表里查用户，有：
        if is_registered:  # 已经注册的用户->直接登录
            # TODO:if有登录后首页之前的逻辑的完善
            token = get_random_token(phone)  # 给用户下发访问Token
            response['token'] = token
            response['execute'] = "Login"
            return Response(response, status=status.HTTP_200_OK)
        else:  # 未注册的用户->直接注册
            # TODO:注册新用户逻辑的完善
            user_id = register_new_user(phone)  # 注册到用户表、score表、token表
            response['user_id'] = user_id
            response['execute'] = "Register"
            return Response(response, status=status.HTTP_201_CREATED)
