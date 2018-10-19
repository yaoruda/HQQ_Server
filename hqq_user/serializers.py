# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/14

from rest_framework import serializers
from hqq_user import models


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
    user = serializers.ReadOnlyField(source='hqq_user.username')

    class Meta:
        model = models.Score
        fields = (
            'id',
            'hqq_user',
            'score',
        )


class TokenSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='hqq_user.username')

    class Meta:
        model = models.Token
        fields = (
            'id',
            'hqq_user',
            'token',
        )
