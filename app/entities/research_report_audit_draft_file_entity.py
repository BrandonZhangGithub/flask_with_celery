# coding=utf-8

from sqlalchemy import TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, VARCHAR

from initialization.sqlalchemy_process import db

class ResearchReportAuditDraftFileEntity(db.Model):
    """
    底稿审核文件
    """
    __tablename__ = 'research_report_audit_draft_file'
    __table_desc__ = '底稿审核文件'

    id = db.Column(INTEGER, primary_key=True, autoincrement=True)
    research_report_audit_task_id = db.Column(INTEGER, index=True, comment="任务ID")
    file_name = db.Column(VARCHAR(256), nullable=False, comment="文件名")
    unique_name = db.Column(VARCHAR(256), nullable=False, comment="文件uuid")
    is_ocr = db.Column(TINYINT, comment="是否已经ocr 0:未ocr,1:已ocr")
    status = db.Column(TINYINT, nullable=False, comment='状态：0.已删除')
    creator_id = db.Column(INTEGER, comment='创建者ID')
    create_time = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    last_update_time = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    failed_reason = db.Column(VARCHAR(256), comment="失败原因")
    file_type = db.Column(TINYINT, nullable=False, comment='文件类型:1研报2底稿', primary_key=True, autoincrement=False)
    version = db.Column(TINYINT, nullable=False, comment='版本')
    remark = db.Column(VARCHAR(1024), comment="备注")