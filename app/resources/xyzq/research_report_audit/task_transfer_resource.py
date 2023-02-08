# coding=utf-8
from configs.base import *
from utils.response import RF
from flask.views import MethodView
from utils.resource_utils.utils import InterfaceForwardServices
from models.research_report_task_model import research_report_task_model


class TaskTransfer(MethodView):
    def get(self):
        response_json = InterfaceForwardServices().forward(API_HOST_IP+'/research_report_audit/task')
        if response_json['status'] == 200:
            task_ids = [int(item['task_id']) for item in response_json['data']['items']]
            task_id_assigned_time_dict = research_report_task_model.get_task_assigned_time(task_ids)
            for item in response_json['data']['items']:
                item['task_assigned_time'] = task_id_assigned_time_dict[int(item['task_id'])]
        return response_json