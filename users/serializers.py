# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/14

from rest_framework import serializers
from users import models


class MyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MyUser
        fields = (
            'id',
            'phone',
            'nickname',
            'age',
            'gender',
        )


class ScoreSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = models.Score
        fields = (
            'id',
            'user',
            'score',
        )


class TokenSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = models.TokenLogin
        fields = (
            'id',
            'user',
            'token',
        )
