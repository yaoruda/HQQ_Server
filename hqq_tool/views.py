# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/10/11
import time as sys_time
import uuid as sys_uuid
import acm
import json
from django.http import HttpResponse
from qiniu import Auth


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


def get_acm_data(data_name):
    ENDPOINT = "acm.aliyun.com:8080"
    NAMESPACE = "520a608f-cf8e-4769-99a4-aa09b4397088"
    AK = "LTAIbIchC6epwWTO"
    SK = "cpIAKyNPnbwACvuU303gKeqAUXVIFM"
    client = acm.ACMClient(ENDPOINT, NAMESPACE, AK, SK)
    group = "DEFAULT_GROUP"
    data_raw = client.get(data_name, group, timeout=30, no_snapshot=True)
    data_json = json.loads(data_raw)
    data_dict = {}
    for key in data_json:
        data_dict[key] = data_json[key]
    return data_dict


def get_token(key):
    # key 上传到七牛后保存的文件名

    access_key = 'ODiiBhlSmrpiua7rZ4l8cx8tuOjsAQ2mdtuYKtUV'
    secret_key = 'YaQbBkbWaXO7voNhP191JQhrr6XoKyLnruQL_da_'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'hqq-picture'

    # 上传策略示例
    # https://developer.qiniu.com/kodo/manual/1206/put-policy
    # 生成上传 Token，可以指定过期时间等
    policy = {
        # 'callbackUrl':'https://requestb.in/1c7q2d31',
        # 'callbackBody':'filename=$(fname)&filesize=$(fsize)'
        # 'persistentOps':'imageView2/1/w/200/h/200' 资源上传成功后触发执行的预转持久化处理指令列表。
        'fsizeLimit':'2048', # 限定上传文件大小最大值
        'mimeLimit':'image/*' #限定用户上传的文件类型 image/*表示只允许上传图片类型
    }
    # 3600为token过期时间，秒为单位。3600等于一小时
    token = q.upload_token(bucket_name, key, 3600, policy)
    return token