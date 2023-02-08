import random
from flask.views import MethodView

import os
import re
import requests
from .. import xyzq
from configs.base import *
from utils.response import RF
from schemas.anaplatform_schema import CreateTaskSchema
from utils.resource_utils.utils import InterfaceForwardServices, ConnectTypt, ConnectInner
from models.research_report_task_model import research_report_task_model
from models.research_report_task_con_model import research_report_task_con_model
from initialization.logger_process import logger
from celery_tasks.task.flask_check_tasks import check_sensitive_words_task, check_separation_wall_task
import json


class CreateTask(MethodView):
    @xyzq.arguments(CreateTaskSchema, as_kwargs=True, location="query")
    def get(self, employeeId, docId):
        self.employeeId = employeeId
        self.doc_id = docId
        task_detail = ConnectTypt(employeeId).get_task_detail(docId)
        logger.info('创建/更新任务，task_detail：{}'.format(json.dumps(task_detail, ensure_ascii=False)))
        file_name = task_detail.get('title', '')
        now_draft_files = task_detail.get('workingSheet', [])
        now_research_report_files = task_detail.get('attachment', [])


        if research_report_task_con_model.check_doc_id_exist(docId): # 已存在历史任务，为撤回操作，更新文件与状态
            task_id = research_report_task_con_model.get_task_id_by_doc_id(docId)
            jump_url, access_token = self.update_old_task(task_id, now_draft_files, now_research_report_files, file_name, docId)
        else: # 新建任务
            jump_url, access_token = self.create_new_task(now_draft_files, now_research_report_files, file_name, docId)

        return RF.success(data={'jump_url': jump_url + '&access_token=' + access_token})

    def update_old_task(self, task_id, now_draft_files, now_research_report_files, file_name, docId):
        # 更新任务名称
        self.update_task_name(task_id, file_name)

        extended = research_report_task_model.get_extended_by_task_id(task_id)
        ori_draft_file_ids = extended['draft_file_ids']
        ori_research_report_file_ids = extended['research_report_file_ids']

        params = {}
        params['task_id'] = str(task_id)
        params['draft_files'], draft_file_ids, file_id_uuid_dict = self.save_typt_files(now_draft_files, file_ids=ori_draft_file_ids,
                                                                     type='draft_file', update=True)
        params['research_report_files'], research_report_file_ids, _ = self.save_typt_files(now_research_report_files,
                                                                     file_ids=ori_research_report_file_ids, type='research_report', update=True)
        # 只有研报文件新增, 清空敏感词与隔离墙检测结果, 敏感词检测、隔离墙检测
        if params['research_report_files']:
            research_report_task_model.clear_sensitive_and_separation(task_id)
            check_sensitive_words_task.delay(task_id)
            check_separation_wall_task.delay(task_id)

        # 判断有新增的文件ID
        if params['draft_files'] or params['research_report_files']:
            self.update_task(params) # 新增文件
            # 保存本次更新信息，删除不匹配文件
            research_report_task_model.save_task_create_info(task_id, docId, draft_file_ids, research_report_file_ids, file_id_uuid_dict, update=True) # 删除不存在的底稿
        # 判断是只对底稿做了删除
        elif len(ori_draft_file_ids) > len(now_draft_files):
            research_report_task_model.solve_only_delete(task_id, docId, draft_file_ids, ori_draft_file_ids)

        research_report_task_model.remove_call_back_status(task_id)
        jump_url = CZT_IP_PORT + '/#/research-report/record/audit-detail/{}?page=1'.format(task_id)
        access_token = ConnectInner(self.employeeId).request_user_token()
        return jump_url, access_token

    def update_task_name(self, task_id, file_name):
        user_ids = ConnectInner(self.employeeId).get_edit_user_ids(task_id)
        # if not user_ids:
        #     raise
        ConnectInner(self.employeeId).post_edit_task_name(task_id, file_name, user_ids)



    def create_new_task(self, now_draft_files, now_research_report_files, file_name, docId):
        draft_files, draft_file_ids, file_id_uuid_dict = self.save_typt_files(now_draft_files, type='draft_file', update=False)
        research_report_files, research_report_file_ids, _  = self.save_typt_files(now_research_report_files, type='research_report', update=False)

        params = {}
        params['draft_files'] = draft_files
        params['research_report_files'] = research_report_files
        params['task_name'] = file_name
        params['report_type'] = "1"

        task_id = self.create_task(params)
        research_report_task_model.add_task_assigned_time(task_id)
        research_report_task_model.save_task_create_info(task_id, docId, draft_file_ids, research_report_file_ids, file_id_uuid_dict, update=False)
        check_sensitive_words_task.delay(task_id)
        check_separation_wall_task.delay(task_id)
        jump_url = CZT_IP_PORT + '/#/research-report/record/audit-detail/{}?page=1'.format(task_id)
        access_token = ConnectInner(self.employeeId).request_user_token()
        return jump_url, access_token

    def save_typt_files(self, files, file_ids=None, type='research_report',update=False):
        # 如果创建新文件，那么file_ids_result与file_id_uuid_list都是最新的
        # 如果更新文件，那么file_ids_result是包含交集与新加入的id， file_id_uuid_list只有新加入的id
        # 目前file_id_uuid_list只保存底稿文件

        files_result = []
        file_ids_result = []
        file_id_uuid_dict = {} # 底稿文件id与本系统uuid
        if type == 'research_report': # 研报
            file_type_list = [single_research_report_file['fileName'].split('.')[-1] for single_research_report_file in files]
            if 'docx' in file_type_list or 'doc' in file_type_list:
                HAS_DOC = True
            else:
                HAS_DOC = False

            for research_report_file in files:
                file_id = research_report_file['id']
                if update and file_id in file_ids: # 过滤已有id
                    file_ids_result.append(file_id)
                    continue
                file_name = research_report_file['fileName']
                if file_name.split('.')[-1] not in  ['pdf', 'docx', 'doc']: # 只取这三种
                    continue
                file_url = research_report_file['url']
                if HAS_DOC and file_name.split('.')[-1] not in ['docx', 'doc']:  # 有word取word，否则研报只要pdf
                    continue
                save_url =  os.path.join(STATIC_DIR, str(self.doc_id), 'research_report')
                self.download_typt_file(save_url, file_url, file_name)
                files_result.append(self.web_api_upload_file(save_url, file_name))
                file_ids_result.append(file_id)
                break
        else: #　type == 'draft_file' 底稿
            for draft_file in files:
                file_id = draft_file['workingSheetId']
                if update and file_id in file_ids:
                    file_ids_result.append(file_id) # 保存当前底稿全部文件
                    continue
                file_name = draft_file['workingSheetName']
                file_url = draft_file['workingSheetPath']
                save_url =  os.path.join(STATIC_DIR, str(self.doc_id), 'draft_file')
                self.download_typt_file(save_url, file_url, file_name)
                upload_file_result = self.web_api_upload_file(save_url, file_name)
                files_result.append(upload_file_result)  # 只保存更新的文件
                file_ids_result.append(file_id)
                file_id_uuid_dict[file_id] = upload_file_result.get('unique_name', '')
        return files_result, file_ids_result, file_id_uuid_dict

    def download_typt_file(self, save_url, file_url, file_name):
        logger.info('下载文件，原file_url：{}'.format(file_url))
        file_url = re.sub(TYPT_DOMAIN_NAME, TYPT_HOST_PORT, file_url)
        if not os.path.exists(save_url):
            os.makedirs(save_url)
        logger.info('下载文件，save_url：{}，file_url：{}, file_name:{}'.format(save_url,file_url, file_name))
        result = requests.get(file_url)
        with open(os.path.join(save_url, file_name), 'wb') as f:
            f.write(result.content)
            f.close()

    def web_api_upload_file(self, save_url, file_name):
        url = API_HOST_IP + API_UPLOAD_FILE
        payload = {}
        files = [
            ('file', (
            file_name, open(os.path.join(save_url, file_name), 'rb'), 'application/msword'))
        ]
        headers = {
            'Authorization': 'Bearer {}'.format(ConnectInner(self.employeeId).request_user_token()),
            'Cookie': 'JSESSIONID=D2A08BABC01930778407C66C69796E3C'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        logger.info('上传文件到datagrand，response：{}'.format(response.json()))

        return response.json().get('data')

    def create_task(self,params):
        url = API_HOST_IP + CREATE_TASK
        payload = json.dumps(params)
        headers = {
            'Authorization': 'Bearer {}'.format(ConnectInner(self.employeeId).request_user_token()),
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=D2A08BABC01930778407C66C69796E3C'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('创建任务到datagrand，response：{}'.format(response.json()))

        # 设置自审任务获取时间
        task_id = response.json().get('data').get('task_id')
        return task_id

    def update_task(self, params):
        url = API_HOST_IP + UPDATE_TASK
        payload = json.dumps(params)
        headers = {
            'Authorization': 'Bearer {}'.format(ConnectInner(self.employeeId).request_user_token()),
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=D2A08BABC01930778407C66C69796E3C'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('追加文件到datagrand，response：{}'.format(response.json()))
        task_id = response.json().get('data').get('task_id')
        return task_id