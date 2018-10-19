# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/20

from django.urls import path, include
from hqq_topic import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register('first-hqq_topic', views.FirstTopicViewSet, base_name='first-hqq_topic')
# router.register('first-topic', views.AddFirstTopic, base_name='create_first_topic')
# router.register('second-hqq_topic', views.SecondTopicViewSet, base_name='second-hqq_topic'),


urlpatterns = [
    path('first-topic/add', views.AddFirstTopic.as_view()),
    path('second-topic/add', views.AddSecondTopic.as_view()),
    path('first-topic/delete', views.CloseFirstTopic.as_view()),
    path('first-topic', views.SelectAllFirstTopic.as_view()),
    path('get-all-topic', views.SelectAllTopic.as_view()),
    path('open-second-topic', views.VerifySecondTopic.as_view()),
    path('unchecked-second-topic', views.SelectUncheckedSecondTopic.as_view()),



    path('', include(router.urls)),

]