# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/10/21
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hqq_tool import views as hqq_tool
from hqq_tool.rongcloud import RongCloud
from hqq_group import models as group_models
from hqq_user import views as user_views


class Add(APIView):

    def post(self, request):
        '''
        发布群聊
        @:param request:
        @:param userID,(create_user_id)
        @:param first_topic_id,
        @:param second_topic_id,
        @:param title &
        @:param description,
        @:param portrait_url,
        @:param question_state,
        @:param question,

        @:param# prefer_list,
        @:param # location & city,
        @:return:
        '''
        return_info = {'code': 0}
        request_params_name = [
            'user_id',
            'first_topic_id',
            'second_topic_id',
            'title',
            'description',
            'portrait_url',
            'question_state',
            'question',
            'max_member_number',
        ]
        request_params = {}
        for param in request_params_name:
            request_params[param] = request.query_params.get(param)
        if hqq_tool.is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

        create_user_id = request_params.get(request_params_name[0])
        first_topic_id = request_params.get(request_params_name[1])
        second_topic_id = request_params.get(request_params_name[2])
        title = request_params.get(request_params_name[3])
        description = request_params.get(request_params_name[4])
        portrait_url = request_params.get(request_params_name[5])
        question_state = request_params.get(request_params_name[6])
        question = request_params.get(request_params_name[7])
        max_member_number = request_params.get(request_params_name[8])

        group_id = hqq_tool.get_uuid()
        new_group = group_models.Group(id=group_id, create_user_id=create_user_id, first_topic_id=first_topic_id,
                                       second_topic_id=second_topic_id, title=title, state=0, popularity=1200,
                                       portrait_url=portrait_url, description=description, admin_user_id=create_user_id,
                                       question_state=question_state, question=question,
                                       member_number=1, max_member_number=max_member_number)
        new_group.save()
        group_member_id = hqq_tool.get_uuid()
        new_group_member = group_models.GroupMember(id=group_member_id, group_id=group_id, user_id=create_user_id,
                                                    state=0, answer='群主')
        new_group_member.save()

        rongyun_api = RongCloud()
        # 融云Group.create方法https://www.rongcloud.cn/docs/server.html#group_create
        rongyun_return = rongyun_api.Group.create(create_user_id, group_id, title)

        if rongyun_return.result['code'] == 200:
            return_info['code'] = 200
            return_info['description'] = '创建群聊成功'
            return_info['chat_id'] = group_id
            return Response(return_info, status=status.HTTP_200_OK)
        else:
            new_group.delete_mark = 1
            new_group.state = 4
            new_group.save()
            return_info['code'] = 500
            return_info['description'] = '聊天服务器异常，请稍后尝试'
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)


class Join(APIView):

    def post(self, request):
        '''
        加入群聊
        :param request:
        :return:
        '''
        return_info = {'code': 0}
        request_params_name = [
            'group_id',
            'user_id',
        ]
        request_params = {}
        for param in request_params_name:
            request_params[param] = request.query_params.get(param)
        if hqq_tool.is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

        group_id = request_params.get(request_params_name[0])
        user_id = request_params.get(request_params_name[1])

        # 群聊id不存在
        if not is_group_id_exist(group_id, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        elif not user_views.is_user_exist(user_id, return_info):
            # user不存在
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

        # 1: 可以直接进入
        # 群主:
        if group_models.Group.objects.filter(id=group_id, create_user_id=user_id).first():
            return_info['code'] = 201
            return_info['description'] = '群主进入群聊'
            return Response(return_info, status=status.HTTP_200_OK)
        # 已加入的群成员:
        group_member = group_models.GroupMember.objects\
            .values('state')\
            .filter(group_id=group_id, user_id=user_id)\
            .first()
        if group_member:
            if group_member['state'] == 0:
                # 0-正常
                return_info['code'] = 202
                return_info['description'] = '群成员进入群聊'
                return Response(return_info, status=status.HTTP_200_OK)

            # 2: 绝对不能进入
            elif group_member['state'] == 2:
                # 已被踢出
                return_info['code'] = 401
                return_info['description'] = '您已被踢出群聊'
                return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

        # 3: 加入此群聊
        group = group_models.Group.objects.filter(id=group_id).first()
        # 3.0: 是否满人
        if group.member_number == group.max_member_number:
            return_info['code'] = 402
            return_info['description'] = '群聊已满人'
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

        # 3.1: 有加群提问
        if group.question_state != 0:
            return_info['code'] = 203
            return_info['description'] = '需要回答进群审核问题'
            return_info['question'] = group.question
            return Response(return_info, status=status.HTTP_200_OK)

        # 3.2: 无加群提问
        if group.question_state == 0:
            update_time = datetime.datetime.now()
            add_member = group_models.Group.objects \
                .filter(id=group_id, state=0, member_number=group.max_member_number-1, delete_mark=0) \
                .update(state=1, member_number=group.max_member_number, update_time=update_time)
            if add_member != 1:
                add_member = group_models.Group.objects \
                    .filter(id=group_id, state=0, member_number=group.member_number, delete_mark=0) \
                    .update(member_number=group.member_number + 1, update_time=update_time)
                if add_member != 1:
                    return_info['code'] = 403
                    return_info['description'] = '访问群聊异常，请重新尝试'
                    return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

            new_member_id = hqq_tool.get_uuid()
            new_member = group_models.GroupMember(id=new_member_id, group_id=group_id, user_id=user_id,
                                                  state=0, answer='')
            new_member.save()

            rongyun_api = RongCloud()
            rongyun_return = rongyun_api.Group.join(user_id, group_id, group.title)
            if rongyun_return.result['code'] == 200:
                # 融云成功
                return_info['code'] = 200
                return_info['description'] = '加入群聊成功'
                return Response(return_info, status=status.HTTP_200_OK)
            else:
                # 融云失败：回滚数据库操作
                group.state = 0
                group.member_number = group.max_member_number - 1
                group.save()
                new_member.state = 3
                new_member.delete_mark = 1
                new_member.save()
                return_info['code'] = 500
                return_info['description'] = '聊天服务器异常，请稍后尝试'
                return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        #TODO:ERROR-log
        return_info['code'] = 500
        return_info['description'] = '服务器接口异常'
        return Response(return_info, status=status.HTTP_400_BAD_REQUEST)


class Exit(APIView):
    def post(self, request):
        '''
        用户退出群聊
        '''
        return_info = {'code': 0}
        request_params_name = [
            'group_id',
            'user_id',
        ]
        request_params = {}
        for param in request_params_name:
            request_params[param] = request.query_params.get(param)
        if hqq_tool.is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        group_id = request_params.get(request_params_name[0])
        user_id = request_params.get(request_params_name[1])

        if not is_group_id_exist(group_id, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        elif not user_views.is_user_exist(user_id, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        elif not is_group_ok(group_id, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

        # 1:成员退出
        group = group_models.Group.objects.filter(id=group_id).first()
        members = list_group_members(group_id)

        return_info['code'] = 200
        return_info['description'] = '200'
        return Response(return_info, status=status.HTTP_200_OK)


        # if group.create_user_id == user_id:

        # if chat_models.Chat.objects.filter(id=chat_id, join_user_id=user_id, state=1).first():
        #     # 参与者退出：异步
        #     chat_tasks.exit_join_user.delay(chat_id, user_id)
        #     return_info['code'] = 200
        #     return_info['description'] = '退出成功'
        #     return Response(return_info, status=status.HTTP_200_OK)
        # elif chat_models.Chat.objects.filter(id=chat_id, create_user_id=user_id).first():
        #     # 创建者退出
        #     chat = chat_models.Chat.objects.values('join_user_id') \
        #         .filter(id=chat_id, state=1).first()
        #     if chat:
        #         # 存在参与者
        #         join_user_id = chat['join_user_id']
        #         chat_tasks.exit_create_user.delay(chat_id, user_id, join_user_id)
        #     else:
        #         # 不存在参与者
        #         chat_tasks.exit_create_user.delay(chat_id, user_id)
        #     return_info['code'] = 200
        #     return_info['description'] = '退出成功'
        #     return Response(return_info, status=status.HTTP_200_OK)
        # else:
        #     return_info['code'] = 401
        #     return_info['description'] = '此用户不是此聊天的创建者'
        #     return Response(return_info, status=status.HTTP_200_OK)

def is_group_id_exist(group_id, return_info):
    '''
    群聊id是否存在
    :param group_id:
    :param return_info:
    :return1: True:存在
    :return2: False:不存在
    '''
    if group_models.Group.objects.filter(id=group_id).first():
        return True
    else:
        return_info['code'] = 404
        return_info['description'] = '此群聊不存在 '
        return False


def is_group_ok(group_id, return_info):
    '''
    群聊是否状态正常
    @:param group_id:
    @:param return_info:
    @:return: True:正常
    @:return: False:异常
    '''
    group = group_models.Group.objects.values('state').filter(id=group_id).first()
    if group['state'] == 0 or group['state'] == 1:
        # 可加入or已满人
        return True
    elif group['state'] == 2:
        return_info['code'] = 402
        return_info['description'] = '此群聊已解散'
        return False
    elif group['state'] == 3:
        return_info['code'] = 403
        return_info['description'] = '此群聊已被封'
        return False
    else:
        return_info['code'] = 405
        return_info['description'] = '此群聊异常'
        return False


def list_group_members(group_id):
    group_members = group_models.GroupMember.objects.filter(group_id=group_id, delete_mark=0).all()
    members = {
        'count': group_members.count(),
    }
    if group_members:
        for i in range(0, group_members.count()):
            print(group_members[i].id)
    return group_members

