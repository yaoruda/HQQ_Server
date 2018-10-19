# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/10/17

from __future__ import absolute_import, unicode_literals
from celery import shared_task
import datetime

from hqq_chat import models as chat_models
from hqq_tool.rongcloud import RongCloud


@shared_task
def exit_join_user(chat_id, user_id):
    '''
    异步退出单聊参与者（并通知创建者）
    :param user_id:
    :param chat_id:
    :return:
    '''
    return_info = {'code': 0}
    update_time = datetime.datetime.now()
    result = chat_models.Chat.objects \
        .filter(id=chat_id, join_user_id=user_id, state=1, delete_mark=0) \
        .update(state=0, update_time=update_time)
    if result != 1:
        # 数据库失败
        return_info['code'] = 402
        return_info['description'] = '数据库失败：参与者{}退出单聊{}'.format(user_id, chat_id)
        return return_info

    # 数据库成功
    rongyun_api = RongCloud()
    # 融云Group.quit方法https://www.rongcloud.cn/docs/server.html#group_quit
    rongyun_return = rongyun_api.Group.quit(user_id, chat_id)
    if rongyun_return.result['code'] == 200:
        # 融云成功
        return_info['code'] = 200
        return_info['description'] = '数据库&融云成功：参与者{}退出单聊{}'.format(user_id, chat_id)
    else:
        # 融云失败：回滚数据库操作
        update_time = datetime.datetime.now()
        chat_models.Chat.objects \
            .filter(id=chat_id, join_user_id=user_id, state=0, delete_mark=0) \
            .update(state=1, update_time=update_time)
        return_info['code'] = 500
        return_info['description'] = '融云失败：参与者{}退出单聊{}'.format(user_id, chat_id)
        return return_info

    return return_info


@shared_task
def exit_create_user(chat_id, user_id, join_user_id=None):
    '''
    异步退出单聊创建者（删除单聊并通知参与者）
    :param chat_id:
    :param user_id:
    :param join_user_id:
    :return:
    '''
    return_info = {'code': 0}
    update_time = datetime.datetime.now()
    result = chat_models.Chat.objects \
        .filter(id=chat_id, create_user_id=user_id, delete_mark=0) \
        .update(state=2, update_time=update_time, delete_mark=1)
    if result != 1:
        # 数据库失败
        return_info['code'] = 402
        return_info['description'] = '数据库失败：创建者{}退出单聊{}'.format(user_id, chat_id)
        return return_info

    # 数据库成功
    rongyun_api = RongCloud()
    # 融云Group.dismiss方法https://www.rongcloud.cn/docs/server.html#group_dismiss
    rongyun_return = rongyun_api.Group.dismiss(user_id, chat_id)
    if rongyun_return.result['code'] == 200:
        # 融云成功
        return_info['code'] = 200
        return_info['description'] = '数据库&融云成功：创建者{}退出单聊{}'.format(user_id, chat_id)
    else:
        # 融云失败：回滚数据库操作
        update_time = datetime.datetime.now()
        if join_user_id:  # 存在参与者的情况回滚到state=1
            chat_models.Chat.objects \
                .filter(id=chat_id, create_user_id=user_id, state=2, delete_mark=1) \
                .update(state=1, delete_mark=0, update_time=update_time)
        else:
            chat_models.Chat.objects \
                .filter(id=chat_id, create_user_id=user_id, state=2, delete_mark=1) \
                .update(state=0, delete_mark=0, update_time=update_time)
        return_info['code'] = 500
        return_info['description'] = '融云失败：创建者{}退出单聊{}'.format(user_id, chat_id)
        return return_info

    return return_info

