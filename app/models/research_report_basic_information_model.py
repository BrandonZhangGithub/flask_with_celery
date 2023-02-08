# coding=utf-8
from typing import List

from sqlalchemy import func

from entities.research_report_basic_information_entity import ResearchReportBasicInformationEntity
from initialization.sqlalchemy_process   import session
from financial_beans.enum.research_report_audit.research_report_audit_task_status import ResearchReportAuditTaskStatus


class ResearchReportBasicInformationModel():
    """基础信息数据库操作层"""
    _entity = ResearchReportBasicInformationEntity

    def query_result_by_file_id(self, file_id: int, is_count: bool = False):
        """
        根据文件id查询文件结果
        """
        q = session.query(self._entity).filter(self._entity.audit_version == session.query(func.max(self._entity.audit_version)).filter(
            self._entity.research_report_audit_report_file_id == file_id,
            self._entity.status != ResearchReportAuditTaskStatus.DELETE)). \
            filter(self._entity.research_report_audit_report_file_id == file_id,
                   self._entity.status != ResearchReportAuditTaskStatus.DELETE)
        if is_count:
            return q.count()
        return q.all()

    def query_recycle_by_file_id(self, file_id: int):
        q = session.query(self._entity.id.label("id"),
                          self._entity.research_report_audit_report_file_id.label('report_file_id'),
                          self._entity.research_report_audit_task_id.label('task_id'),
                          self._entity.audit_version.label('audit_version'),
                          self._entity.result_type.label('result_type'),
                          self._entity.is_solve.label('is_solve'),
                          self._entity.status.label('status')). \
            filter(self._entity.audit_version == session.query(func.max(self._entity.audit_version)).
                   filter(self._entity.research_report_audit_report_file_id == file_id, self._entity.status == ResearchReportAuditTaskStatus.DELETE)). \
            filter(self._entity.research_report_audit_report_file_id == file_id,
                   self._entity.status == ResearchReportAuditTaskStatus.DELETE)
        return q.all()

research_report_basic_information_model = ResearchReportBasicInformationModel()
