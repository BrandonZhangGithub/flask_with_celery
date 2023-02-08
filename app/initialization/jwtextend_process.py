#! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2020年02月07日

@author: jianzhihua
'''

from typing import Any

from flask import request
from flask_jwt_extended import JWTManager as _JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTExtendedException

from configs.base import JWT_SECRET_KEY
from configs.sysconf import JWT_ACCESS_TOKEN_EXPIRES
from . import app

app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES


class JWTManager(_JWTManager):

    def _set_error_handler_callbacks(self, app):
        """
        暂停注册错误, 由exception_process统一处理
        """
        ...


jwt = JWTManager(app)
