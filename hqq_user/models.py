# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Date: 2018/9/14

from django.db import models


class MyUser (models.Model):
    """
    用户信息
    """
    id = models.CharField(max_length=32, verbose_name='用户id主键', primary_key=True)
    phone = models.CharField(max_length=25, verbose_name='用户手机号', unique=True)
    nickname = models.CharField(max_length=50, verbose_name='用户昵称')
    birth = models.DateField(verbose_name='用户生日')
    gender = models.SmallIntegerField(
        verbose_name='用户性别',
        choices=((0, '女'), (1, '男')),
        default=0
    )
    state = models.SmallIntegerField(
        verbose_name='用户状态',
        choices=((0, '正常'), (1, '暂时封禁'), (2, '永久封禁')),
        default=0
    )
    ban_time = models.DateTimeField(auto_now_add=True, verbose_name='封禁截止时间')

    location = models.CharField(max_length=25, verbose_name='坐标', default='')
    city_code = models.CharField(max_length=32, verbose_name='所属城市id', default='')

    login_time = models.DateTimeField(auto_now_add=True, verbose_name='本次登录时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class Token(models.Model):
    """
    Token信息
    """
    id = models.CharField(max_length=32, verbose_name='Token_id主键', primary_key=True)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, verbose_name='外键用户id')
    token = models.CharField(max_length=256, verbose_name='登录Token', default='')
    rongyun_token = models.CharField(max_length=256, verbose_name='融云Token', default='')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class VerifyCode(models.Model):
    """
    验证码
    """
    id = models.CharField(max_length=32, verbose_name='验证码id主键', primary_key=True)
    phone = models.CharField(max_length=25, verbose_name='用户手机号', default='')
    code = models.CharField(max_length=8, verbose_name='验证码', default='')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class UserStatistic(models.Model):
    """
    用户统计表
    """
    id = models.CharField(max_length=32, verbose_name='用户统计表id', primary_key=True)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, verbose_name='外键用户id')
    group_amount = models.IntegerField(verbose_name='创建的群聊数量', default=0)
    dating_amount = models.IntegerField(verbose_name='创建的相亲角数量', default=0)
    ban_group_amount = models.IntegerField(verbose_name='', default=0)
    ban_forum_amount = models.IntegerField(verbose_name='', default=0)
    ban_reply_amount = models.IntegerField(verbose_name='', default=0)
    ban_discussion_amount = models.IntegerField(verbose_name='', default=0)
    ban_dating_amount = models.IntegerField(verbose_name='', default=0)
    unreal_report_amount = models.IntegerField(verbose_name='', default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class UserPortrait(models.Model):
    """
    用户头像
    """
    id = models.CharField(max_length=32, verbose_name='头像id主键', primary_key=True)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    url = models.CharField(max_length=50, verbose_name='头像url地址', default='')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )
