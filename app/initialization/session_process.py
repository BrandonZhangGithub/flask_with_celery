#! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2019年2月14日

@author: ljbai
'''
from flask_session import Session

from configs import base, sysconf
from initialization.redis_process import redis_cli
from . import app

app.secret_key = base.SECRET_KEY
# app.permanent_session_lifetime = sysconf.SESSION_TIMEOUT  # 设置session超时时间

app.config['SESSION_TYPE'] = 'redis'  # session类型为redis
app.config['SESSION_PERMANENT'] = False  # 如果设置为True，则关闭浏览器session就失效。
app.config['SESSION_USE_SIGNER'] = True  # 是否对发送到浏览器上session的cookie值进行加密
# 保存到session中的值的前缀
# app.config['SESSION_KEY_PREFIX'] = sysconf.SESSION_KEY_PREFIX
app.config['SESSION_REDIS'] = redis_cli

Session(app)
