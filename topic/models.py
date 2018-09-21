# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/19

from django.db import models


class FirstTopic(models.Model):
    '''
    ID 主键 自增 id
    一级话题名称
    创建时间
    更新时间
    删除标志
    '''

    name = models.CharField(max_length=32, verbose_name="一级话题名称")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(verbose_name='删除1，正常0', default=0)


class SecondTopic(models.Model):
    '''
    ID 主键 自增 id
    一级话题名称
    二级话题名称
    创建时间
    更新时间
    删除标志
    '''

    first_topic = models.ForeignKey(to=FirstTopic, related_name='secondtopic', on_delete=models.CASCADE,
                                    verbose_name='外键一级话题id')
    name = models.CharField(max_length=32, verbose_name="二级话题名称")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(verbose_name='删除1，正常0', default=0)
