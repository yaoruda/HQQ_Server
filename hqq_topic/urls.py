# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/20

from django.urls import path, include
from hqq_topic import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('get-all-topic', views.SelectAllTopic),

    path('first-topic/add', views.AddFirstTopic.as_view()),
    path('first-topic/delete', views.CloseFirstTopic.as_view()),
    path('first-topic', views.SelectAllFirstTopic.as_view()),

    path('second-topic/add', views.AddSecondTopic.as_view()),
    path('open-second-topic', views.VerifySecondTopic.as_view()),
    path('unchecked-second-topic', views.SelectUncheckedSecondTopic.as_view()),

]
