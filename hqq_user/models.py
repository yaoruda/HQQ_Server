# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/14

from django.db import models
from django.contrib.auth.models import User


class MyUser (models.Model):
    '''
    用户id user_id
    用户手机号 phone
    用户认证码 auth_code
    用户昵称 nickname
    用户当前融云认证码 rongyun_code
    用户年龄 age
    用户性别 gender
    用户头像下载地址 head_addr
    用户位置坐标 location
    用户城市位置 city
    用户位置更新时间 location_time
    用户分数 score
    用户状态 state
    用户注册时间 regist_time
    用户上一次登录时间 login_time
    数据创建时间 create_time
    数据更新时间 refresh_time
    删除标志 delete_mark
    '''

    phone = models.CharField(max_length=20, verbose_name='用户手机号', unique=True)
    nickname = models.CharField(max_length=40, verbose_name='用户昵称', unique=True)
    age = models.IntegerField(verbose_name='用户年龄', default=0)
    gender = models.SmallIntegerField(
        verbose_name='用户性别',
        choices=((0, '女'), (1, '男')),
        default=0
    )


class Score(models.Model):
    user = models.OneToOneField(to=MyUser, related_name='score', on_delete=models.CASCADE, verbose_name='外键用户id')
    score = models.IntegerField(verbose_name='用户得分')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    state = models.SmallIntegerField(verbose_name='删除1，正常0', default=0)


class Token(models.Model):
    user = models.OneToOneField(to=MyUser, related_name='token', on_delete=models.CASCADE, verbose_name='外键用户id')
    token = models.CharField(max_length=256, verbose_name='api用Token')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    state = models.SmallIntegerField(verbose_name='删除1，正常0', default=0)


class VerifyCode(models.Model):
    '''
    短信验证码
    :用户外键
    :短信验证码
    :验证码更新时间
    '''
    phone = models.CharField(max_length=20, verbose_name='用户手机号', unique=True)
    code = models.CharField(max_length=8, verbose_name='验证码')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    state = models.SmallIntegerField(verbose_name='删除1，正常0', default=0)
