# coding=utf-8
import random

from .. import xyzq
from configs.base import *
from flask.views import MethodView
from utils.response import RF
from flask import send_from_directory
from schemas.ideas_schema import ExportResearchReportSchema
from utils.resource_utils.utils import InterfaceForwardServices
from models.research_report_task_model import research_report_task_model
from financial_beans.enum.research_report_audit.research_report_audit_task_status import TaskWorkflowRequestStatus

class ExportResearchReport(MethodView):
    @xyzq.arguments(ExportResearchReportSchema, as_kwargs=True, location="query")
    def get(self, task_id, file_name, original_file_path):
        save_url, file_name = research_report_task_model.get_export_filename(task_id)
        if save_url:
            return send_from_directory(save_url, file_name)
        else:
            return RF.failed(message='未查询到可下载研报！')