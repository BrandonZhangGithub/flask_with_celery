import random
from flask.views import MethodView

import os
import requests
import datetime
from .. import xyzq
from configs.base import *
from utils.response import RF
from schemas.anaplatform_schema import SyncCallBackSchema
from utils.resource_utils.utils import ConnectTypt, ConnectDgauth
import json
from utils.resource_utils.aes_encrypt import aes_encryption

from initialization.logger_process import logger
from initialization.sqlalchemy_process import session
from entities.research_report_typt_users_entity import ResearchReportTyptUsersEntity



class SyncUsersFirst(MethodView):
    @xyzq.arguments(SyncCallBackSchema, as_kwargs=True, location="query")
    def get(self, update_date, increase=False):
        sync_users = SyncUsers(update_date, increase, logger)
        sync_users.sync_research_report_typt_users()
        sync_users.sync_dg_oauth_users()

        return RF.success()


class SyncUsers():
    def __init__(self, update_date, increase, logger):
        self.update_date = update_date if update_date else self.get_default_update_date()  # 回溯时间
        self.increase = increase  # 增量/全量
        self.logger = logger
        self.users = self.get_users()


    def get_default_update_date(self):
        today = datetime.datetime.now()
        last_month = today - datetime.timedelta(days=UPDATE_DAYS)
        last_month_date = last_month.strftime("%Y-%m-%d %H:%M:%S")
        return last_month_date

    def sync_dg_oauth_users(self):
        for user in self.users:
            username, nickname, recStatus = user.get('employeeId'), user.get('employeeName'), int(user.get('isdisable'))
            if not username:
                continue
            status = 1 if recStatus == 0 else 0

            if self.increase:
                single_user = ConnectDgauth().get_user_by_username(username)
                if single_user:
                    ConnectDgauth().update_user(
                        [{
                            'expireTime': "2099-12-31",
                            'group_ids': [1],
                            'nickname': nickname,
                            'role_ids': [3],
                            'status': status,
                            'username': single_user['userName'],
                            'userId': single_user['userId']
                        }]
                    )
                    self.logger.info(
                        '增量更新Dgauth username:{} nickname:{}'.format(
                            username, nickname))
                else:
                    ConnectDgauth().create_user([{
                        'username': aes_encryption(str(username)),
                        'nickname': nickname,
                        'password': aes_encryption('2wsx!QAZ'),
                        'role_ids': [3],
                        'group_ids': [1],
                        'expireTime': '2099-12-31'
                    }])
                    self.logger.info(
                        '增量新增Dgauth username:{} nickname:{}'.format(
                            username, nickname))
            else:
                ConnectDgauth().create_user([{
                    'username': aes_encryption(str(username)),
                    'nickname': nickname,
                    'password': aes_encryption('2wsx!QAZ'),
                    'role_ids': [3],
                    'group_ids': [1],
                    'expireTime': '2099-12-31'
                }])
                self.logger.info(
                    '全量新增Dgauth username:{} nickname:{}'.format(
                        username, nickname))
                if status == 0:
                    single_user = ConnectDgauth().get_user_by_username(username)
                    ConnectDgauth().update_user(
                        [{
                            'expireTime': "2099-12-31",
                            'group_ids': [1],
                            'nickname': single_user['nickName'],
                            'role_ids': [3],
                            'status': 0,
                            'username': single_user['userName'],
                            'userId': single_user['userId']
                        }]
                    )
                    self.logger.info(
                        '全量新增，更新status状态 Dgauth username:{} nickname:{}'.format(
                            username, nickname))


    def sync_research_report_typt_users(self):
        if self.increase:
            users_list = []
            for user in self.users:
                user_id, username, nickname, certificate, email, isdisable = user.get('id'), user.get('employeeId'), \
                     user.get('employeeName'), user.get('certificate') if user.get('certificate') else '', \
                     user.get('email') if user.get('email') else '', int(user.get('isdisable', 0))
                if not username:
                    self.logger.info('增量更新ResearchReportTyptUsersEntity，username为空，略过: user_id:{}'.format(user_id))
                    continue
                pick_typt_user = session.query(ResearchReportTyptUsersEntity).filter(ResearchReportTyptUsersEntity.username == username).first()

                if pick_typt_user:
                    pick_typt_user.user_id = user_id
                    pick_typt_user.nickname = nickname
                    pick_typt_user.certificate = certificate
                    pick_typt_user.email = email
                    pick_typt_user.isdisable = isdisable
                    self.logger.info(
                        '增量更新ResearchReportTyptUsersEntity username:{} nickname:{}'.format(
                            username, nickname))
                    session.flush()
                else:
                    users_list.append(
                        ResearchReportTyptUsersEntity(user_id, username, nickname, certificate, email, isdisable))
            else:
                if users_list:
                    self.logger.info(
                        '增量新增ResearchReportTyptUsersEntity users:{}'.format(
                            [(user.username, user.nickname) for user in users_list]))
                    session.bulk_save_objects(users_list)
                session.commit()

        else:
            pick_typt_user = session.query(ResearchReportTyptUsersEntity).first()
            if pick_typt_user:
                self.logger.info('已有users， 全量新增ResearchReportTyptUsersEntity不可行')
                return

            users_list = []
            for user in self.users:
                user_id, username, nickname, certificate, email, isdisable = user.get('id'), user.get('employeeId'), \
                     user.get('employeeName'), user.get('certificate') if user.get('certificate') else '', \
                     user.get('email') if user.get('email') else '', int(user.get('isdisable', 0))
                if not username:
                    self.logger.info('全量新增ResearchReportTyptUsersEntity，username为空，略过: user_id:{}'.format(user_id))
                    continue
                users_list.append(
                    ResearchReportTyptUsersEntity(user_id, username, nickname, certificate, email, isdisable))
            if users_list:
                self.logger.info(
                    '全量新增ResearchReportTyptUsersEntity users:{}'.format([(user.username, user.nickname) for user in users_list]))
                session.bulk_save_objects(users_list)
            session.commit()

    def get_users(self):
        if self.increase:
            payload = json.dumps({
                "token": ConnectTypt(ADMIN_EMPLOYEE_ID).get_user_token(),
                "body": {
                    "pageNumber": 1,
                    "pageSize": 99999999,
                    "updateDate": self.update_date,
                }
            })
        else:
            payload = json.dumps({
                "token": ConnectTypt(ADMIN_EMPLOYEE_ID).get_user_token(),
                "body": {
                    "pageNumber": 1,
                    "pageSize": 99999999,
                }
            })

        url = TYPT_HOST_PORT + SYNC_USERS

        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=7087B2A6B4D302E66D95FBFB74836789'
        }
        self.logger.info('users request, url:{}; payload:{}'.format(url, json.dumps(payload, ensure_ascii=False)))
        response = requests.request("POST", url, headers=headers, data=payload)
        self.logger.info('users response, {}'.format(json.dumps(response.json())))
        users = response.json()['json']['userList']
        return users