# coding=utf-8
from sqlalchemy import TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, VARCHAR, TEXT

from initialization.sqlalchemy_process import db


class ResearchReportAuditTaskEntity(db.Model):
    """表格解析任务列表"""
    __tablename__ = 'research_report_audit_task'
    __table_desc__ = '研报审核任务'

    # fields
    id = db.Column(INTEGER, primary_key=True, comment="任务ID")
    task_name = db.Column(VARCHAR(256), nullable=False, comment="任务名称")
    status = db.Column(TINYINT, nullable=False, comment='状态：0.已删除')
    creator_id = db.Column(INTEGER, comment='创建者ID')
    extended = db.Column(TEXT, comment='备用(存储额外的信息)')
    operator_status = db.Column(TINYINT, comment="人工审核状态 0表示正在处理 1表示处理完成")
    operator_user_id = db.Column(VARCHAR(256), comment="当前操作人ID字符串集合")
    create_time = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    last_update_time = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    remark = db.Column(VARCHAR(256), comment="备注")
