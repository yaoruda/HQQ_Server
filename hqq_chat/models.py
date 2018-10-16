# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/10/11

from django.db import models

'''
单聊唯一标识 chat_id
单聊创建者的用户id fk_user_id
（唯一）参与用户id
单聊一级话题 fk_chat_topic
单聊二级话题 

单聊标题 chat_title
单聊年龄偏好 chat_age_prefer
单聊性别偏好 chat_gender_prefer
单聊距离偏好 chat_location_prefer

单聊坐标位置 chat_location
单聊所属城市 chat_city

单聊热度 chat_popularity
单聊状态 chat_state
创建时间 create_time
更新时间 refresh_time
删除标志 delete_mark
'''


class Chat(models.Model):
    id = models.CharField(max_length=32, verbose_name='单聊id主键', primary_key=True)
    create_user_id = models.CharField(max_length=32, verbose_name='创建者id')
    join_user_id = models.CharField(max_length=32, verbose_name='参与者id')
    first_topic_id = models.CharField(max_length=32, verbose_name='一级话题id')
    second_topic_id = models.CharField(max_length=32, verbose_name='二级话题id')

    title = models.CharField(max_length=32, verbose_name='单聊标题')
    # TODO:添加偏好的字段18。10。14
    # TODO:添加location与city

    popularity = models.IntegerField(verbose_name='热度')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '待加入'), (1, '已满人')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除'), (2, ''), (3, '')),
        default=0
    )

    def __str__(self):
        return Chat.id

    class Meta:
        verbose_name = "单聊"
        verbose_name_plural = verbose_name
