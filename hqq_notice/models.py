from django.db import models
from hqq_user.models import MyUser
from hqq_group.models import Group, ApplicationForGroup
from hqq_topic.models import Topic
from hqq_forum.models import Forum


class TextNotice(models.Model):
    """
    通知
    """
    id = models.CharField(max_length=32, verbose_name='主键', primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='接收者')
    title = models.CharField(max_length=50, verbose_name='通知内容')
    text = models.CharField(max_length=100, verbose_name='通知内容')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ApplyGroupNotice(models.Model):
    """
    加群通知
    """
    id = models.CharField(max_length=32, verbose_name='主键', primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='接收者')
    title = models.CharField(max_length=50, verbose_name='通知内容')
    text = models.CharField(max_length=100, verbose_name='通知内容')
    application = models.ForeignKey(ApplicationForGroup, on_delete=models.CASCADE, verbose_name='群信息')
    apply_state = models.SmallIntegerField(
        verbose_name='审核状态',
        choices=((0, '待审核'), (1, '同意'), (2, '拒绝')),
        default=0
    )
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class JumpGroupNotice(models.Model):
    """
    跳转到群的通知
    """
    id = models.CharField(max_length=32, verbose_name='主键', primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='接收者')
    title = models.CharField(max_length=50, verbose_name='通知内容')
    text = models.CharField(max_length=100, verbose_name='通知内容')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='群聊')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class JumpTopicNotice(models.Model):
    """
    跳转到全部话题界面的通知
    """
    id = models.CharField(max_length=32, verbose_name='主键', primary_key=True)
    title = models.CharField(max_length=50, verbose_name='通知内容')
    text = models.CharField(max_length=100, verbose_name='通知内容')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='群聊')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class TextNoticeToAll(models.Model):
    """
    全员通知
    """
    id = models.CharField(max_length=32, verbose_name='主键', primary_key=True)
    title = models.CharField(max_length=50, verbose_name='通知内容')
    text = models.CharField(max_length=100, verbose_name='通知内容')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )
