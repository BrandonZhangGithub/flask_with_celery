from initialization.sqlalchemy_process import session
from entities.research_report_audit_report_file_entity import ResearchReportAuditReportFileEntity


class ResearchReportTimeModel():
    _entity = ResearchReportAuditReportFileEntity

    def get_remark_date(self, file_id):
        research_report_file_item = session.query(self._entity).filter(self._entity.id == file_id).first()
        return research_report_file_item.remark

    def modify_remark_date(self, file_id, date):
        draft_file_item = session.query(self._entity).filter(self._entity.id == file_id).first()
        draft_file_item.remark = date
        session.commit()

    def delete_remark_date(self, file_id):
        draft_file_item = session.query(self._entity).filter(self._entity.id == file_id).first()
        draft_file_item.remark = ''
        session.commit()

research_report_time_model = ResearchReportTimeModel()