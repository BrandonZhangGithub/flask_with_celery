import random
from flask.views import MethodView

import json
import requests
from .. import xyzq
from configs.base import *
from utils.response import RF
from utils.resource_utils.utils import ConnectInner, ConnectDgauth
from schemas.phone_schema import PhoneNormalApproveSchema, PhoneFinalApproveSchema, PhoneRejectSchema
from configs.static_variables import TyptResponseStatusEnum, TyptTaskStatusEnum
from schemas.response_schema import BaseResponseSchema, ListResponseSchema
from utils.exceptions import TipResponse
from models.research_report_task_model import research_report_task_model
from utils.response_container import BaseResponse, ListData, ListResponse
from configs.static_variables import XYZQTaskWorkflowRequestStatus
from models.research_report_task_con_model import research_report_task_con_model
from initialization.logger_process import logger


class PhoneNormalApprove(MethodView):
    @xyzq.arguments(PhoneNormalApproveSchema, as_kwargs=True, location="json")
    def post(self, docId, employeeId, forwardIds):
        task_id = research_report_task_con_model.get_task_id_by_doc_id(docId)
        forward_to_user_ids = [ConnectDgauth().get_user_by_username(forwardId).get('userId') for forwardId in forwardIds]

        response = self.post_request(employeeId, task_id, forward_to_user_ids)
        if response.json().get('status') == 200:
            research_report_task_model.add_forward_to_user_ids(task_id, forward_to_user_ids) # 设置任务可见权限
        return RF.success()

    def post_request(self, employeeId, task_id, forward_to_user_ids):
        url = API_HOST_IP + '/research_report_audit/task/workflow'

        payload = json.dumps({
            "task_id": task_id,
            "forward_to_user_ids": forward_to_user_ids,
            "flow_status": 0
        })
        headers = {
            'Authorization': 'Bearer {}'.format(ConnectInner(employeeId).get_user_token()),
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=972B88090FE4A75D4086DE17608DAA15'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('手机APP平台，审批通过请求 employeeId：{}，task_id：{}，forward_to_user_ids：{}'.format(
            employeeId, task_id, json.dumps(forward_to_user_ids, ensure_ascii=False)))
        logger.info('审批通过请求response:{}'.format(json.dumps(response.json(), ensure_ascii=False)))
        return response

class PhoneFinalApprove(MethodView):
    @xyzq.arguments(PhoneFinalApproveSchema, as_kwargs=True, location="json")
    def post(self, docId, employeeId):
        task_id = research_report_task_con_model.get_task_id_by_doc_id(docId)
        response = self.post_request(employeeId, task_id)
        return RF.success()


    def post_request(self, employeeId, task_id):
        url = API_HOST_IP + '/research_report_audit/task/workflow'

        payload = json.dumps({
            "task_id": task_id,
            "flow_status": 1
        })
        headers = {
            'Authorization': 'Bearer {}'.format(ConnectInner(employeeId).get_user_token()),
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=972B88090FE4A75D4086DE17608DAA15'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('手机APP平台，任务通过请求 employeeId：{}，task_id：{}'.format(
            employeeId, task_id))
        logger.info('任务通过请求response:{}'.format(json.dumps(response.json(), ensure_ascii=False)))
        return response

class PhoneReject(MethodView):
    @xyzq.arguments(PhoneRejectSchema, as_kwargs=True, location="json")
    def post(self, docId, employeeId):
        task_id = research_report_task_con_model.get_task_id_by_doc_id(docId)
        response = self.post_request(employeeId, task_id)
        return RF.success()

    def post_request(self, employeeId, task_id):
        url = API_HOST_IP + '/research_report_audit/task/workflow'

        payload = json.dumps({
            "task_id": task_id,
            "flow_status": -1
        })
        headers = {
            'Authorization': 'Bearer {}'.format(ConnectInner(employeeId).get_user_token()),
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=972B88090FE4A75D4086DE17608DAA15'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('手机APP平台，退回请求 employeeId：{}，task_id：{}'.format(
            employeeId, task_id))
        logger.info('退回请求response:{}'.format(json.dumps(response.json(), ensure_ascii=False)))
        return response