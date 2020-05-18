# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Date: 2019/1/9
import datetime

from rest_framework.test import RequestsClient
from rest_framework.test import APITestCase
from hqq_group.tests import GroupTestCase
from .models import Blacklist


class BlacklistComponentTestCase(APITestCase):
    # server = 'http://192.168.1.131'
    server = 'http://www.huaquanquan.cn'
    appv1 = '/group/v1/'

    def setUp(self):
        Blacklist.objects.create(
            id=1,
            user_id=1,
            user_other_id=2,
        )

    def test_create_a_group(self):
        """
        create:200
        """
        method = 'add' + '?'
        params = {
            'user_id': 1,
            'topic_id': 1,
            'location': 1,
            'city_code': 1,
            'title': 1,
            'url': 1,
            'introduction': 1,
            'max_member': 1,
            'location_prefer': 1,
            'gender_prefer': 1,
            'age_prefer': 1,
            'question_amount': 1,
            'question': 1,
        }
        params_url = ''
        for k, v in params.items():
            params_url += '{}={}&'.format(k, v)

        response = self.client.get(self.server + self.appv1 + method + params_url)
        self.assertIs(response.status_code, 200)
        self.assertEqual(response.data['code'], 200)

    def test_get_settings_by_owner(self):
        """
        get_settings:200
        """
        response = self.client.get(self.server +
                                   '/group/v1/get_settings?'
                                   'group_id=1&'
                                   'user_id=1&'
                                   'type=1'
                                   )
        self.assertIs(response.status_code, 200)
        self.assertEqual(response.data['code'], 200)

    def test_active_exit_user_who_belongs_to_the_group(self):
        """
        active_exit:200
        """
        response = self.client.get(self.server +
                                   '/group/v1/active_exit?'
                                   'user_id=2&'
                                   'group_id=1'
                                   )
        self.assertEqual(response.data['code'], 200)
        self.assertIs(response.status_code, 200)

    def test_set_join_introduction_by_owner(self):
        """
        set_join_introduction:200
        """
        method = 'set_join_introduction' + '?'
        params = {
            'group_id': 1,
            'user_id': 1,
            'title': 'set',
            'introduction': 'set',
            'question_amount': 2,
            'question': '111,222',
        }
        params_url = ''
        for k, v in params.items():
            params_url += '{}={}&'.format(k, v)

        response = self.client.get(self.server + self.appv1 + method + params_url)
        self.assertIs(response.status_code, 200)
        self.assertEqual(response.data['code'], 200)

    def test_get_join_introduction_no_question(self):
        """
        get_join_introduction:201
        """
        method = 'get_join_introduction' + '?'
        params = {
            'group_id': 1,
        }
        params_url = ''
        for k, v in params.items():
            params_url += '{}={}&'.format(k, v)

        response = self.client.get(self.server + self.appv1 + method + params_url)
        self.assertIs(response.status_code, 200)
        self.assertEqual(response.data['code'], 201)
        self.assertEqual(response.data['description'], '无提问，可加入')

    def test_get_join_introduction_has_question(self):
        """
        get_join_introduction:200
        """
        group_models.Group.objects.filter(
            id=1,
        ).update(
            question_amount=1,
            question='q1',
        )
        method = 'get_join_introduction' + '?'
        params = {
            'group_id': 1,
        }
        params_url = ''
        for k, v in params.items():
            params_url += '{}={}&'.format(k, v)

        response = self.client.get(self.server + self.appv1 + method + params_url)
        self.assertIs(response.status_code, 200)
        self.assertEqual(response.data['code'], 200)
        self.assertEqual(response.data['description'], '需回答问题')

    def test_check_is_owner(self):
        """
        check:201
        """
        method = 'check' + '?'
        params = {
            'group_id': 1,
            'user_id': 1,
        }
        params_url = ''
        for k, v in params.items():
            params_url += '{}={}&'.format(k, v)

        response = self.client.get(self.server + self.appv1 + method + params_url)
        self.assertIs(response.status_code, 200)
        self.assertEqual(response.data['code'], 201)
        self.assertEqual(response.data['description'], '群主')

    def test_check_is_member(self):
        """
        check:200
        """
        method = 'check' + '?'
        params = {
            'group_id': 1,
            'user_id': 2,
        }
        params_url = ''
        for k, v in params.items():
            params_url += '{}={}&'.format(k, v)

        response = self.client.get(self.server + self.appv1 + method + params_url)
        self.assertIs(response.status_code, 200)
        self.assertEqual(response.data['code'], 200)
        self.assertEqual(response.data['description'], '群成员')

    def test_check_is_able_to_join(self):
        """
        check:202
        """
        method = 'check' + '?'
        params = {
            'group_id': 1,
            'user_id': 3,
        }
        params_url = ''
        for k, v in params.items():
            params_url += '{}={}&'.format(k, v)

        response = self.client.get(self.server + self.appv1 + method + params_url)
        self.assertIs(response.status_code, 200)
        self.assertEqual(response.data['code'], 202)
        self.assertEqual(response.data['description'], '可加入')
