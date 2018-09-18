import hashlib
import time
import random

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from users import models
from users import serializers
from users import auth

# TODO:开发用待删除
import logging
logging.getLogger().setLevel(logging.INFO)

class MyUserViewSet(viewsets.ModelViewSet):
    queryset = models.MyUser.objects.all()
    serializer_class = serializers.MyUserSerializer
    permission_classes = ()
    authentication_classes = [auth.APIAuth, ]
    lookup_field = 'id'


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = models.Score.objects.all()
    serializer_class = serializers.ScoreSerializer
    permission_classes = ()
    lookup_field = 'user'


class TokenViewSet(viewsets.ModelViewSet):
    queryset = models.TokenLogin.objects.all()
    serializer_class = serializers.TokenSerializer
    permission_classes = ()

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
            models.TokenLogin.objects.update_or_create(defaults={"token": token}, user=user)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(dict({'token': token}), status=status.HTTP_200_OK)


class SendVerifyCode(APIView):
    '''
    发送验证码
    '''
    def post(self, request):
        phone = request.query_params.get('phone')
        user = models.MyUser.objects.filter(phone=phone).first()
        if not user:  # 存在用此手机号注册的用户
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        code = random.randint(100, 999)
        # TODO:发送验证码...

        if True:  # 发送验证码成功
            models.VerifyCode.objects.update_or_create(defaults={"code": code}, user=user)
            return Response(dict({'code': code}), status=status.HTTP_200_OK)
        # else:
            # TODO:处理短信验证码发送失败的情况


class RegisterAndLogin(APIView):
    '''
    （注册）并登录
    '''
    def post(self, request):
        phone = request.query_params.get('phone')  # 不一定是已注册用户的手机号
        code = request.query_params.get('code')
        try:
            models.VerifyCode.objects.get(phone=phone, )
        except models.User.DoesNotExist:  # 如果抛出的异常是"不存在"，返回没有找到
                return Response(status=status.HTTP_404_NOT_FOUND)

        user = models.MyUser.objects.filter(phone=phone).first()

        # if user:
