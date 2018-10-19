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
    if not topic_models.FirstTopic.objects.filter(name=name).first():
        new_first_topic = topic_models.FirstTopic(id=id, name=name)
        new_first_topic.save()
        return True


@shared_task
def add_new_second_topic(id, second_topic_name, first_topic):
    if not topic_models.SecondTopic.objects.filter(name=second_topic_name).first():
        new_second_topic = topic_models.SecondTopic(id=id, name=second_topic_name, first_topic_id=first_topic)
        new_second_topic.save()
        return True