# coding=utf-8
from typing import List, Tuple

from sqlalchemy import func
import json
import time
import requests
from configs.base import *
from initialization.sqlalchemy_process import session
from entities.research_report_audit_task_entity import ResearchReportAuditTaskEntity
from entities.research_report_typt_task_con_entity import ResearchReportTyptTaskConEntity
from entities.research_report_audit_task_user_relation_entity import ResearchReportAuditTaskUserRelationEntity
from utils.resource_utils.utils import ConnectTypt, ConnectInner, ConnectDgauth


# noinspection DuplicatedCode
class ResearchReportTaskConModel():
    _entity = ResearchReportTyptTaskConEntity

    def get_task_id_by_doc_id(self, doc_id):
        q = session.query(self._entity).filter(self._entity.doc_id == doc_id)
        return q.first().task_id

    def check_doc_id_exist(self, doc_id):
        q = session.query(ResearchReportTyptTaskConEntity).filter(ResearchReportTyptTaskConEntity.doc_id == doc_id)
        return bool(q.first())

research_report_task_con_model = ResearchReportTaskConModel()
