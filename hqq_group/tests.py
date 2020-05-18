# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Date: 2018/11/15
import datetime

from rest_framework.test import RequestsClient
from rest_framework.test import APITestCase
from hqq_user import models as user_models
from hqq_topic import models as topic_models
from hqq_group import models as group_models


class GroupTestCase(APITestCase):

    # server = 'http://192.168.1.131'
    server = 'http://www.huaquanquan.cn'
    appv1 = '/group/v1/'

    def setUp(self):
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
            group_amount=1,
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
            group_amount=1,
        )
        # 用户3
        user_models.MyUser.objects.create(
            id=3,
            phone='3',
            nickname='333',
            birth='1996-3-8',
            gender=1,
            state=0,
            login_time=datetime.datetime.now(),
        )
        user_models.UserStatistic.objects.create(
            id=3,
            user_id=3,
            group_amount=0,
        )
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
        group_models.Group.objects.create(
            id=1,
            number=1,
            popularity=1200,
            member_amount=2,
            state=0,

            create_user_id=1,
            topic_id=1,
            location='',
            city_code='',

            title=1,
            url=1,
            introduction='',
            max_member=5,
            location_prefer=0,
            gender_prefer=0,
            age_prefer=0,

            question_amount=0,
            question='',
        )
        group_models.GroupMember.objects.create(
            id=1,
            user_id=1,
            is_muted=0,
            group_id=1,
            state=1,
        )
        group_models.GroupMember.objects.create(
            id=2,
            user_id=2,
            is_muted=0,
            group_id=1,
            state=0,
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
