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
        rongyun_return = rongyun_api.Group.create(create_user_id, chat_id, title)

        if rongyun_return.result['code'] == 200:
            return_info['code'] = 200
            return_info['description'] = '创建单聊成功'
            return_info['chat_id'] = chat_id
            return Response(return_info, status=status.HTTP_200_OK)
        else:
            chat = chat_models.Chat(id=chat_id)
            chat.delete_mark = 1
            chat.save()
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
            'user_id',
            'chat_id',
        ]
        request_params = {}
        for param in request_params_name:
            request_params[param] = request.query_params.get(param)
        if hqq_tool.is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        user_id = request_params.get(request_params_name[0])
        chat_id = request_params.get(request_params_name[1])

        if not chat_models.Chat.objects.filter(id=chat_id).first():
            # chat不存在
            return_info['code'] = 404
            return_info['description'] = '此聊天不存在'
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

        # 创建者进入：
        if chat_models.Chat.objects.filter(id=chat_id, create_user_id=user_id, state=0).first():
            # 创建者加入单聊(未满人)
            return_info['code'] = 201
            return_info['description'] = '创建者加入单聊(未满人)'
            return Response(return_info, status=status.HTTP_200_OK)

        elif chat_models.Chat.objects.filter(id=chat_id, create_user_id=user_id, state=1).first():
            # 创建者加入单聊(已满人)
            return_info['code'] = 202
            return_info['description'] = '创建者加入单聊(已满人)'
            return Response(return_info, status=status.HTTP_200_OK)

        # 参与者进入：
        elif chat_models.Chat.objects.filter(id=chat_id, join_user_id=user_id, state=1).first():
            # 参与者加入单聊
            return_info['code'] = 203
            return_info['description'] = '参与者加入单聊'
            return Response(return_info, status=status.HTTP_200_OK)

        # 首次加入：
        else:
            update_time = datetime.datetime.now()
            result = chat_models.Chat.objects\
                .filter(id=chat_id, state=0)\
                .update(state=1, join_user_id=user_id, update_time=update_time)
            if result == 1:
                # 加入操作在数据库操作成功
                rongyun_api = RongCloud()
                result = chat_models.Chat.objects.values('title').filter(id=chat_id).first()
                rongyun_return = rongyun_api.Group.join(user_id, chat_id, result['title'])
                if rongyun_return.result['code'] == 200:
                    # 加入操作在融云操作成功
                    return_info['code'] = 200
                    return_info['description'] = '加入单聊成功'
                    return Response(return_info, status=status.HTTP_200_OK)
                else:
                    update_time = datetime.datetime.now()
                    chat_models.Chat.objects \
                        .filter(id=chat_id, state=1) \
                        .update(state=0, join_user_id='', update_time=update_time)
                    return_info['code'] = 500
                    return_info['description'] = '聊天服务器异常，请稍后尝试'
                    return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

            else:
                # 加入操作在数据库操作时发现已经满人
                return_info['code'] = 402
                return_info['description'] = '此聊天已满人'
                return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

