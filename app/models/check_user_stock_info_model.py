# coding=utf-8
from typing import List, Tuple

from sqlalchemy import func
import json
import time
import requests
from flask import request
import jwt
from configs.base import *
from initialization.sqlalchemy_process import session
from entities.research_report_typt_users_entity import ResearchReportTyptUsersEntity
from enum import Enum


class UserStatus(Enum):
    ENABLE = 0
    DISABLE = 1

class CheckUserStockInfoModel():
    _entity = ResearchReportTyptUsersEntity

    def query_by_email(self, email):
        q = session.query(self._entity).filter(self._entity.email == email).filter(self._entity.isdisable == UserStatus.ENABLE)
        return q.first()

    def query_by_cn_license(self, cn_license):
        q = session.query(self._entity).filter(self._entity.certificate == cn_license).filter(self._entity.isdisable == UserStatus.ENABLE)
        return q.first()

    def query_by_name(self, name):
        q = session.query(self._entity).filter(self._entity.username == name).filter(self._entity.isdisable == UserStatus.ENABLE)
        return q.first()

    def get_user_id_by_user_name(self, name):
        q = session.query(self._entity).filter(self._entity.username == int(name)).filter(self._entity.isdisable == UserStatus.ENABLE)
        return q.first().user_id

    def query_all_users(self, enabled=True):
        if enabled:
            q = session.query(self._entity).filter(self._entity.isdisable == UserStatus.ENABLE)
        else:
            q = session.query(self._entity)
        return q.all()

check_user_stock_info_model = CheckUserStockInfoModel()
