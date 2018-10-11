# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/10/11


def is_request_empty(request_params, return_info):
    '''
    检测request参数是否缺失
    :param request_params:
    :param return_info:
    :return:
    '''
    for param_name, param_value in request_params.items():
        if not param_value:  # 未获得此参数（None）
            message = '请求缺少字段:' + str(param_name)
            add_response(400, message, return_info)
            return True
    return False


def add_response(code, message, return_info):
    '''
    在return_info中修改code并添加信息
    :param code:
    :param message:
    :param return_info:
    :return:
    '''
    return_info['code'] = code
    return_info['message'] = message
    return return_info