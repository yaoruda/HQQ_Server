# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Date: 2018/10/21

from django.db import models
from hqq_user import models as user_models
from hqq_topic import models as topic_models


class Group(models.Model):
    """
    群聊
    """
    id = models.CharField(max_length=32, verbose_name='群聊id主键', primary_key=True)
    number = models.CharField(max_length=20, verbose_name='群号', unique=True)
    popularity = models.IntegerField(verbose_name='热度', default=0)
    member_amount = models.IntegerField(verbose_name='群聊人数', default=0)
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '可加入'), (1, '已满人')),
        default=0
    )

    create_user = models.ForeignKey(user_models.MyUser, related_name='create_user', on_delete=models.CASCADE, verbose_name='创建者')
    admin_user = models.ForeignKey(user_models.MyUser, related_name='admin_user', on_delete=models.CASCADE, verbose_name='群主')
    topic = models.ForeignKey(topic_models.Topic, on_delete=models.CASCADE, verbose_name='话题外键')
    location = models.CharField(max_length=50, verbose_name='坐标', default='')
    city_code = models.CharField(max_length=20, verbose_name='所属城市id', default='')

    title = models.CharField(max_length=32, verbose_name='标题', default='')
    url = models.CharField(max_length=50, verbose_name='群头像url地址', default='')
    introduction = models.TextField(max_length=280, verbose_name='群聊简介', default='')

    max_member = models.IntegerField(verbose_name='群聊最大人数', default=0)
    location_prefer = models.SmallIntegerField(
        verbose_name='距离偏好',
        choices=((0, '无所谓'), (1, '同城')),
        default=0
    )
    gender_prefer = models.SmallIntegerField(
        verbose_name='性别偏好',
        choices=((0, '无所谓'), (1, '男性可见'), (2, '女性可见')),
        default=0
    )
    age_prefer = models.SmallIntegerField(
        verbose_name='年龄偏好',
        choices=((0, '无所谓'), (1, '同龄人')),
        default=0
    )
    # v2
    # min_age_prefer = models.PositiveIntegerField(verbose_name='偏好最小年龄范围', default=0)
    # max_age_prefer = models.PositiveIntegerField(verbose_name='偏好最大年龄范围', default=100)

    question_amount = models.SmallIntegerField(
        verbose_name='问题数量',
        choices=((0, '关闭'), (1, '数量为1')),
        default=0
    )
    question = models.CharField(max_length=50, verbose_name='加群提问问题', default='')
    ban_mark = models.SmallIntegerField(
        verbose_name='封禁状态',
        choices=((0, '无'), (1, '半封禁'), (2, '全封禁')),
        default=0
    )
    refresh_time = models.DateTimeField(auto_now_add=True, verbose_name='刷新置顶时间')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class GroupMember(models.Model):
    """
    群聊成员信息
    """
    id = models.CharField(max_length=32, verbose_name='群聊成员id主键', primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='群聊外键')
    user = models.ForeignKey(user_models.MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    is_muted = models.SmallIntegerField(
        verbose_name='是否消息免打扰',
        choices=((0, '否'), (1, '是')),
        default=0
    )
    chat_permission = models.SmallIntegerField(
        verbose_name='私聊许可',
        choices=((0, '不允许'), (1, '允许')),
        default=1
    )
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '群主'), (2, '已被踢出'), (3, '曾经主动退出')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ApplicationForGroup(models.Model):
    """
    申请加群表
    """
    id = models.CharField(max_length=32, verbose_name='主键', primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='群聊外键')
    user = models.ForeignKey(user_models.MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '待审核'), (1, '通过'), (2, '拒绝')),
        default=0
    )
    question_amount = models.SmallIntegerField(
        verbose_name='问题数量',
        choices=((0, '关闭'), (1, '数量为1')),
        default=0
    )
    question = models.CharField(max_length=50, verbose_name='加群提问问题', default='')
    answer = models.CharField(max_length=60, verbose_name='加群问题回答', default='')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )
