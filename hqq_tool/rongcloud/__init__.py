#!/usr/bin/env python
# encoding: utf-8
'''
融云 Server API Python 客户端
create by kitName
create datetime : 2017-02-09 
  
v2.0.1 
'''
import os
from .user import User
from .message import Message
from .wordfilter import Wordfilter
from .group import Group
from .chatroom import Chatroom
from .push import Push
from .sms import SMS
from hqq_tool.hqq_tool import ACM


class RongCloud(object):
    def __new__(cls, app_key=None, app_secret=None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RongCloud, cls).__new__(cls)
            acm = ACM()
            if os.environ["DJANGO_SETTINGS_MODULE"] == 'DRF.settings.dev':
                key = acm.rongyun['dev']['APP_KEY']
                secret = acm.rongyun['dev']['APP_SECRET']
            elif os.environ["DJANGO_SETTINGS_MODULE"] == 'DRF.settings.test':
                key = acm.rongyun['dev']['APP_KEY']
                secret = acm.rongyun['dev']['APP_SECRET']
            elif os.environ["DJANGO_SETTINGS_MODULE"] == 'DRF.settings.production':
                key = acm.rongyun['production']['APP_KEY']
                secret = acm.rongyun['production']['APP_SECRET']
            else:
                raise Exception('【融云acm获取信息错误】')

            if app_key is None:
                app_key = key
            if app_secret is None:
                app_secret = secret
            cls.User = User(app_key, app_secret)
            cls.Message = Message(app_key, app_secret)
            cls.Wordfilter = Wordfilter(app_key, app_secret)
            cls.Group = Group(app_key, app_secret)
            cls.Chatroom = Chatroom(app_key, app_secret)
            cls.Push = Push(app_key, app_secret)
            cls.SMS = SMS(app_key, app_secret)

        return cls.instance
    #
    # def __init__(self, app_key=None, app_secret=None):
    #     acm = ACM()
    #     key = acm.rongyun['APP_KEY']
    #     secret = acm.rongyun['APP_SECRET']
    #     if app_key is None:
    #         app_key = key
    #     if app_secret is None:
    #         app_secret = secret
    #     self.User = User(app_key, app_secret)
    #     self.Message = Message(app_key, app_secret)
    #     self.Wordfilter = Wordfilter(app_key, app_secret)
    #     self.Group = Group(app_key, app_secret)
    #     self.Chatroom = Chatroom(app_key, app_secret)
    #     self.Push = Push(app_key, app_secret)
    #     self.SMS = SMS(app_key, app_secret)
