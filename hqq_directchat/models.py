# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Date: 2018/10/19

from django.db import models
from hqq_user.models import MyUser
from hqq_topic.models import Topic


class DirectChat(models.Model):
    """
    私聊表:私聊ID及映射两个用户的关系
    """
    id = models.CharField(max_length=32, verbose_name='私聊ID', primary_key=True)
    remark = models.CharField(max_length=60, verbose_name='备注')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='话题外键')
    user_one = models.ForeignKey(MyUser, related_name='user_one', on_delete=models.CASCADE, verbose_name='用户1外键')
    user_two = models.ForeignKey(MyUser, related_name='user_two', on_delete=models.CASCADE, verbose_name='用户2外键')
    relationship = models.SmallIntegerField(
        verbose_name='关系',
        choices=((0, '未加好友'), (1, '已是好友')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class DirectChatMember(models.Model):
    """
    私聊用户表:一条私聊产生两个私聊用户表
    """
    id = models.CharField(max_length=32, verbose_name='表主键', primary_key=True)
    directchat = models.ForeignKey(DirectChat, on_delete=models.CASCADE, verbose_name='私聊外键')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    is_muted = models.SmallIntegerField(
        verbose_name='是否消息免打扰',
        choices=((0, '否'), (1, '是')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )
