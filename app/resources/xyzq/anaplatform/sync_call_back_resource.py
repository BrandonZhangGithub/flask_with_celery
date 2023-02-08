import random
from flask.views import MethodView

import os
import requests
import json
from .. import xyzq
from configs.base import *
from utils.response import RF
from schemas.anaplatform_schema import CreateTaskSchema
from schemas.response_schema import BaseResponseSchema, ListResponseSchema
from utils.exceptions import TipResponse
from utils.response_container import BaseResponse, ListData, ListResponse
from utils.resource_utils.utils import InterfaceForwardServices, ConnectTypt, ConnectInner
from models.research_report_task_model import research_report_task_model
from models.research_report_task_con_model import research_report_task_con_model


class SyncCallBack(MethodView):
    @xyzq.arguments(CreateTaskSchema, as_kwargs=True, location="query")
    def get(self, employeeId, docId):
        task_id = research_report_task_con_model.get_task_id_by_doc_id(docId)
        response_json = self.request_call_back(task_id, employeeId)

        if response_json.get('status') == 200:
            research_report_task_model.set_call_back_status(task_id)
            return RF.success(message='撤回成功')
        else:
            return RF.failed(message='撤回失败', status=201)

    def request_call_back(self, task_id, employeeId):
        url = API_HOST_IP + FOR_CALL_BACK
        payload = json.dumps({
            "task_id": str(task_id),
            "flow_status": -1
        })
        headers = {
            'Authorization': 'Bearer {}'.format(ConnectInner(employeeId).request_user_token()),
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=73EB5CFBF30ACB3518071CDBA59D51AF'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()