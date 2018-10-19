# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/10/19

from django.db import models


class DirectChat(models.Model):
    id = models.CharField(max_length=32, verbose_name='私聊id主键', primary_key=True)
    user_id_1 = models.CharField(max_length=32, verbose_name='用户1的id')
    user_id_2 = models.CharField(max_length=32, verbose_name='用户2的id')

    user_id_1_name = models.CharField(max_length=32, verbose_name='用户1的nickname')
    user_id_2_name = models.CharField(max_length=32, verbose_name='用户2的nickname')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '私聊正常'), (1, '已删除'), (2, '已封禁'), (3, '私聊创建时融云失败')),
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )

    def __str__(self):
        return DirectChat.id

    class Meta:
        verbose_name = "私聊"
        verbose_name_plural = verbose_name
