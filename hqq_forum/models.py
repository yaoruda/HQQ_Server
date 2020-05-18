from django.db import models
from hqq_user.models import MyUser
from hqq_topic.models import Topic
from hqq_group.models import Group


class Forum(models.Model):
    """
    帖子
    """
    id = models.CharField(max_length=32, verbose_name='帖子主键', primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='创建者')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='话题外键')
    title = models.CharField(max_length=100, verbose_name='标题', default='')
    ban_mark = models.SmallIntegerField(
        verbose_name='封禁状态',
        choices=((0, '正常'), (1, '半封禁'), (2, '全封禁')),
        default=0
    )
    location_prefer = models.SmallIntegerField(
        verbose_name='距离偏好',
        choices=((0, '无所谓'), (1, '同城')),
        default=0
    )
    gender_prefer = models.SmallIntegerField(
        verbose_name='性别偏好',
        choices=((0, '无所谓'), (1, '男性可见'), (2, '女性可见')),
        default=0
    )
    age_prefer = models.SmallIntegerField(
        verbose_name='年龄偏好',
        choices=((0, '无所谓'), (1, '同龄人')),
        default=0
    )
    # v2
    # min_age_prefer = models.PositiveIntegerField(verbose_name='偏好最小年龄范围', default=0)
    # max_age_prefer = models.PositiveIntegerField(verbose_name='偏好最大年龄范围', default=100)

    chat_permission = models.SmallIntegerField(
        verbose_name='私聊许可',
        choices=((0, '不'), (1, '可')),
        default=0
    )
    reply_permission = models.SmallIntegerField(
        verbose_name='评论许可',
        choices=((0, '不'), (1, '可')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class Content(models.Model):
    """
    内容
    """
    id = models.CharField(max_length=32, verbose_name='帖子统计主键', primary_key=True)
    forum = models.OneToOneField(Forum, on_delete=models.CASCADE, verbose_name='帖子外键')
    text = models.TextField(verbose_name='帖子文本内容', default='')
    url = models.CharField(max_length=400, verbose_name='图片链接最多六张', default='')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ForumStatistic(models.Model):
    """
    统计（点赞、踩、评论、收藏、访问、热度等）
    """
    id = models.CharField(max_length=32, verbose_name='帖子统计主键', primary_key=True)
    forum = models.OneToOneField(Forum, on_delete=models.CASCADE, verbose_name='帖子外键')
    like = models.PositiveIntegerField(verbose_name='点赞数量', default=0)
    reply = models.PositiveIntegerField(verbose_name='一级回复数量', default=0)
    discussion = models.PositiveIntegerField(verbose_name='二级讨论数量', default=0)
    collection = models.PositiveIntegerField(verbose_name='收藏数量', default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ForumHistory(models.Model):
    """
    历史记录
    """
    id = models.CharField(max_length=32, verbose_name='帖子统计主键', primary_key=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, verbose_name='帖子外键')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    operation = models.SmallIntegerField(
        verbose_name='历史记录类型',
        choices=((0, '点赞'), (1, '')),
        default=0
    )
    value = models.SmallIntegerField(
        verbose_name='记录状态',
        choices=((0, '未操作'), (1, '已选中')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class Reply(models.Model):
    """
    一级回复
    """
    id = models.CharField(max_length=32, verbose_name='帖子统计主键', primary_key=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, verbose_name='帖子外键')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    text = models.TextField(verbose_name='一级回复文本', default='')
    ban_mark = models.SmallIntegerField(
        verbose_name='封禁状态',
        choices=((0, '正常'), (1, '半封禁'), (2, '全封禁')),
        default=0
    )
    like = models.PositiveIntegerField(verbose_name='点赞数量', default=0)
    discussion_amount = models.PositiveIntegerField(verbose_name='二级讨论数量', default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ReplyHistory(models.Model):
    """
    历史记录
    """
    id = models.CharField(max_length=32, verbose_name='帖子统计主键', primary_key=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, verbose_name='一级回复外键')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    operation = models.SmallIntegerField(
        verbose_name='历史记录类型',
        choices=((0, '点赞'), (1, '')),
        default=0
    )
    value = models.SmallIntegerField(
        verbose_name='记录状态',
        choices=((0, '未操作'), (1, '已选中')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class Discussion(models.Model):
    """
    二级回复
    """
    id = models.CharField(max_length=32, verbose_name='帖子统计主键', primary_key=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, verbose_name='一级回复外键')
    discuss_discussion = models.ForeignKey('self', null=True, on_delete=models.CASCADE, verbose_name='被二级回复回复的二级回复外键')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    text = models.TextField(verbose_name='一级回复文本', default='')
    ban_mark = models.SmallIntegerField(
        verbose_name='封禁状态',
        choices=((0, '正常'), (1, '半封禁'), (2, '全封禁')),
        default=0
    )
    type = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '向一级话题的回复'), (1, '二级话题之间的讨论')),
        default=0
    )
    like = models.PositiveIntegerField(verbose_name='点赞数量', default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class DiscussionHistory(models.Model):
    """
    历史记录
    """
    id = models.CharField(max_length=32, verbose_name='帖子统计主键', primary_key=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, verbose_name='二级回复外键')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    operation = models.SmallIntegerField(
        verbose_name='历史记录类型',
        choices=((0, '点赞'), (1, '')),
        default=0
    )
    value = models.SmallIntegerField(
        verbose_name='记录状态',
        choices=((0, '未操作'), (1, '已选中')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ForumCollection(models.Model):
    id = models.CharField(max_length=32, verbose_name='帖子收藏表主键', primary_key=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, verbose_name='帖子外键')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    value = models.SmallIntegerField(
        verbose_name='记录状态',
        choices=((0, '不收藏'), (1, '收藏')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ForumGroup(models.Model):
    id = models.CharField(max_length=32, verbose_name='帖子展示群聊表主键', primary_key=True)
    forum = models.OneToOneField(Forum, on_delete=models.CASCADE, verbose_name='帖子外键')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='群聊外键')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )
