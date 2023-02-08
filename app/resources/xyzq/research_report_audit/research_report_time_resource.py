# coding=utf-8
from .. import xyzq
from configs.base import *
from utils.response import RF
from flask.views import MethodView
from schemas.ideas_schema import PostResearchReportTimeSchema, PutResearchReportTimeSchema, DeleteResearchReportTimeSchema
from models.research_report_time_model import research_report_time_model


class ResearchReportTime(MethodView):

    @xyzq.arguments(PostResearchReportTimeSchema, as_kwargs=True, location="json")
    def post(self, file_id, date):
        research_report_time_model.modify_remark_date(file_id, date)
        return RF.success(message='新增成功')

    @xyzq.arguments(PutResearchReportTimeSchema, as_kwargs=True, location="json")
    def put(self, file_id, date):
        research_report_time_model.modify_remark_date(file_id, date)
        return RF.success(message='修改成功')

    @xyzq.arguments(DeleteResearchReportTimeSchema, as_kwargs=True, location="json")
    def delete(self, file_id):
        research_report_time_model.delete_remark_date(file_id)
        return RF.success(message='删除成功')