# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/14
from hqq_user import views
from django.urls import path

version_1 = 'v1/'
'''
2018年9月份开始的版本
初创版
亟待优化重构
'''




urlpatterns = [
    path(version_1 + 'get-code/', views.SendVerifyCode.as_view()),
    path(version_1 + 'verify-token/', views.VerifyToken.as_view()),
    path(version_1 + 'register-and-login/', views.RegisterAndLogin.as_view()),
    path(version_1 + 'change-score/', views.ChangeScore.as_view()),
]

