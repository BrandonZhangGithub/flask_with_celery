# -*- coding: utf-8 -*-
from sqlalchemy import Index
from sqlalchemy.dialects.mysql import INTEGER

from initialization.sqlalchemy_process import db


class ResearchReportAuditTaskUserRelationEntity(db.Model):
    __tablename__ = 'research_report_audit_task_user_relation'
    __tablename_zh__ = '研报审核任务用户关系表'
    __table_desc__ = '研报审核任务用户关系表'

    __table_args__ = (
        Index('index_task_id_creator_id', 'research_report_audit_task_id', 'user_id'),
    )
    id = db.Column(INTEGER, primary_key=True, comment="id")
    research_report_audit_task_id = db.Column(INTEGER, comment="任务id")
    user_id = db.Column(INTEGER, comment="有权限用户id")
