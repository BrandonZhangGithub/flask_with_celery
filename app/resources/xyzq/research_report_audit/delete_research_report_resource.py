# coding=utf-8
import time, datetime

from .. import xyzq
from configs.base import *
from utils.response import RF
from flask.views import MethodView
from utils.resource_utils.utils import ConnectTypt
from schemas.ideas_schema import DeleteResearchReportSchema
from models.research_report_task_model import research_report_task_model
from models.research_report_task_con_model import research_report_task_con_model
from models.research_report_file_model import research_report_file_model

class DeleteResearchReport(MethodView):
    @xyzq.arguments(DeleteResearchReportSchema, as_kwargs=True, location="query")
    def get(self, docId):
        if research_report_task_con_model.check_doc_id_exist(docId):
            task_id = research_report_task_con_model.get_task_id_by_doc_id(docId)
            research_report_task_model.delete_task_by_id(task_id)
            return RF.success(message='删除成功')
        else:
            return RF.success(data={}, message='未找到该任务', status=201)

    # 已废弃，本是为了删除具体的文件
    # extended = research_report_task_model.get_extended_by_task_id(task_id)
    # research_report_file_model.delete_file_by_unique_name(task_id, extended['file_id_uuid_dict'][file_id])
    # extended['file_id_uuid_dict'].pop(file_id)
    # research_report_task_model.update_extended_by_task_id(task_id,extended)