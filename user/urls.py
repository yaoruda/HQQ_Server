# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/14

from user import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('myuser', views.MyUserViewSet, base_name='user')
router.register('score', views.ScoreViewSet, base_name='score')
router.register('token', views.TokenViewSet, base_name='token')


urlpatterns = [
    path('getcode/', views.SendVerifyCode.as_view()),
    path('verifytoken/', views.VerifyToken.as_view()),
    path('registerandlogin/', views.RegisterAndLogin.as_view()),
    path('', include(router.urls)),
]

