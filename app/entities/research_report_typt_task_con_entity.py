# coding=utf-8
from sqlalchemy import TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, VARCHAR, TEXT

from initialization.sqlalchemy_process import db


class ResearchReportTyptTaskConEntity(db.Model):
    """表格解析任务与投研平台文档ID关系表"""
    __tablename__ = 'research_report_typt_task_con'
    __table_desc__ = '研报审核任务'

    # fields
    id = db.Column(INTEGER, primary_key=True, comment="主键")
    task_id = db.Column(INTEGER, nullable=False, comment="任务id")
    doc_id = db.Column(INTEGER, nullable=False, comment="投研平台文档ID")
    create_time = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    last_update_time = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))