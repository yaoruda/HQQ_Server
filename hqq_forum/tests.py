from django.test import TestCase
import datetime
from hqq_forum.component import FacedForumComponent
from hqq_forum import models as forum_models
from hqq_topic import models as topic_models
from hqq_user import models as user_models


class ForumTestCase(TestCase):

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
            group_amount=1,
        )

        # 帖子
        forum_models.Forum.objects.create(
            id=1,
            user_id=1,
            topic_id=1,
        )
        forum_models.ForumStatistic.objects.create(
            id=1,
            forum_id=1,
        )

    def test_observer_like_a_forum_null_to_0(self):
        """
        点赞帖子：history无记录 to 不点赞
        """
        forum = FacedForumComponent()
        result = forum.Observer.forum_like({
            'user_id': '1',
            'forum_id': '1',
            'value': '0'
        })
        self.assertEqual(result, 200)

    def test_observer_like_a_forum_null_to_1(self):
        """
        点赞帖子：history无记录 to 点赞
        """
        forum = FacedForumComponent()
        result = forum.Observer.forum_like({
            'user_id': '1',
            'forum_id': '1',
            'value': '1'
        })
        self.assertEqual(result, 200)

    def test_observer_like_a_forum_0_to_1(self):
        """
        点赞帖子：history有记录 未点赞 to 点赞
        """
        forum_models.ForumHistory.objects.create(
            id=1,
            forum_id=1,
            user_id=1,
            value=0,
        )
        forum = FacedForumComponent()
        result = forum.Observer.forum_like({
            'user_id': '1',
            'forum_id': '1',
            'value': '1'
        })
        self.assertEqual(result, 200)

    def test_observer_like_a_forum_1_to_0(self):
        """
        点赞帖子：history有记录 点赞 to 未点赞
        """
        forum_models.ForumHistory.objects.create(
            id=1,
            forum_id=1,
            user_id=1,
            value=1,
        )
        forum_models.ForumStatistic.objects.filter(
            id=1,
        ).update(
            like=1,
        )
        forum = FacedForumComponent()
        result = forum.Observer.forum_like({
            'user_id': '1',
            'forum_id': '1',
            'value': '0'
        })
        self.assertEqual(result, 200)

    def test_observer_like_a_forum_0_to_0(self):
        """
        点赞帖子：history有记录 未点赞 to 未点赞
        """
        forum_models.ForumHistory.objects.create(
            id=1,
            forum_id=1,
            user_id=1,
            value=0,
        )
        forum = FacedForumComponent()
        result = forum.Observer.forum_like({
            'user_id': '1',
            'forum_id': '1',
            'value': '0'
        })
        self.assertEqual(result, 200)

    def test_observer_like_a_forum_1_to_1(self):
        """
        点赞帖子：history有记录 点赞 to 点赞
        """
        forum_models.ForumHistory.objects.create(
            id=1,
            forum_id=1,
            user_id=1,
            value=1,
        )
        forum_models.ForumStatistic.objects.filter(
            id=1,
        ).update(
            like=1,
        )
        forum = FacedForumComponent()
        result = forum.Observer.forum_like({
            'user_id': '1',
            'forum_id': '1',
            'value': '1'
        })
        self.assertEqual(result, 200)