# coding=utf-8
import random

from .. import xyzq
from configs.base import *
from flask.views import MethodView
from schemas.ideas_schema import SensitiveWordsSchema
from utils.resource_utils.utils import InterfaceForwardServices
from models.research_report_task_model import research_report_task_model
from utils.resource_utils.utils import InterfaceForwardServices, ConnectTypt
from financial_beans.enum.research_report_audit.research_report_audit_task_status import TaskWorkflowRequestStatus

class TaskOneTransfer(MethodView):
    @xyzq.arguments(SensitiveWordsSchema, as_kwargs=True, location="query")
    def get(self, task_id):
        response_json = InterfaceForwardServices().forward(API_HOST_IP+'/research_report_audit/task/one')
        if response_json['status'] == 200:
            task_one_info = research_report_task_model.get_task_info(task_id)
            response_json['data']['customized'] = task_one_info
        return response_json