# -*- coding: utf-8 -*-
# __author__= "suangsuang"
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
    id = models.CharField(max_length=32, verbose_name='一级话题id主键', primary_key=True)
    name = models.CharField(max_length=32, verbose_name="一级话题名称")
    state = models.SmallIntegerField(
        verbose_name='一级话题状态：正常启用0，不可用1',
        choices=((0, '正常'), (1, '不可用/关闭')),
        default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )

    def __str__(self):
        return FirstTopic.id

class SecondTopic(models.Model):
    '''
    ID 主键 自增 id
    一级话题名称
    二级话题名称
    创建时间
    更新时间
    删除标志
    '''
    id = models.CharField(max_length=32, verbose_name='二级话题id主键', primary_key=True)
    first_topic_id =models.CharField(max_length=32, verbose_name="一级话题id")
    name = models.CharField(max_length=32, verbose_name="二级话题名称")
    state = models.SmallIntegerField(
        verbose_name='2级话题状态：审核中2，不可用1，正常0',
        choices=((0, '正常'), (1, '删除'), (2, '审核中')),
        default=2)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )

    def __str__(self):
        return SecondTopic.id

class Meta:
    verbose_name = "话题模块"
    verbose_name_plural = verbose_name