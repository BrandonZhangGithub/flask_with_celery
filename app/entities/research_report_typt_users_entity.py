# coding=utf-8
from sqlalchemy import TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, VARCHAR, TEXT

from initialization.sqlalchemy_process import db


class ResearchReportTyptUsersEntity(db.Model):
    """表格解析任务与投研平台文档ID关系表"""
    __tablename__ = 'research_report_typt_users'
    __table_desc__ = '研报审核任务'

    def __init__(self, user_id, username, nickname, certificate, email, isdisable):
        self.user_id = user_id
        self.username = username
        self.nickname = nickname
        self.certificate = certificate
        self.email = email
        self.isdisable = isdisable

    # fields
    id = db.Column(INTEGER, primary_key=True, comment="默认ID")
    user_id = db.Column(INTEGER, nullable=False, comment="投研平台ID")
    username =  db.Column(VARCHAR(100), comment="工号-账户名")
    nickname = db.Column(VARCHAR(100), comment="姓名")
    certificate = db.Column(VARCHAR(100), comment="证书号")
    email = db.Column(VARCHAR(100), comment="邮箱")
    isdisable = db.Column(INTEGER, comment="是否生效")
