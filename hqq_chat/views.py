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

        :param request:
        userID,(create_user_id)
        first_topic_id,
        second_topic_id,
        title & # prefer_list,
        # location & city,
        :return:
        '''
        return_info = {'code': 200}
        request_params = {}
        request_params['user_id'] = request.query_params.get('user_id')
        request_params['first_topic_id'] = request.query_params.get('first_topic_id')
        request_params['second_topic_id'] = request.query_params.get('second_topic_id')
        request_params['title'] = request.query_params.get('title')
        if hqq_tool.is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        create_user_id = request_params.get('user_id')
        first_topic_id = request_params.get('first_topic_id')
        second_topic_id = request_params.get('second_topic_id')
        title = request_params.get('title')

        chat_id = hqq_tool.get_uuid()

        new_chat = chat_models.Chat(chat_id=chat_id, create_user_id=create_user_id, first_topic_id=first_topic_id,
                                    second_topic_id=second_topic_id, title=title, state=0, popularity=1200)
        new_chat.save()


