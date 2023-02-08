# coding=utf-8
from typing import List, Tuple

from sqlalchemy import func
import json
import time
import os
import requests
from configs.base import *
from flask import request
import jwt
from initialization.sqlalchemy_process import session
from entities.research_report_audit_task_entity import ResearchReportAuditTaskEntity
from entities.research_report_typt_task_con_entity import ResearchReportTyptTaskConEntity
from entities.research_report_audit_task_user_relation_entity import ResearchReportAuditTaskUserRelationEntity
from models.research_report_file_model import research_report_file_model
from models.check_user_stock_info_model import check_user_stock_info_model
from utils.resource_utils.utils import ConnectTypt, ConnectInner, ConnectDgauth
from configs.static_variables import XYZQ_TaskWorkflowRequestStatus
from initialization.logger_process import logger


class ResearchReportTaskModel():
    _entity = ResearchReportAuditTaskEntity

    # 设置审核人员获得任务时间
    def add_task_assigned_time(self, task_id):
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if item.extended:
            extended = json.loads(item.extended)
            extended['task_assigned_time'] = now_time
        else:
            extended = {'task_assigned_time': now_time}
        item.extended = json.dumps(extended, ensure_ascii=False)
        session.commit()

    # 保存创建任务时doc_id, 删除当前不存在的底稿
    def save_task_create_info(self, task_id, doc_id, draft_file_ids, research_report_file_ids, file_id_uuid_dict, update=False):
        # 保存extended字段
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        if item.extended:
            extended = json.loads(item.extended)
            if update:
                to_remove_keys = []
                to_delete_unique_names = []
                for ori_draft_file_ids, unique_name in extended['file_id_uuid_dict'].items():
                    if int(ori_draft_file_ids) not in draft_file_ids:
                        to_remove_keys.append(ori_draft_file_ids)
                        to_delete_unique_names.append(unique_name)
                for to_remove_key in to_remove_keys:
                    del extended['file_id_uuid_dict'][to_remove_key]
                for to_delete_unique_name in to_delete_unique_names:
                    research_report_file_model.delete_file_by_unique_name(task_id, to_delete_unique_name)
                extended['file_id_uuid_dict'].update(file_id_uuid_dict)
            else:
                extended['file_id_uuid_dict'] = file_id_uuid_dict

            extended['doc_id'] = doc_id
            extended['draft_file_ids'] = draft_file_ids
            extended['research_report_file_ids'] = research_report_file_ids

        else:
            extended = {'doc_id': doc_id,
                        'draft_file_ids': draft_file_ids,
                        'research_report_file_ids': research_report_file_ids,
                        'file_id_uuid_dict': file_id_uuid_dict}
        item.extended = json.dumps(extended, ensure_ascii=False)
        session.commit()

        if not update:
            # 保存关系表
            con = ResearchReportTyptTaskConEntity()
            con.task_id = task_id
            con.doc_id = doc_id
            session.add(con)
            session.commit()

    # 单独判断只做了删除底稿的动作
    def solve_only_delete(self, task_id, docId, draft_file_ids, ori_draft_file_ids):
        to_delete_unique_names = []
        to_remove_keys = list(set(ori_draft_file_ids) - set(draft_file_ids))
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        extended = json.loads(item.extended)
        for to_remove_key in to_remove_keys:
            to_delete_unique_names.append(extended['file_id_uuid_dict'][str(to_remove_key)])
            del extended['file_id_uuid_dict'][str(to_remove_key)]
        for to_delete_unique_name in to_delete_unique_names:
            research_report_file_model.delete_file_by_unique_name(task_id, to_delete_unique_name)


    #　获取创建任务时doc_id
    def get_task_doc_id(self, task_id):
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        extended = json.loads(item.extended)
        return extended.get('doc_id')

    # 获取审核人员获得任务时间-多任务
    def get_task_assigned_time(self, task_ids):
        items = session.query(self._entity).filter(self._entity.id.in_(task_ids)).all()
        return {item.id: json.loads(item.extended)['task_assigned_time'] if item.extended else '' for item in items}

    # 设置撤回状态
    def set_call_back_status(self, task_id):
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        extended = json.loads(item.extended)
        extended['status_before_call_back'] = item.status
        item.extended = json.dumps(extended, ensure_ascii=False)
        item.status = XYZQ_TaskWorkflowRequestStatus.CALL_BACK
        session.commit()

    # 确认撤回状态并修改为正常状态
    def remove_call_back_status(self, task_id):
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        if item.status == XYZQ_TaskWorkflowRequestStatus.CALL_BACK:
            extended = json.loads(item.extended)
            item.status = extended['status_before_call_back']
        session.commit()

    # 获取任务状态
    def get_task_status(self, task_id):
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        return item.status

    # 获取投研平台任务状态
    def get_typt_task_status(self, task_id):
        docId = self.get_task_doc_id(task_id)
        task_detail = ConnectTypt().get_task_detail(docId)
        return task_detail.get('taskStatus')

    # 获取entended字段
    def get_extended_by_task_id(self, task_id):
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        extended = json.loads(item.extended)
        return extended

    # 更新entended字段
    def update_extended_by_task_id(self, task_id, extended):
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        item.extended = json.dumps(extended, ensure_ascii=False)
        session.commit()
        return extended

    #查询任务创建人
    def query_creator_id(self, task_id):
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        return item.creator_id

    def query_now_login_id(self):
        return ConnectDgauth().get_user_by_username(ConnectTypt().user_id).get('userId')

    def get_task_info(self, task_id):
        docId = self.get_task_doc_id(task_id)
        task_info = ConnectTypt().get_one_task_info(docId)
        return task_info

    # 自审开启任务流
    def start_process(self, task_id, customized):
        docId = self.get_task_doc_id(task_id)
        response_data = ConnectTypt().send_start_process_request(docId, customized)
        return response_data

    # 正常审核通过
    def next_process(self, task_id, customized):
        docId = self.get_task_doc_id(task_id)
        response_data = ConnectTypt().send_next_process_request(docId, customized)
        return response_data

    # 撤回
    def back_process(self, task_id):
        docId = self.get_task_doc_id(task_id)
        response_data = ConnectTypt().send_back_process_request(docId)
        return response_data

    # 获取任务审核记录
    def get_work_flow_info(self, task_id):
        docId = self.get_task_doc_id(task_id)
        response_data = ConnectTypt().query_work_flow_info(docId)
        return response_data

    # 敏感词检测
    def query_and_save_sensitive_result(self, task_id):
        docId = self.get_task_doc_id(task_id)
        response_json = ConnectTypt(ADMIN_EMPLOYEE_ID).send_sensitive_check(docId)
        result, download_url = response_json.get('result', ""), response_json.get('downUrl', "")

        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        if item.extended:
            extended = json.loads(item.extended)
            extended['sensitive_words_result'] = {
                'result': result,
                'download_url': download_url
            }
        else:
            extended = {'sensitive_words_result': {
                'result': result,
                'download_url': download_url
            }}
        item.extended = json.dumps(extended, ensure_ascii=False)
        session.commit()
        return result, download_url

    # 敏感词检测结果查询
    def get_sensitive_result(self, task_id):
        result, download_url = '暂无敏感词结果', ''
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        if item.extended:
            extended = json.loads(item.extended)
            if 'sensitive_words_result' in extended:
                result, download_url = extended['sensitive_words_result']['result'], extended['sensitive_words_result']['download_url']
        return result, download_url

    # 隔离墙检测
    def query_and_save_separation_result(self, task_id):
        docId = self.get_task_doc_id(task_id)
        response_json = ConnectTypt(ADMIN_EMPLOYEE_ID).send_sepatation_check(docId)
        result, download_url = response_json.get('result', ""), response_json.get('downUrl', "")

        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        if item.extended:
            extended = json.loads(item.extended)
            extended['separation_wall_result'] = {
                'result': result,
                'download_url': download_url
            }
        else:
            extended = {'separation_wall_result': {
                'result': result,
                'download_url': download_url
            }}
        item.extended = json.dumps(extended, ensure_ascii=False)
        session.commit()
        return result, download_url

    # 清空敏感词与隔离墙检测结果
    def clear_sensitive_and_separation(self, task_id):
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        if item.extended:
            extended = json.loads(item.extended)
            if 'sensitive_words_result' in extended:
                extended.pop('sensitive_words_result')
            if 'separation_wall_result' in extended:
                extended.pop('separation_wall_result')
            item.extended = json.dumps(extended, ensure_ascii=False)
            session.commit()

    # 隔离墙检测结果查询
    def get_separation_result(self, task_id):
        result, download_url = '暂无隔离墙结果', ''
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        if item.extended:
            extended = json.loads(item.extended)
            if 'separation_wall_result' in extended:
                result, download_url = extended['separation_wall_result']['result'], extended['separation_wall_result']['download_url']
        return result, download_url

    # 判断task_detail是否包含reviewList
    def check_review_list_not_exist(self, task_id):
        docId = self.get_task_doc_id(task_id)
        response_json = ConnectTypt().get_task_detail(docId)
        if not response_json.get('reviewList'):
            return True

    #　动态添加可见用户
    def add_forward_to_user_ids(self, task_id, forward_to_user_ids):
        def query_con_exist(task_id, user_id):
            q = session.query(ResearchReportAuditTaskUserRelationEntity).filter(ResearchReportAuditTaskUserRelationEntity.research_report_audit_task_id == task_id).filter\
                (ResearchReportAuditTaskUserRelationEntity.user_id == user_id)
            return q.first()

        def bulk_create_by_entities(entities: list, return_defaults=False):
            if entities:
                if len(entities) <= 1000:
                    session.bulk_save_objects(entities, return_defaults=return_defaults)
                else:
                    tmp_list = []
                    for index, item in enumerate(entities):
                        tmp_list.append(item)
                        if len(tmp_list) == 1000 or index == len(entities) - 1:
                            session.bulk_save_objects(tmp_list, return_defaults=return_defaults)
                            session.flush()
                            tmp_list = []
                session.commit()

        relation_list = []
        for user_id in set(forward_to_user_ids):
            if not query_con_exist(task_id, user_id):
                r = ResearchReportAuditTaskUserRelationEntity()
                r.research_report_audit_task_id = task_id
                r.user_id = int(user_id)
                relation_list.append(r)
        bulk_create_by_entities(relation_list)

    # 删除任务
    def delete_task_by_id(self, task_id):
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        item.status = 0
        session.commit()

    # 获取导出文件名
    def get_export_filename(self, task_id):
        def download_typt_file(save_url, file_url, file_name):
            if not os.path.exists(save_url):
                os.makedirs(save_url)
            result = requests.get(file_url)
            with open(os.path.join(save_url, file_name), 'wb') as f:
                f.write(result.content)
                f.close()

        save_url, file_name = '', ''
        docId = self.get_task_doc_id(task_id)
        task_detail = ConnectTypt().get_task_detail(docId)
        now_research_report_files = task_detail.get('attachment', [])
        for research_report_file in now_research_report_files:
            file_id = research_report_file['id']
            file_name = research_report_file['fileName']
            if file_name.endswith('pdf'):
                name = jwt.decode(request.headers.environ.get('HTTP_AUTHORIZATION').split(' ')[-1], verify=False, algorithms="HS256"
        )['username']
                typt_user_id = check_user_stock_info_model.get_user_id_by_user_name(name)
                file_url = TYPT_HOST_PORT + EXPORT_WATER_MARK.format(file_id, typt_user_id)
                save_url = os.path.join(STATIC_DIR, str(docId), 'research_report')
                download_typt_file(save_url, file_url, file_name)
                break
        return save_url, file_name

    # 校验任务创建人、当前处理人与当前登陆人是否为同一个人
    def check_three_in_one(self, task_id):
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        creater_user_id, operator_user_id = item.creator_id, item.operator_user_id
        try:
            operator_user_id = int(operator_user_id)
        except:
            return False
        current_login_user_id = jwt.decode(
                request.headers.environ.get('HTTP_AUTHORIZATION').split(' ')[-1], verify=False, algorithms="HS256"
            )['userId']
        if creater_user_id == operator_user_id == current_login_user_id:
            return True

    # 获取operator_status
    def query_operator_user_id(self, task_id):
        item = session.query(self._entity).filter(self._entity.id == task_id).first()
        return item.operator_status

research_report_task_model = ResearchReportTaskModel()
