# coding=utf-8
import time, datetime

from .. import xyzq
from configs.base import *
from utils.response import RF
from flask.views import MethodView
from utils.resource_utils.utils import ConnectTypt
from schemas.ideas_schema import RedirectTaskDetailSchema
from models.research_report_task_model import research_report_task_model
from models.research_report_task_con_model import research_report_task_con_model
from models.research_report_file_model import research_report_file_model
from utils.resource_utils.utils import InterfaceForwardServices, ConnectTypt, ConnectInner

class RedirectTaskDetailResource(MethodView):
    @xyzq.arguments(RedirectTaskDetailSchema, as_kwargs=True, location="query")
    def get(self, docId, employeeId):
        if research_report_task_con_model.check_doc_id_exist(docId):
            task_id = research_report_task_con_model.get_task_id_by_doc_id(docId)

            jump_url = CZT_IP_PORT + '/#/research-report/record/audit-detail/{}?page=1'.format(task_id)
            access_token = ConnectInner(employeeId).request_user_token()
        else:
            return RF.success(data={}, message='未找到该任务', status=201)

        return RF.success(data={'jump_url': jump_url + '&access_token=' + access_token})


        # extended = research_report_task_model.get_extended_by_task_id(task_id)
        # research_report_file_model.delete_file_by_unique_name(task_id, extended['file_id_uuid_dict'][file_id])
        # extended['file_id_uuid_dict'].pop(file_id)
        # research_report_task_model.update_extended_by_task_id(task_id,extended)