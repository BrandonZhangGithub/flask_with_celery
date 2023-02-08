# coding=utf-8
import random

from .. import xyzq
from configs.base import *
from utils.response import RF
from flask.views import MethodView
from schemas.ideas_schema import SensitiveWordsSchema
from models.research_report_task_model import research_report_task_model

from utils.resource_utils.utils import InterfaceForwardServices, ConnectTypt

class TaskWorkflowInfo(MethodView):
    @xyzq.arguments(SensitiveWordsSchema, as_kwargs=True, location="query")
    def get(self, task_id):
        work_flow_info = research_report_task_model.get_work_flow_info(task_id)
        return RF.success(data=work_flow_info)