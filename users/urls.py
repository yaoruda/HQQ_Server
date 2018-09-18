# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/14

from rest_framework.authtoken import views as authtoken_views
from users import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('myuser', views.MyUserViewSet)
router.register('score', views.ScoreViewSet)
router.register('token', views.TokenViewSet)


urlpatterns = [
    path('getcode/', views.SendVerifyCode.as_view()),
    path('verifytoken/', views.VerifyToken.as_view()),
    path('', include(router.urls)),
]
