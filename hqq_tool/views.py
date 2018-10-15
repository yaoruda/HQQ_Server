# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/10/11
import time as sys_time
import uuid as sys_uuid


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


def get_uuid():
    time = sys_time.time()
    nanosecond_time = int(time * 1e9)
    uuid_time = int(nanosecond_time/100) + 0x01b21dd213814000
    # 0x01b21dd213814000 is the number of 100-ns intervals between the
    # UUID epoch 1582-10-15 00:00:00 and the Unix epoch 1970-01-01 00:00:00.
    data1 = hex((uuid_time >> 28) & 0xffffffff)[2:10]
    data2 = hex(((uuid_time >> 12) & 0xffff) + 0x1000)[2:6]
    data3 = hex((uuid_time & 0xffff) + 0x1000)[2:6]

    data4 = str(sys_uuid.uuid1())[19:].replace('-', '')
    # 比如：'9c51-a45e60f013f3'

    uuid = '{}{}{}{}'.format(data1, data2, data3, data4)
    if uuid.__len__() != 32:
        print(uuid.__len__())

    return uuid
