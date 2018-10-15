# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/10/12

from django.urls import path
from hqq_chat import views

version_1 = 'v1/'
'''
2018年9月份开始的版本
初创版
亟待优化重构
'''

urlpatterns = [
    path(version_1 + 'add/', views.Add.as_view()),
]
