# coding=utf-8
from .. import xyzq
from configs.base import *
from utils.response import RF
from flask.views import MethodView
from utils.resource_utils.utils import ConnectTypt
from schemas.ideas_schema import SensitiveWordsSchema
from utils.resource_utils.utils import InterfaceForwardServices
from models.research_report_task_model import research_report_task_model
from models.research_report_file_model import research_report_file_model

class TaskDetailTransfer(MethodView):
    @xyzq.arguments(SensitiveWordsSchema, as_kwargs=True, location="query")
    def get(self, task_id):
        response_json = InterfaceForwardServices().forward(API_HOST_IP+'/research_report_audit/task/detail')
        if response_json['status'] == 200:
            # 设置task_assigned_time与jump_url
            task_ids = [task_id]
            task_id_assigned_time_dict = research_report_task_model.get_task_assigned_time(task_ids)
            operator_status = research_report_task_model.query_operator_user_id(task_ids)
            response_json['data']['task_info']['task_assigned_time'] = task_id_assigned_time_dict[task_id]
            response_json['data']['task_info']['jump_url'] = TYPT_DOMAIN_NAME + TYPT_HOST_PAGE
            response_json['data']['task_info']['operator_status'] = operator_status

            file_list = response_json.get('data', {}).get('file_list', [])
            latest_file_id = research_report_file_model.query_report_file_id_by_task_id(task_id)
            for file in file_list:
                if file['file_type'] == 1:
                    # 设置下载文件名
                    file_name = file['file_name']
                    download_file_name = file_name.split('.')[0] + '.pdf'
                    file['download_file_name'] = download_file_name
                    # 设置最新的研报与历史研报的区分字段
                    if int(file['file_id']) == latest_file_id:
                        file['is_latest'] = True
                    else:
                        file['is_latest'] = False
        return response_json