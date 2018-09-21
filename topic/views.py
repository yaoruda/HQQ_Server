# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/20

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from topic import models
from topic import serializers
from rest_framework.views import APIView
from DRF import auth


class FirstTopicListCreateView(generics.ListCreateAPIView):
    queryset = models.FirstTopic.objects.all()
    # authentication_classes = [auth.APIAuth, ]
    serializer_class = serializers.FirstTopicSerializer
    lookup_field = 'id'

class SecondTopicListCreateView(generics.ListCreateAPIView):
    queryset = models.SecondTopic.objects.all()
    # authentication_classes = [auth.APIAuth, ]
    serializer_class = serializers.SecondTopicSerializer
    lookup_field = 'id'

class SecondTopic(APIView):
    # authentication_classes = [auth.APIAuth, ]
    # def post(self, request):

    def get(self, request):
        '''
        列出某一个一级话题下的所有二级话题
        :param request:
        :return:
        '''
        first_topic_id = request.query_params.get('first-topic-id')
        name_list = models.SecondTopic.objects.filter(pk=first_topic_id)

        return Response(name_list, status=status.HTTP_200_OK)
