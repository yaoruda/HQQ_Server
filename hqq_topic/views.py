# -*- coding: utf-8 -*-
# __author__= "suangsuang"
# Data: 2018/9/20

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from hqq_topic import models as topic_models
from hqq_topic import tasks as topic_tasks
from hqq_tool import views as hqq_tool


class AddFirstTopic(APIView):
    """
    #TODO:添加异步处理
        添加一级话题
        :param :
        :return
    """
    def post(self, request):
        return_info = {'code': 0}
        request_params_name = [
            'name',
        ]
        request_params = {}
        for params in request_params_name:
            request_params[params] = request.query_params.get(params)

        if hqq_tool.is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        id = hqq_tool.get_uuid()
        name = request.query_params.get("name")
        is_created = topic_models.FirstTopic.objects.filter(name=name).first()
        if is_created:
            return_info['code'] = 401
            return_info['info'] = '该名字的一级话题已被建立'
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        else:
            topic_tasks.add_new_first_topic.delay(id, name)
            return_info['code'] = 200
            return_info['info'] = '创建一级话题成功'
            # return_info['first_topic_id'] = new_first_topic.id
            return Response(return_info, status=status.HTTP_200_OK)


class AddSecondTopic(APIView):
    """
         #TODO:添加异步处理
        添加未审核的二级话题
        :param :
        :return
    """
    def post(self, request):
        return_info = {'code': 0}
        request_params_name = [
            'name',
            'first_topic_id',
        ]
        request_params = {}
        for params in request_params_name:
            request_params[params] = request.query_params.get(params)

        if hqq_tool.is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

        id = hqq_tool.get_uuid()
        second_topic_name = request.query_params.get("name")
        first_topic_id = request.query_params.get("first_topic_id")

        is_created = topic_models.SecondTopic.objects.filter(name=second_topic_name,first_topic_id=first_topic).first()
        is_existed = topic_models.FirstTopic.objects.filter(id=first_topic_id).first()
        if is_created:
            return_info['code'] = 401
            return_info['info'] = '该名字的二级话题已被建立'
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        elif is_existed:
            new_second_topic = topic_models.SecondTopic(id=id, name=second_topic_name, first_topic_id=first_topic)
            new_second_topic.save()
            return_info['code'] = 200
            return_info['info'] = '创建未审核的二级话题成功'
            return_info['new_second_topic_id'] = new_second_topic.id
            return Response(return_info, status=status.HTTP_200_OK)
        else:
            return_info['code'] = 402
            return_info['info'] = '没有对应的一级话题'
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)


class CloseFirstTopic(APIView):
    """

        :param :
        :return
    """
    def post(self, request):
        return_info = {'code': 0}
        request_params_name = [
            'first_topic_id',
        ]
        request_params = {}
        for params in request_params_name:
            request_params[params] = request.query_params.get(params)

        if hqq_tool.is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

        first_topic_id = request.query_params.get("first_topic_id")

        update_first_topic = topic_models.FirstTopic.objects.filter(id=first_topic_id).first()
        if update_first_topic:
            update_first_topic.state = 1
            update_first_topic.delete_mark = 1
            update_first_topic.save()
            return_info['code'] = 200
            return_info['info'] = '一级话题关闭成功'
            # return_info['first_topic_id'] = new_first_topic.id
            return Response(return_info, status=status.HTTP_200_OK)
        else:
            return_info['code'] = 401
            return_info['info'] = '没有要关闭的一级话题'
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)


class SelectAllFirstTopic(APIView):
    """
        #
        :param :
        :return
    """
    def get(self, request):
        return_info = {'code': 0}
        first_topics = topic_models.FirstTopic.objects.filter(state=0, delete_mark=0)
        json_list = []
        if first_topics:
            for first_topic in first_topics:
                json_dict = {}
                json_dict['id'] = first_topic.id
                json_dict['name'] = first_topic.name
                # json_dict['name'] =
                json_list.append(json_dict)
                return_info['code'] = 200
                return_info['info'] = '成功返回一级话题列表'
                return_info['first topic'] = json_list
            return Response(return_info, status=status.HTTP_200_OK)
        else:
            return_info['code'] = 401
            return_info['info'] = '没有找到一级话题'
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)


class SelectUncheckedSecondTopic(APIView):
    """
        #
        :param :
        :return
    """
    def get(self):
        return_info = {'code': 0}
        second_topics = topic_models.SecondTopic.objects.filter(state=2, delete_mark=0).all()
        json_list = []
        if second_topics:
            for second_topic in second_topics:
                # for params in request_params_name:
                json_dict = {}
                json_dict['id'] = second_topic.id
                json_dict['name'] = second_topic.name
                first_topic_name = get_first_topic_name(second_topic.first_topic_id)
                if first_topic_name:
                    json_dict['first_topic_name'] = first_topic_name
                    json_list.append(json_dict)
                    return_info['code'] = 200
                    return_info['info'] = '成功返回未审核的二级话题列表'
                    return_info['unchecked second topic'] = json_list
                    return Response(return_info, status=status.HTTP_200_OK)
                else:
                    return_info['code'] = 402
                    return_info['info'] = '没有对应的一级话题'
                    return Response(return_info, status=status.HTTP_400_BAD_REQUEST)
        else:
            return_info['code'] = 401
            return_info['info'] = '没有找到未审核的二级话题'
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

#
# class SelectAllTopic(APIView):
#     """
#         #
#         :param :
#         :return
#     """


@api_view(['get'])
def SelectAllTopic(request):
    return_info = {'code': 0}
    first_topics = topic_models.FirstTopic.objects.filter(state=0, delete_mark=0).all()
    if first_topics:
        for first_topic in first_topics:
            first_topic_name = get_first_topic_name(first_topic.id)
            second_topics = topic_models.SecondTopic.objects.filter(first_topic_id=first_topic.id, state=0,
                                                                    delete_mark=0).all()
            json_list = []
            if second_topics:
                return_info['info'] = '成功返回所有话题列表'
                for second_topic in second_topics:
                    json_dict = {}
                    json_dict['id'] = second_topic.id
                    json_dict['name'] = second_topic.name
                    json_list.append(json_dict)
            return_info[first_topic_name] = json_list
        return_info['code'] = 200

        return Response(return_info, status=status.HTTP_200_OK)

    else:
        return_info['code'] = 401
        return_info['info'] = '没有找到任何话题'
        return Response(return_info, status=status.HTTP_400_BAD_REQUEST)


class VerifySecondTopic(APIView):
    """
        #
        :param :
        :return
    """
    def post(self, request):
        return_info = {'code': 0}
        request_params_name = [
            'second_topic_id',
        ]
        request_params = {}
        for params in request_params_name:
            request_params[params] = request.query_params.get(params)

        if hqq_tool.is_request_empty(request_params, return_info):
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)

        second_topic_id = request.query_params.get("second_topic")

        update_second_topic = topic_models.SecondTopic.objects.filter(id=second_topic_id, state=2).first()
        if update_second_topic:
            update_second_topic.state = 0
            update_second_topic.save()
            return_info['code'] = 200
            return_info['info'] = '开启二级话题成功'
            return_info['second_topic_id'] = update_second_topic.id
            return Response(return_info, status=status.HTTP_200_OK)
        else:
            return_info['code'] = 401
            return_info['info'] = '没有找到对应的二级话题'
            return Response(return_info, status=status.HTTP_400_BAD_REQUEST)


def get_first_topic_name(first_topic_id):
    first_topic = topic_models.FirstTopic.objects.filter(id=first_topic_id, state=0, delete_mark=0).first()
    if first_topic:
        return first_topic.name
    else:
        return False
