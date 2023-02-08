# coding=utf-8
import json

from sqlalchemy import TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, VARCHAR, BIGINT


from initialization.sqlalchemy_process import db


class ResearchReportBasicInformationEntity(db.Model):
    """表格解析任务列表"""
    __tablename__ = 'research_report_basic_information'
    __table_desc__ = '研报审核基本信息'

    id: db.Column = db.Column(BIGINT, primary_key=True, autoincrement=False, comment="卡片ID")
    research_report_audit_report_file_id: db.Column = db.Column(INTEGER, comment='研报文件id', index=True)
    research_report_audit_task_id: db.Column = db.Column(INTEGER, comment='任务id', index=True)
    is_solve: db.Column = db.Column(TINYINT, comment='1 已解决,0未解决', default=0)
    result_type: db.Column = db.Column(TINYINT, comment='5字符错误,6基本信息,7敏感词', default=6)
    second_result_type: db.Column = db.Column(TINYINT, comment='1.股票信息2.分析师信息3.报告时间4.评级信息')
    is_comment: db.Column = db.Column(TINYINT, comment='1 有评论,0没有评论', default=0)
    audit_version: db.Column = db.Column(INTEGER, comment='审核结果版本')
    stock_code: db.Column = db.Column(VARCHAR(1024), comment='股票代码')
    stock_name: db.Column = db.Column(VARCHAR(1024), comment='股票名称')
    report_date: db.Column = db.Column(VARCHAR(1024), comment='报告日期')
    rating: db.Column = db.Column(VARCHAR(1024), comment='评级')
    rating_changes: db.Column = db.Column(VARCHAR(1024), comment='评级变动')
    role: db.Column = db.Column(VARCHAR(1024), comment='角色')
    name: db.Column = db.Column(VARCHAR(1024), comment='姓名')
    phone: db.Column = db.Column(VARCHAR(1024), comment='电话')
    email: db.Column = db.Column(VARCHAR(1024), comment='邮箱')
    cn_license: db.Column = db.Column(VARCHAR(1024), comment='国内执照信息')
    hk_license: db.Column = db.Column(VARCHAR(1024), comment='香港执照信息')
    create_time: db.Column = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    status: db.Column = db.Column(TINYINT, nullable=False, comment='状态：0.已删除', default=1)
    last_update_time: db.Column = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
