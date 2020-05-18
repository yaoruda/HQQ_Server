# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Date: 2018/10/3

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.task import Task
import time

from hqq_user import models as user_models
from hqq_tool import hqq_tool as hqq_tool


@shared_task
def save_verify_code(verify_code, phone):
    is_exist = user_models.VerifyCode.objects.filter(phone=phone).update(code=verify_code)
    if is_exist:
        return_info = {'code': 200, 'operation': '更新{}的验证码'.format(phone)}
    else:
        verify_code_pk_id = hqq_tool.get_uuid()
        user_models.VerifyCode.objects.create(id=verify_code_pk_id,
                                              code=verify_code,
                                              phone=phone,
                                              state=0,
                                              )
        return_info = {'code': 200, 'operation': '新建{}的验证码'.format(phone)}
    return return_info


@shared_task
class CourseTask(Task):
    name = 'course-task'

    def run(self, *args, **kwargs):
        print('Start Task!')
        time.sleep(4)
        print('End Task!')


@shared_task
def add(x, y):
    print('Start Task!')
    time.sleep(4)
    print('End Task!')
    return x + y, 'aaa'


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
