# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/10/19

from django.urls import path
from hqq_directchat import views

version_1 = 'v1/'
'''
2018年9月份开始的版本
初创版
亟待优化重构
'''

urlpatterns = [
    path(version_1 + 'add/', views.MakeDirectChat.as_view()),
    path(version_1 + 'exit/', views.ExitDirectChat.as_view()),

]
