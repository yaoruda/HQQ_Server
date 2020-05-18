from django.db import models
from hqq_forum.models import Forum
from hqq_forum.models import Reply
from hqq_forum.models import Discussion
from hqq_group.models import Group
from hqq_user.models import MyUser
from hqq_dating.models import Dating


#####################################
# 帖子相关
#####################################
class BanForumHistory(models.Model):
    """
    帖子封禁记录
    """
    id = models.CharField(max_length=32, verbose_name='封禁帖子记录表主键', primary_key=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, verbose_name='帖子外键')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '待复核'), (1, '已复核'), (2, '已复原')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ReportForum(models.Model):
    """
    举报帖子
    """
    id = models.CharField(max_length=32, verbose_name='举报帖子主键', primary_key=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, verbose_name='帖子外键')
    reason_id = models.IntegerField(verbose_name='举报原因code')
    report_amount = models.IntegerField(verbose_name='此类别的举报数量', default=0)
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除'), (2, '')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ReportForumHistory(models.Model):
    """
    举报帖子记录
    """
    id = models.CharField(max_length=32, verbose_name='举报记录表主键', primary_key=True)
    report_forum = models.ForeignKey(ReportForum, on_delete=models.CASCADE, verbose_name='举报帖子外键')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    reason_id = models.IntegerField(verbose_name='举报原因code')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除'), (2, '')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


#####################################
# 一级回复相关
#####################################
class BanReplyHistory(models.Model):
    """
    一级回复封禁记录
    """
    id = models.CharField(max_length=32, verbose_name='封禁一级回复记录表主键', primary_key=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, verbose_name='一级回复外键')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '待复核'), (1, '已复核'), (2, '已复原')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ReportReply(models.Model):
    """
    举报一级回复
    """
    id = models.CharField(max_length=32, verbose_name='举报一级回复主键', primary_key=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, verbose_name='一级回复外键')
    reason_id = models.IntegerField(verbose_name='举报原因code')
    report_amount = models.IntegerField(verbose_name='此类别的举报数量', default=0)
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除'), (2, '')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ReportReplyHistory(models.Model):
    """
    举报一级回复记录
    """
    id = models.CharField(max_length=32, verbose_name='举报记录表主键', primary_key=True)
    report_reply = models.ForeignKey(ReportReply, on_delete=models.CASCADE, verbose_name='举报一级回复外键')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    reason_id = models.IntegerField(verbose_name='举报原因code')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除'), (2, '')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


#####################################
# 二级回复相关
#####################################
class BanDiscussionHistory(models.Model):
    """
    二级回复封禁记录
    """
    id = models.CharField(max_length=32, verbose_name='封禁二级回复记录表主键', primary_key=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, verbose_name='二级回复外键')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '待复核'), (1, '已复核'), (2, '已复原')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ReportDiscussion(models.Model):
    """
    举报二级回复
    """
    id = models.CharField(max_length=32, verbose_name='举报一级回复主键', primary_key=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, verbose_name='二级回复外键')
    reason_id = models.IntegerField(verbose_name='举报原因code')
    report_amount = models.IntegerField(verbose_name='此类别的举报数量', default=0)
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除'), (2, '')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ReportDiscussionHistory(models.Model):
    """
    举报二级回复记录
    """
    id = models.CharField(max_length=32, verbose_name='举报记录表主键', primary_key=True)
    report_discussion = models.ForeignKey(ReportDiscussion, on_delete=models.CASCADE, verbose_name='举报二级回复外键')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    reason_id = models.IntegerField(verbose_name='举报原因code')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除'), (2, '')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


#####################################
# 群聊相关
#####################################
class BanGroupHistory(models.Model):
    """
    群聊封禁记录
    """
    id = models.CharField(max_length=32, verbose_name='封禁群聊记录表主键', primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='群聊外键')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '待复核'), (1, '已复核'), (2, '已复原')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ReportGroup(models.Model):
    """
    举报群聊
    """
    id = models.CharField(max_length=32, verbose_name='举报群聊主键', primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='群聊外键')
    reason_id = models.IntegerField(verbose_name='举报原因code')
    report_amount = models.IntegerField(verbose_name='此类别的举报数量', default=0)
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除'), (2, '')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ReportGroupHistory(models.Model):
    """
    举报群聊记录
    """
    id = models.CharField(max_length=32, verbose_name='举报群聊记录表主键', primary_key=True)
    report_group = models.ForeignKey(ReportGroup, on_delete=models.CASCADE, verbose_name='举报群聊外键')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    reason_id = models.IntegerField(verbose_name='举报原因code')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除'), (2, '')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


#####################################
# 相亲角相关
#####################################
class BanDatingHistory(models.Model):
    """
    相亲角封禁记录
    """
    id = models.CharField(max_length=32, verbose_name='封禁相亲角记录表主键', primary_key=True)
    dating = models.ForeignKey(Dating, on_delete=models.CASCADE, verbose_name='相亲角外键')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '待复核'), (1, '已复核'), (2, '已复原')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ReportDating(models.Model):
    """
    举报相亲角
    """
    id = models.CharField(max_length=32, verbose_name='举报相亲角主键', primary_key=True)
    dating = models.ForeignKey(Dating, on_delete=models.CASCADE, verbose_name='相亲角外键')
    reason_id = models.IntegerField(verbose_name='举报原因code')
    report_amount = models.IntegerField(verbose_name='此类别的举报数量', default=0)
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除'), (2, '')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class ReportDatingHistory(models.Model):
    """
    举报相亲角记录
    """
    id = models.CharField(max_length=32, verbose_name='举报记录表主键', primary_key=True)
    report_dating = models.ForeignKey(ReportDating, on_delete=models.CASCADE, verbose_name='举报相亲角外键')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    reason_id = models.IntegerField(verbose_name='举报原因code')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除'), (2, '')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


#####################################
# 一级回复，用户评价
#####################################
class ChangeScoreByReplyHistory(models.Model):
    """
    生效评价记录(来自一级回复)
    """
    id = models.CharField(max_length=32, verbose_name='评价记录表主键', primary_key=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, verbose_name='一级回复外键')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '待复核'), (1, '已复核'), (2, '已复原')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class EvaluateReply(models.Model):
    """
    评价一级回复
    """
    id = models.CharField(max_length=32, verbose_name='评价一级回复主键', primary_key=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, verbose_name='一级回复外键')
    reason_id = models.IntegerField(verbose_name='评价原因code')
    evaluate_amount = models.IntegerField(verbose_name='此类别的评价数量', default=0)
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除'), (2, '')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class EvaluateReplyHistory(models.Model):
    """
    评价一级回复记录
    """
    id = models.CharField(max_length=32, verbose_name='评价记录表主键', primary_key=True)
    evaluate_reply = models.ForeignKey(EvaluateReply, on_delete=models.CASCADE, verbose_name='评价一级回复外键')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    reason_id = models.IntegerField(verbose_name='评价原因code')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除'), (2, '')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


#####################################
# 二级回复，用户评价
#####################################
class ChangeScoreByDiscussionHistory(models.Model):
    """
    生效评价记录(来自二级回复)
    """
    id = models.CharField(max_length=32, verbose_name='评价记录表主键', primary_key=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, verbose_name='二级回复外键')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '待复核'), (1, '已复核'), (2, '已复原')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class EvaluateDiscussion(models.Model):
    """
    评价二级回复
    """
    id = models.CharField(max_length=32, verbose_name='评价二级回复主键', primary_key=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, verbose_name='二级回复外键')
    reason_id = models.IntegerField(verbose_name='评价原因code')
    evaluate_amount = models.IntegerField(verbose_name='此类别的评价数量', default=0)
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除'), (2, '')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


class EvaluateDiscussionHistory(models.Model):
    """
    评价二级回复记录
    """
    id = models.CharField(max_length=32, verbose_name='评价记录表主键', primary_key=True)
    evaluate_discussion = models.ForeignKey(EvaluateDiscussion, on_delete=models.CASCADE, verbose_name='评价一级回复外键')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户外键')
    reason_id = models.IntegerField(verbose_name='评价原因code')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '删除'), (2, '')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


#####################################
# 群主踢人，用户评价
#####################################
class EvaluateGroupAdmin(models.Model):
    """
    群主踢人评价
    """
    id = models.CharField(max_length=32, verbose_name='群主踢人评价表主键', primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='群组外键')
    admin = models.ForeignKey(MyUser, related_name='evaluate_group_admin_RN_admin', on_delete=models.CASCADE, verbose_name='群主外键')
    reason_id = models.IntegerField(verbose_name='评价原因code')
    out_user = models.ForeignKey(MyUser, related_name='evaluate_group_admin_RN_out_user', on_delete=models.CASCADE, verbose_name='被踢者外键')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '已审核'), (2, '删除')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )


#####################################
# 私聊退出，用户评价
#####################################
class EvaluateDirectchat(models.Model):
    """
    私聊退出评价
    """
    id = models.CharField(max_length=32, verbose_name='私聊退出评价表主键', primary_key=True)
    user = models.ForeignKey(MyUser, related_name='evaluate_directchat_RN_user', on_delete=models.CASCADE, verbose_name='主动评价者外键')
    reason_id = models.IntegerField(verbose_name='评价原因code')
    other_user = models.ForeignKey(MyUser, related_name='evaluate_directchat_RN_other_user', on_delete=models.CASCADE, verbose_name='被评价者外键')
    state = models.SmallIntegerField(
        verbose_name='状态',
        choices=((0, '正常'), (1, '已审核'), (2, '删除')),
        default=0
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_mark = models.SmallIntegerField(
        verbose_name='删除标记',
        choices=((0, '正常'), (1, '删除')),
        default=0
    )
