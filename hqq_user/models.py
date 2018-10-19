# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/14

from django.db import models
from django.contrib.auth.models import User


class MyUser (models.Model):
    '''
    用户id user_id
    用户手机号 phone
    用户昵称 nickname
    用户年龄 age
    用户性别 gender
    用户状态 state

    用户登录时间 login_time(首次获取即为上一次登录时间，更新后即为本次登录时间)

    *用户头像下载地址 head_addr
    用户当前融云认证码 rongyun_token

    *用户位置坐标 location
    *用户城市位置 city
    *用户位置更新时间 location_time

    用户注册时间 create_time
    数据更新时间 update_time
    删除标志 delete_mark
    '''
    id = models.CharField(max_length=32, verbose_name='用户id主键', primary_key=True)
    phone = models.CharField(max_length=20, verbose_name='用户手机号')
    nickname = models.CharField(max_length=40, verbose_name='用户昵称')
    age = models.IntegerField(verbose_name='用户年龄')
    gender = models.SmallIntegerField(
        verbose_name='用户性别',
        choices=((0, '女'), (1, '男')),
        default=0
    )
    state = models.SmallIntegerField(
        verbose_name='用户状态',
        choices=((0, '正常'), (1, '异常')),
        default=0
    )
    login_time = models.DateTimeField(verbose_name='本次登录时间')
    portrait_url = models.CharField(max_length=256, verbose_name='用户头像url地址')
    rongyun_token = models.CharField(max_length=256, verbose_name='融云用户令牌')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Score(models.Model):
    id = models.CharField(max_length=32, verbose_name='用户得分id主键', primary_key=True)
    user_id = models.CharField(max_length=32, verbose_name='用户id主键')

    # user = models.OneToOneField(to=MyUser, related_name='score', on_delete=models.CASCADE, verbose_name='外键用户id')

    score = models.IntegerField(verbose_name='用户得分')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )

    def __str__(self):
        return self.user_id

    class Meta:
        verbose_name = "分数"
        verbose_name_plural = verbose_name


class Token(models.Model):
    id = models.CharField(max_length=32, verbose_name='Token_id主键', primary_key=True)
    user_id = models.CharField(max_length=32, verbose_name='用户id主键')
    token = models.CharField(max_length=256, verbose_name='api用Token')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )

    def __str__(self):
        return self.user_id

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = verbose_name


class VerifyCode(models.Model):
    '''
    短信验证码
    :用户外键
    :短信验证码
    :验证码更新时间
    '''
    id = models.CharField(max_length=32, verbose_name='验证码id主键', primary_key=True)
    phone = models.CharField(max_length=20, verbose_name='用户手机号')
    code = models.CharField(max_length=8, verbose_name='验证码')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "验证码"
        verbose_name_plural = verbose_name
