# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Date: 2018/11/30
from django.db import models
from hqq_user.models import MyUser


class Blacklist(models.Model):
    id = models.CharField(max_length=32, verbose_name='黑名单表主键', primary_key=True)
    user = models.ForeignKey(MyUser, related_name='blacklist_user', verbose_name='用户外键', on_delete=models.CASCADE)
    user_other = models.ForeignKey(MyUser, related_name='blacklist_user_other', verbose_name='被拉黑用户外键', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )
