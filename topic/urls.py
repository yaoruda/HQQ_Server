# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/20

from django.urls import path, include
from topic import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register('firsttopic', views.CreateFirstTopic, base_name='create_first_topic')
# router.register('second-topic', views.SecondTopicViewSet, base_name='second-topic'),


urlpatterns = [
    path('first-topic/', views.FirstTopicListCreateView.as_view()),
    path('second-topic/', views.SecondTopicListCreateView.as_view()),
    path('second-topic/', views.SecondTopic.as_view()),
    path('', include(router.urls)),

]
