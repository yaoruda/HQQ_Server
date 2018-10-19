# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/10/19

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hqq_tool import views as hqq_tool
from hqq_tool.rongcloud import RongCloud
from hqq_directchat import models as directchat_models
from hqq_user import views as user_views
from hqq_directchat import tasks as directchat_tasks


class MakeDirectChat(APIView):
    def post(self, request):
        '''
        直接创建双人单聊（私聊）
        此私聊题目为相互来说对方的nickname，且任何一人退出后私聊即解散
        :param request:
        :return:
        '''
        return_info = {'code': 0}
        request_params_name = [
            'user_id_1',
            'user_id_2',
        ]
        request_params = {}
        for param in request_params_name:
            request_params[param] = request.query_params.get(param)
        if hqq_tool.is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        user_id_1 = request_params.get(request_params_name[0])
        user_id_2 = request_params.get(request_params_name[1])

        chat = is_direct_chat_users_exist(user_id_1, user_id_2)
        if chat:
            if chat['state'] == 0:
                # 如果存在这两位用户的私聊，即返回私聊id
                chat_id = chat['id']
                return_info['code'] = 201
                return_info['description'] = '已经存在此私聊'
                return_info['chat_id'] = chat_id
                return Response(return_info, status=status.HTTP_200_OK)
            elif chat['state'] == 2:
                return_info['code'] = 401
                return_info['description'] = '此私聊已被封禁'
                return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
            else:  # state异常情况，设置为已删除，之后继续开启新私聊
                chat = directchat_models.DirectChat.objects.filter(id=chat['id']).first()
                chat.state = 1
                chat.delete_mark = 1
                chat.save()

        # 私聊不存在，或者state=1或3的情况：新建私聊
        # state状态：(0, '私聊正常'), (1, '已删除'), (2, '已封禁'), (3, '私聊创建时融云失败')
        new_chat_id = hqq_tool.get_uuid()
        user_id_1_name = user_views.get_user_nickname(user_id_1)
        user_id_2_name = user_views.get_user_nickname(user_id_2)
        new_chat = directchat_models.DirectChat(id=new_chat_id, user_id_1=user_id_1, user_id_2=user_id_2,
                                                user_id_1_name=user_id_1_name, user_id_2_name=user_id_2_name, state=0)
        new_chat.save()

        rongyun_api = RongCloud()
        rongyun_return = rongyun_api.Group.create_direct_chat(user_id_1, user_id_2, new_chat_id, '私聊')
        if rongyun_return.result['code'] == 200:
            return_info['code'] = 200
            return_info['chat_id'] = new_chat_id
            return Response(return_info, status=status.HTTP_200_OK)
        else:
            new_chat.state = 3
            new_chat.delete_mark = 1
            new_chat.save()
            return_info['code'] = 500
            return_info['description'] = '创建私聊失败（融云方面）'
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)


class ExitDirectChat(APIView):
    def post(self, request):
        '''
        退出（删除）双人单聊（私聊）
        :param request:
        :return:
        '''
        return_info = {'code': 0}
        request_params_name = [
            'chat_id',  # 私聊id
            'user_id',  # 此用户id
            'other_user_id',  # 对方用户id
        ]
        request_params = {}
        for param in request_params_name:
            request_params[param] = request.query_params.get(param)
        if hqq_tool.is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        chat_id = request_params.get(request_params_name[0])
        user_id = request_params.get(request_params_name[1])
        other_user_id = request_params.get(request_params_name[2])

        if not is_direct_chat_id_exist(chat_id, return_info):
            # direct_chat_id不存在
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        elif not user_views.is_user_exist(user_id, return_info):
            # user不存在
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        elif is_direct_chat_delete(chat_id, return_info):
            # direct_chat被删除
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        elif not is_direct_chat_id_user_exist(chat_id, user_id):
            return_info['code'] = 401
            return_info['description'] = '此用户id与私聊id不匹配'
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

        chat = is_direct_chat_id_users_exist(chat_id, user_id, other_user_id)
        if chat:
            if chat['state'] == 0:
                directchat_tasks.ExitDirectChat.delay(chat_id)
                return_info['code'] = 200
                return_info['description'] = '删除私聊成功'
                return Response(return_info, status=status.HTTP_200_OK)
            else:  # state == 1（已删除）、2（已封禁）、3（私聊创建时融云失败）、及其他时，确保将delete_mark=1
                chat = directchat_models.DirectChat.objects.filter(id=chat_id).first()
                chat.delete_mark = 1
                chat.save()
                return_info['code'] = 200
                return_info['description'] = '删除私聊成功'
        else:  # chat_id, user_id与other_user_id不匹配
            return_info['code'] = 402
            return_info['description'] = '对方用户id不匹配'
            return Response(return_info, status=status)


def is_direct_chat_id_exist(chat_id, return_info):
    '''
    查看私聊id私否存在
    :param chat_id:
    :param return_info:
    :return:
    '''
    if directchat_models.DirectChat.objects.filter(id=chat_id).first():
        return True
    else:
        return_info['code'] = 404
        return_info['description'] = '此聊天不存在'
        return False


def is_direct_chat_delete(chat_id, return_info):
    '''
    根据私聊id，返回私聊是否被删除
    :param chat_id:
    :param return_info:
    :return:
    '''
    if directchat_models.DirectChat.objects.filter(id=chat_id, delete_mark=1).first():
        return_info['code'] = 404
        return_info['description'] = '此聊天已被删除'
        return True
    else:
        return False


def is_direct_chat_users_exist(user_id_1, user_id_2):
    '''
    根据两个用户id寻找是否存在此私聊并返回状态等信息
    :param user_id_1:
    :param user_id_2:
    :return:
    '''
    chat = directchat_models.DirectChat.objects.values('id', 'state') \
        .filter(user_id_1=user_id_1, user_id_2=user_id_2, delete_mark=0) \
        .first()
    if chat:
        return chat
    else:
        chat = directchat_models.DirectChat.objects.values('id', 'state') \
            .filter(user_id_1=user_id_2, user_id_2=user_id_1, delete_mark=0) \
            .first()
        if chat:
            return chat
    return None


def is_direct_chat_id_user_exist(chat_id, user_id):
    '''
    根据私聊id和一个用户id，检测私聊是否存在
    :param chat_id:
    :param user_id:
    :return:
    '''
    chat = directchat_models.DirectChat.objects \
        .filter(id=chat_id, user_id_1=user_id) \
        .first()
    if chat:
        return True
    else:
        chat = directchat_models.DirectChat.objects \
            .filter(id=chat_id, user_id_2=user_id) \
            .first()
        if chat:
            return True
    return False


def is_direct_chat_id_users_exist(chat_id, user_id_1, user_id_2):
    '''
    根据私聊id、两个用户id返回私聊状态(检测私聊是否存在)
    :param chat_id:
    :param user_id_1:
    :param user_id_2:
    :return:
    '''
    chat = directchat_models.DirectChat.objects.values('state') \
        .filter(id=chat_id, user_id_1=user_id_1, user_id_2=user_id_2, delete_mark=0) \
        .first()
    if chat:
        return chat
    else:
        chat = directchat_models.DirectChat.objects.values('state') \
            .filter(id=chat_id, user_id_1=user_id_2, user_id_2=user_id_1, delete_mark=0) \
            .first()
        if chat:
            return chat
    return None
