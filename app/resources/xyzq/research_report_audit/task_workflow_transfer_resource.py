# coding=utf-8
import random

from .. import xyzq
from configs.base import *
from utils.response import RF
from flask import request
from flask.views import MethodView
from schemas.ideas_schema import TaskWorkflowTransferSchema
from utils.resource_utils.utils import InterfaceForwardServices
from models.research_report_task_model import research_report_task_model
from configs.static_variables import XYZQ_TaskWorkflowRequestStatus
from configs.static_variables import TyptResponseStatusEnum, TyptTaskStatusEnum
from financial_beans.enum.research_report_audit.research_report_audit_task_status import TaskWorkflowRequestStatus


class TaskWorkflowTransfer(MethodView):
    @xyzq.arguments(TaskWorkflowTransferSchema, as_kwargs=True, location="json")
    def post(self, task_id, forward_to_user_ids, flow_status, customized):
        # 自审请求-当前任务为审核通过且登录人与任务创建人相同

        if flow_status == TaskWorkflowRequestStatus.NEXT: # 开启新流程与审核通过
            # 开启新流程，判断是否是
            if research_report_task_model.query_creator_id(task_id) == research_report_task_model.query_now_login_id():
                if research_report_task_model.get_typt_task_status(task_id) in [TyptTaskStatusEnum.CALL_BACK, TyptTaskStatusEnum.IN_BOX]:
                    response_data = research_report_task_model.start_process(task_id, customized)
                    if response_data['status'] == TyptResponseStatusEnum.SUCCESS:
                        research_report_task_model.remove_call_back_status(task_id)  # 正常修改撤回状态为正常
                else:
                    response_data = research_report_task_model.next_process(task_id, customized) # 证明是退回任务，直接普通审核
            else: # 普通审核通过
                response_data = research_report_task_model.next_process(task_id, customized)
        elif flow_status == TaskWorkflowRequestStatus.BACK: # 撤回与退回
            # 撤回
            if research_report_task_model.query_creator_id(task_id) == research_report_task_model.query_now_login_id():
                response_data = research_report_task_model.back_process(task_id)
                if response_data['status'] == TyptResponseStatusEnum.SUCCESS:
                    research_report_task_model.set_call_back_status(task_id)
            else: # 退回
                response_data = research_report_task_model.next_process(task_id, customized)
        else:
            response_data = {}

        if response_data['status'] == TyptResponseStatusEnum.SUCCESS:
            InterfaceForwardServices().forward(API_HOST_IP + '/research_report_audit/task/workflow')
            # 动态添加可见用户
            research_report_task_model.add_forward_to_user_ids(task_id, forward_to_user_ids)
            # 修改审核人员获取任务时间
            research_report_task_model.add_task_assigned_time(task_id)

            # 增加接下来的任务处理人
            users_response_json = self.get_operator_info(task_id)
            operator_user_ids = []
            if users_response_json['status'] == 200:
                operator_user_ids = users_response_json.get('data', {}).get('operator_user_ids', [])
            response_data['operator_user_ids'] = operator_user_ids

            response_json = RF.success(data=response_data)
        else:
            response_json = RF.success(data=response_data)

        return response_json

    def get_operator_info(self, task_id):
        import requests
        url = API_HOST_IP + '/research_report_audit/task/one' + '?task_id={}'.format(task_id)
        payload = {}
        headers = {
            'Authorization': request.headers.environ.get('HTTP_AUTHORIZATION')
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()