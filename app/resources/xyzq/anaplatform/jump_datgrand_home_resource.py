import random
from flask.views import MethodView

import os
import requests
from .. import xyzq
from configs.base import *
from utils.response import RF
from schemas.anaplatform_schema import JumpDatagrandHomeSchema
from schemas.response_schema import BaseResponseSchema, ListResponseSchema
from utils.exceptions import TipResponse
from utils.response_container import BaseResponse, ListData, ListResponse
from utils.resource_utils.utils import InterfaceForwardServices, ConnectTypt, ConnectInner
from models.research_report_task_model import research_report_task_model
from models.research_report_task_con_model import research_report_task_con_model
import json


class JumpDatagrandHome(MethodView):
    @xyzq.arguments(JumpDatagrandHomeSchema, as_kwargs=True, location="query")
    def get(self, employeeId):
        access_token = ConnectInner(employeeId).request_user_token()
        return RF.success(data={'jump_url': CZT_IP_PORT + HOME_PAGE + '&access_token=' + access_token})
