# -*- coding: utf-8 -*-
# __author__= "suangsuang"
# Date: 2018/9/19

from django.db import models
from hqq_user.models import MyUser


class Category(models.Model):
    """
    ID 主键 自增 id
    一级话题名称
    创建时间
    更新时间
    删除标志
    """
    id = models.CharField(max_length=32, verbose_name='话题id主键', primary_key=True)
    name = models.CharField(max_length=32, verbose_name="话题类别名称")
    state = models.SmallIntegerField(
        verbose_name='话题类别状态：正常启用0，不可用1',
        choices=((0, '正常'), (1, '关闭')),
        default=0)
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class Topic(models.Model):
    """
    话题
    """
    id = models.CharField(max_length=32, verbose_name='话题id主键', primary_key=True)
    category = models.ForeignKey(Category, verbose_name='话题类别', on_delete=models.CASCADE)
    name = models.CharField(max_length=32, verbose_name="话题名称")
    url = models.CharField(max_length=50, verbose_name="话题图片id")
    small_url = models.CharField(max_length=50, verbose_name="主页话题小图片id")
    state = models.SmallIntegerField(
        verbose_name='话题状态',
        choices=((0, '正常'), (1, '关闭')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class Statistic(models.Model):
    """
    话题统计表
    """
    id = models.CharField(max_length=32, verbose_name='用户统计表id', primary_key=True)
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE, verbose_name='话题外键')
    popularity = models.IntegerField(verbose_name='热度', default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ApplyTopic(models.Model):
    """
    申请话题
    """

    id = models.CharField(max_length=32, verbose_name='话题id主键', primary_key=True)
    user = models.ForeignKey(MyUser, verbose_name='用户', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name="话题名称")
    reason = models.TextField(verbose_name="理由")
    state = models.SmallIntegerField(
        verbose_name='话题状态',
        choices=((0, '待处理'), (1, '已处理')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class CommendTopic(models.Model):
    """
    推荐的话题列表
    """
    id = models.CharField(max_length=32, verbose_name='推荐话题表主键', primary_key=True)
    topic = models.ForeignKey(Topic, verbose_name='话题id外键', on_delete=models.CASCADE)
    gender = models.SmallIntegerField(
        verbose_name='匹配的性别',
        choices=((0, '女'), (1, '男')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )
