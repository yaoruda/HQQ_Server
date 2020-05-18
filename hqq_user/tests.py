# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Date: 2018/11/14
import datetime
import time
from rest_framework.test import APITestCase
from hqq_topic import models as topic_models
from hqq_user import models as user_models
from hqq_usertopic import models as usertopic_models


class UserTestCase(APITestCase):

    # server = 'http://192.168.1.131'
    server = 'http://www.huaquanquan.cn'
    appv1 = '/user/v1/'

    def setUp(self):
        # 话题1
        topic_models.Category.objects.create(
            id=1,
            name='1',
        )
        topic_models.Topic.objects.create(
            id=1,
            name='1',
            category_id=1,
        )
        # 用户1
        user_models.MyUser.objects.create(
            id=1,
            phone='111',
            nickname='111',
            birth='1996-3-8',
            gender=1,
            state=0,
            login_time=datetime.datetime.now(),
        )
        user_models.UserStatistic.objects.create(
            id=1,
            user_id=1,
            group_amount=0,
        )
        user_models.Token.objects.create(
            id=1,
            user_id=1,
            token='1',
            rongyun_token='1',
        )
        usertopic_models.UserTopic.objects.create(
            id=1,
            topic_id=1,
            user_id=1,
            folder_id=0,
        )
        # 用户2
        user_models.MyUser.objects.create(
            id=2,
            phone='2',
            nickname='222',
            birth='1996-3-8',
            gender=1,
            state=0,
            login_time=datetime.datetime.now(),
        )
        user_models.UserStatistic.objects.create(
            id=2,
            user_id=2,
            group_amount=0,
        )
        portrait_models.UserPortrait.objects.create(
            id=2,
            url='2',
            user_id=2,
        )
        user_models.Token.objects.create(
            id=2,
            user_id=2,
            token='2',
            rongyun_token='2',
        )
        usertopic_models.UserTopic.objects.create(
            id=2,
            topic_id=1,
            user_id=2,
            folder_id=0,
        )

    def test_register_a_new_user(self):
        method = 'register' + '?'
        params = {
            'phone': 1,
            'nickname': 1,
            'birth': '1999年3月9日',
            'gender': 1,
            'portrait_id': 1,
            'topic': 1,
        }
        params_url = ''
        for k, v in params.items():
            params_url += '{}={}&'.format(k, v)
        response = self.client.get(self.server + self.appv1 + method + params_url)
        self.assertEqual(response.data['code'], 200)
        self.assertEqual(response.data['description'], 'ok')

    def test_verify_token_success(self):
        user_models.Token.objects.filter(
            user_id=1
        ).update(
            update_time=datetime.datetime.now()
        )
        method = 'verify_token' + '?'
        params = {
            'user_id': 1,
            'token': 1,
        }
        params_url = ''
        for k, v in params.items():
            params_url += '{}={}&'.format(k, v)
    
        response = self.client.get(self.server + self.appv1 + method + params_url)
        self.assertEqual(response.data['description'], 'ok')
        self.assertEqual(response.data['code'], 200)

    def test_verify_token_failed(self):
        set_time = time.time() - 2000
        set_time = datetime.datetime.fromtimestamp(set_time)
        user_models.Token.objects.filter(
            user_id=1
        ).update(
            update_time=set_time
        )
        method = 'verify_token' + '?'
        params = {
            'user_id': 1,
            'token': 1,
        }
        params_url = ''
        for k, v in params.items():
            params_url += '{}={}&'.format(k, v)

        response = self.client.get(self.server + self.appv1 + method + params_url)
        self.assertEqual(response.data['description'], 'Token已过期')
        self.assertEqual(response.data['code'], 200001)

