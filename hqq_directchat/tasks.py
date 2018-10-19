# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/10/19

from __future__ import absolute_import, unicode_literals
from celery import shared_task
import datetime

from hqq_directchat import models as directchat_models
from hqq_tool.rongcloud import RongCloud


@shared_task
def ExitDirectChat(chat_id):
    chat = directchat_models.DirectChat.objects.filter(id=chat_id).first()
    chat.state = 1
    chat.delete_mark = 1
    chat.save()
    return '删除私聊{}成功'.format(chat_id)
