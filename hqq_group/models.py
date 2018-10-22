# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/10/21
from django.db import models
'''
群组id grou_id
群组标题 grou_title
创建者的用户id fk_creator_id
群组介绍 grou_intro

一级话题
二级话题

*群组年龄偏好 grou_age_prefer
*群组性别偏好 grou_gender_prefer
*群组距离偏好 grou_location_prefer

群组头像下载地址 grou_headpic

*群组坐标位置 grou_location
*群组所属城市 grou_city

?上一次聊天时间 grou_lastchat_time

加群问题状态
加群问题



群组热度 grou_popularity
创建时间 create_time
更新时间 refresh_time
删除标志 delete_mark
'''


class Group(models.Model):
    id = models.CharField(max_length=32, verbose_name='群聊id主键', primary_key=True)
    title = models.CharField(max_length=32, verbose_name='标题')

    create_user_id = models.CharField(max_length=32, verbose_name='创建者id')
    admin_user_id = models.CharField(max_length=32, verbose_name='群主id')
    description = models.CharField(max_length=300, verbose_name='群聊简介')

    first_topic_id = models.CharField(max_length=32, verbose_name='一级话题id')
    second_topic_id = models.CharField(max_length=32, verbose_name='二级话题id')

    # TODO:添加偏好的字段18。10。21
    # TODO:添加location与city
    portrait_url = models.CharField(max_length=256, verbose_name='群头像url地址')

    popularity = models.IntegerField(verbose_name='热度')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '可加入'), (1, '已满人'), (2, '已删除'), (3, '已封禁'), (4, '私聊创建时融云失败')),
    )
    member_number = models.SmallIntegerField(verbose_name='群聊人数')
    max_member_number = models.SmallIntegerField(verbose_name='群聊最大人数')
    question_state = models.SmallIntegerField(
        verbose_name='是否开启加群审核',
        choices=((0, '关闭'), (1, '开启')),
        default=0
    )
    question = models.CharField(max_length=100, verbose_name='加群提问问题')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )

    def __str__(self):
        return Group.id

    class Meta:
        verbose_name = "群聊"
        verbose_name_plural = verbose_name


class GroupMember(models.Model):
    '''
    id
    群组id group_id
    组员id
    状态
    加群问题回答
    '''
    id = models.CharField(max_length=32, verbose_name='群聊成员id主键', primary_key=True)
    group_id = models.CharField(max_length=32, verbose_name='群聊id主键')
    user_id = models.CharField(max_length=32, verbose_name='参与群聊的此用户id主键')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '已被禁言'), (2, '已主动退群'), (3, '已被踢出'), (4, '融云创建时错误')),
    )
    answer = models.CharField(max_length=100, verbose_name='加群问题回答')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )

    def __str__(self):
        return GroupMember.group_id

    class Meta:
        verbose_name = "群聊成员信息"
        verbose_name_plural = verbose_name
