# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/10/12

import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hqq_tool import views as hqq_tool
from hqq_tool.rongcloud import RongCloud
from hqq_chat import models as chat_models
from hqq_chat import tasks as chat_tasks
from hqq_user import views as user_views


class Add(APIView):

    def post(self, request):
        '''
        发布单聊
        @:param request:
        @:param userID,(create_user_id)
        @:param first_topic_id,
        @:param second_topic_id,
        @:param title & # prefer_list,
        @:param # location & city,
        @:return:
        '''
        return_info = {'code': 0}
        request_params_name = [
            'user_id',
            'first_topic_id',
            'second_topic_id',
            'title',
        ]
        request_params = {}
        for param in request_params_name:
            request_params[param] = request.query_params.get(param)
        if hqq_tool.is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

        create_user_id = request_params.get(request_params_name[0])
        first_topic_id = request_params.get(request_params_name[1])
        second_topic_id = request_params.get(request_params_name[2])
        title = request_params.get(request_params_name[3])

        chat_id = hqq_tool.get_uuid()
        new_chat = chat_models.Chat(id=chat_id, create_user_id=create_user_id, first_topic_id=first_topic_id,
                                    second_topic_id=second_topic_id, title=title, state=0, popularity=1200)
        new_chat.save()

        rongyun_api = RongCloud()
        # 融云Group.create方法https://www.rongcloud.cn/docs/server.html#group_create
        rongyun_return = rongyun_api.Group.create(create_user_id, chat_id, title)

        if rongyun_return.result['code'] == 200:
            return_info['code'] = 200
            return_info['description'] = '创建单聊成功'
            return_info['chat_id'] = chat_id
            return Response(return_info, status=status.HTTP_200_OK)
        else:
            new_chat.delete_mark = 1
            new_chat.state = 4
            new_chat.save()
            return_info['code'] = 500
            return_info['description'] = '聊天服务器异常，请稍后尝试'
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)


class Join(APIView):

    def post(self, request):
        '''
        加入单聊
        '''
        return_info = {'code': 0}
        request_params_name = [
            'chat_id',
            'user_id',
        ]
        request_params = {}
        for param in request_params_name:
            request_params[param] = request.query_params.get(param)
        if hqq_tool.is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        chat_id = request_params.get(request_params_name[0])
        user_id = request_params.get(request_params_name[1])

        # 保证聊天和用户存在
        if not is_chat_exist(chat_id, return_info):
            # chat不存在
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        elif not user_views.is_user_exist(user_id, return_info):
            # user不存在
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        elif not is_chat_ok(chat_id, return_info):
            # chat除了0或1的状态，都返回
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

        chat = chat_models.Chat.objects.filter(id=chat_id).first()
        # 创建者进入：
        if chat.create_user_id == user_id and chat.state == 0:
            # 创建者加入单聊(未满人)
            return_info['code'] = 201
            return_info['description'] = '创建者加入单聊(未满人)'
            return Response(return_info, status=status.HTTP_200_OK)

        elif chat.create_user_id == user_id and chat.state == 1:
            # 创建者加入单聊(已满人)
            return_info['code'] = 202
            return_info['description'] = '创建者加入单聊(已满人)'
            return Response(return_info, status=status.HTTP_200_OK)

        # 参与者进入：
        elif chat.join_user_id == user_id and chat.state == 1:
            # 参与者加入单聊
            return_info['code'] = 203
            return_info['description'] = '参与者加入单聊'
            return Response(return_info, status=status.HTTP_200_OK)

        # 首次加入：
        else:
            update_time = datetime.datetime.now()
            add_chat = chat_models.Chat.objects\
                .filter(id=chat_id, state=0, delete_mark=0)\
                .update(state=1, join_user_id=user_id, update_time=update_time)
            if add_chat == 1:
                # 数据库成功
                rongyun_api = RongCloud()
                rongyun_return = rongyun_api.Group.join(user_id, chat_id, chat.title)
                if rongyun_return.result['code'] == 200:
                    # 融云成功
                    return_info['code'] = 200
                    return_info['description'] = '加入单聊成功'
                    return Response(return_info, status=status.HTTP_200_OK)
                else:
                    # 融云失败：回滚数据库操作
                    update_time = datetime.datetime.now()
                    chat_models.Chat.objects \
                        .filter(id=chat_id, state=1, delete_mark=0) \
                        .update(state=0, join_user_id='', update_time=update_time)
                    return_info['code'] = 500
                    return_info['description'] = '聊天服务器异常，请稍后尝试'
                    return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
            else:
                # 数据库操作时：发现单聊已经满人
                return_info['code'] = 401
                return_info['description'] = '此聊天已满人'
                return Response(return_info, status=status.HTTP_400_BAD_REQUEST)


class ExitChatUser(APIView):
    def post(self, request):
        '''
        用户退出单聊
        '''
        return_info = {'code': 0}
        request_params_name = [
            'chat_id',
            'user_id',
        ]
        request_params = {}
        for param in request_params_name:
            request_params[param] = request.query_params.get(param)
        if hqq_tool.is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        chat_id = request_params.get(request_params_name[0])
        user_id = request_params.get(request_params_name[1])

        if not is_chat_exist(chat_id, return_info):
            # chat不存在
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        elif not user_views.is_user_exist(user_id, return_info):
            # user不存在
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        elif is_chat_ok(chat_id, return_info):
            # chat被删除
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

        if chat_models.Chat.objects.filter(id=chat_id, join_user_id=user_id, state=1).first():
            # 参与者退出：异步
            chat_tasks.exit_join_user.delay(chat_id, user_id)
            return_info['code'] = 200
            return_info['description'] = '退出成功'
            return Response(return_info, status=status.HTTP_200_OK)
        elif chat_models.Chat.objects.filter(id=chat_id, create_user_id=user_id).first():
            # 创建者退出
            chat = chat_models.Chat.objects.values('join_user_id') \
                .filter(id=chat_id, state=1).first()
            if chat:
                # 存在参与者
                join_user_id = chat['join_user_id']
                chat_tasks.exit_create_user.delay(chat_id, user_id, join_user_id)
            else:
                # 不存在参与者
                chat_tasks.exit_create_user.delay(chat_id, user_id)
            return_info['code'] = 200
            return_info['description'] = '退出成功'
            return Response(return_info, status=status.HTTP_200_OK)
        else:
            return_info['code'] = 401
            return_info['description'] = '此用户不是此聊天的创建者'
            return Response(return_info, status=status.HTTP_200_OK)


def is_chat_exist(chat_id, return_info):
    if chat_models.Chat.objects.filter(id=chat_id).first():
        return True
    else:
        return_info['code'] = 404
        return_info['description'] = '此聊天不存在'
        return False


def is_chat_ok(chat_id, return_info):
    '''
    聊天是否状态正常
    :param chat_id:
    :param return_info:
    :return1: True:正常
    :return2: False:异常
    '''
    chat = chat_models.Chat.objects.values('state').filter(id=chat_id).first()
    if chat['state'] == 0 or chat['state'] == 1:
        # 可加入or已满人
        return True
    elif chat['state'] == 2:
        return_info['code'] = 402
        return_info['description'] = '此聊天已被删除'
        return False
    elif chat['state'] == 3:
        return_info['code'] = 403
        return_info['description'] = '此聊天已被封'
        return False
    else:
        return_info['code'] = 405
        return_info['description'] = '此聊天异常'
        return False
