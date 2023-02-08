# coding=utf-8
from typing import List, Tuple

from sqlalchemy import func
import json
import time
import requests
from configs.base import *
from initialization.sqlalchemy_process import session
from entities.research_report_audit_draft_file_entity import ResearchReportAuditDraftFileEntity
from entities.research_report_audit_report_file_entity import ResearchReportAuditReportFileEntity

# noinspection DuplicatedCode
class ResearchReportAuditDraftFileModel():
    rradf = ResearchReportAuditDraftFileEntity
    rrarf = ResearchReportAuditReportFileEntity

    # 根据unique_name删除文件
    def delete_file_by_unique_name(self, task_id, to_delete_unique_name):
        q = session.query(self.rradf).filter(self.rradf.research_report_audit_task_id == task_id).filter(self.rradf.unique_name == to_delete_unique_name)
        item = q.first()
        item.status = 0
        session.commit()

    def query_report_file_id_by_task_id(self, task_id):
        q = session.query(self.rrarf).filter(self.rrarf.research_report_audit_task_id == task_id)
        items = q.all()
        items.sort(key=lambda x:x.version, reverse=True)
        return items[0].id

    def query_excel_name_by_draft_id(self, draft_id):
        q = session.query(self.rradf).filter(self.rradf.id == draft_id)
        return q.first().file_name

research_report_file_model = ResearchReportAuditDraftFileModel()