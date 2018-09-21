# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/9/20

from rest_framework import serializers
from topic import models


class FirstTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FirstTopic
        fields = (
            'id',
            'name',
        )


class SecondTopicSerializer(serializers.ModelSerializer):
    first_topic = serializers.ReadOnlyField(source='first_topic.name')

    class Meta:
        model = models.SecondTopic
        fields = (
            'id',
            'name',
            'first_topic',
        )
