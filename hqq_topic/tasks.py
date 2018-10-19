# -*- coding: utf-8 -*-
# __author__= "suangsuang"
# Data: 2018/10/16
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.task import Task
import time

from hqq_topic import models as topic_models
from hqq_tool import views as hqq_tool


@shared_task
def add_new_first_topic(id, name):
    new_first_topic = topic_models.FirstTopic(id=id, name=name)
    new_first_topic.save()
    return True
