# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/10/12

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hqq_tool import views as hqq_tool
from hqq_chat import models as chat_models


class Add(APIView):

    def post(self, request):
        '''
        发布单聊
        :param request:
        userID,(create_user_id)
        first_topic_id,
        second_topic_id,
        title & # prefer_list,
        # location & city,
        :return:
        '''
        return_info = {'code': 200}
        request_params_name = [
            'user_id',
            'first_topic_id',
            'second_topic_id',
            'title',
        ]
        request_params = {}
        for params in request_params_name:
            request_params[params] = request.query_params.get(params)
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

