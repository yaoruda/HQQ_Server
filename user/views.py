# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/14

import hashlib
import time
import random

from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from user import models
from user import tasks


import logging


class VerifyToken(APIView):
    """
    校验token
    :param phone:用户手机号
    :return
    """
    def post(self, request):
        # POST,data,在request里保存的都是空，只有query_params有东西，不知道为啥
        return_info = {'code': 0}
        request_params = {}
        request_params['phone'] = request.query_params.get('phone')
        request_params['token'] = request.query_params.get('token')  # old_token
        if is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        phone = request_params.get('phone')
        old_token = request_params.get('token')
        old_token_info = models.Token.objects.values('create_time', 'user_id').filter(token__exact=old_token).first()
        if old_token_info:  # 如果存在此token，获取它的时间和外键值（用户id）
            create_time = old_token_info['create_time']
            user_id = old_token_info['user_id']
            result = verify_token_time(create_time)  # 检验Token是否过期
            if result:
                # Token未过期
                return_info['code'] = 0
                return_info['info'] = 'Token验证成功'
                return_info['user_id'] = user_id
                new_token = refresh_token(user_id, phone)  # 分配新Token
                return_info['new_token'] = new_token
                return Response(return_info, status=status.HTTP_200_OK)
            else:
                # Token过期
                return_info['code'] = 1
                return_info['info'] = 'Token已过期'
                return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        else:
            return_info['code'] = 1
            return_info['info'] = 'Token不合法'
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)


class SendVerifyCode(APIView):
    '''
    发送验证码
    '''
    def get(self, request):
        return_info = {'code': 200}
        request_params = {}
        request_params['phone'] = request.query_params.get('phone')
        if is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        phone = request_params.get('phone')
        verify_code = random.randint(100, 999)  # 生成随机3位验证码
        # TODO:发送验证码...

        if True:  # 发送验证码成功
            models.VerifyCode.objects.update_or_create(defaults={"code": verify_code, "phone": phone})
            return_info['verify_code'] = verify_code
            return Response(return_info, status=status.HTTP_200_OK)
        # else:
            # TODO:处理短信验证码发送失败的情况


class RegisterAndLogin(APIView):
    '''
    （注册）并登录
    '''
    def post(self, request):
        return_info= {'code': 200}
        request_params = {}
        request_params['phone'] = request.query_params.get('phone')  # 不一定是已注册用户的手机号
        request_params['code'] = request.query_params.get('code')  # 用户填写的短信验证码
        if is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        #  检验验证码正确与否
        phone = request_params.get('phone')
        code = request_params.get('code')
        if is_code_correct(phone, code):
            is_registered = models.MyUser.objects.filter(phone=phone).first()
            if is_registered:  # 已经注册的用户->直接登录
                # TODO:if有登录后首页之前的逻辑的完善
                token = get_random_token(phone)  # 给用户下发访问Token
                return_info['token'] = token
                return_info['execute'] = "登录"
                return Response(return_info, status=status.HTTP_200_OK)
            else:  # 未注册的用户->直接注册
                # TODO:注册新用户逻辑的完善
                user_id = register_new_user(phone)  # 注册到用户表、score表、token表
                return_info['user_id'] = user_id
                return_info['execute'] = "注册"
                return Response(return_info, status=status.HTTP_200_OK)
        else:
            # 短信验证码错误
            return_info['code'] = 401
            return_info['error'] = "短信验证码错误"
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        log = logging.getLogger()
        # 执行异步任务
        log.error(str(time.time()) + 'Start Request')
        result = tasks.add.delay(2, 4)
        print(str(time.time()) + 'End Request')
        print(result.get())
        time.sleep(5)
        print(result.ready())
        return Response(dict({'result': 'ok'}))


class ChangeScore(APIView):
    '''
    增加用户分
    ～参数：
    1. UserID,
    2. 修改分数的类别(1：年龄段,2：一级话题,3：二级话题)
    3. 具体分数
    '''

    def post(self, request):
        return_info = {'code': 200}
        request_params = {}
        request_params['user'] = request.query_params.get('user')
        request_params['operation'] = request.query_params.get('operation')
        request_params['value'] = request.query_params.get('value')
        if is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        return Response(return_info)


def is_request_empty(request_params, return_info):
    '''
    检测request参数是否缺失
    :param request_params:
    :param return_info:
    :return:
    '''
    for param_name, param_value in request_params.items():
        if not param_value:  # 未获得此参数（None）
            message = '请求缺少字段:' + str(param_name)
            add_response(400, message, return_info)
            return True
    return False


def add_response(code, message, return_info):
    '''
    在return_info中修改code并添加信息
    :param code:
    :param message:
    :param return_info:
    :return:
    '''
    return_info['code'] = code
    return_info['message'] = message
    return return_info


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
    #  TODO:生成Token的规则
    # return m.hexdigest()  # 返回生成md5码的摘要信息（保存的位置等）
    return 'c7b85ef9eee971cf111eb897629e3d13'


def verify_token_time(create_time):
    time_expiration = 20  # 60 * 60 * 24 * 7
    time_now = time.time()
    # 转换成时间数组
    create_time = time.strptime(str(create_time), "%Y-%m-%d %H:%M:%S.%f")
    # 转换成时间戳
    create_time = time.mktime(create_time)
    if create_time + time_expiration > time_now:
        return True
    else:
        return False


def refresh_token(user_id, phone):
    new_token = get_random_token(phone)
    models.Token.objects.filter(user_id__exact=user_id).update(token=new_token)
    return new_token


def is_code_correct(phone, code):  # 检验验证码正确与否
    correct_code = models.VerifyCode.objects.values('code').filter(phone__exact=phone).first()
    if code == correct_code['code']:
        return True
    else:
        return False


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
