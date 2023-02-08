# coding=utf-8
import json
import time, datetime

import re
from .. import xyzq
from initialization.logger_process import logger
from configs.base import *
from utils.response import RF
from configs.base import TIME_RE
from flask.views import MethodView
from utils.resource_utils.utils import ConnectTypt
from schemas.ideas_schema import SensitiveWordsSchema
from models.research_report_task_model import research_report_task_model
from models.research_report_basic_information_model import research_report_basic_information_model
from models.research_report_file_model import research_report_file_model
from models.research_report_time_model import research_report_time_model


class TaskTimetInfo(MethodView):
    @xyzq.arguments(SensitiveWordsSchema, as_kwargs=True, location="query")
    def get(self, task_id):
        now_time = datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            created_time = self.get_research_report_time(task_id)
        except Exception as e:
            logger.exception(e)
            created_time = ''

        audit_result = "时间校验无误"
        if not created_time:
            created_time = '未识别'
            audit_result = '时间校验有误，请确认'
        elif created_time != now_time:
            audit_result = '时间校验有误，请确认'

        if audit_result == "时间校验无误":
            return RF.success(data=dict(
                    research_report_time=created_time,
                    current_server_time=now_time,
                    audit_result = audit_result
                ))
        else:
            return RF.success(data=dict(
                    research_report_time=created_time,
                    current_server_time=now_time,
                    audit_result = audit_result
                ),
                status=201)

    def get_research_report_time(self, task_id): # 优先返回最新研报的后处理时间，如果不存在，就返回产品原研报时间
        file_id = research_report_file_model.query_report_file_id_by_task_id(task_id)

        post_process_time = research_report_time_model.get_remark_date(file_id)
        if post_process_time:
            return post_process_time
        else:
            research_report_items = research_report_basic_information_model.query_result_by_file_id(file_id)

            research_report_time = ''
            re_extracted_time_string = ''
            for item in research_report_items:
                if item.report_date:
                    research_report_time = json.loads(item.report_date).get('value', '')
            if research_report_time:
                time_re_result = re.search(TIME_RE, research_report_time)
                if time_re_result and time_re_result.group(1) and time_re_result.group(2) and time_re_result.group(3):
                    year = str(time_re_result.group(1))
                    month = str(time_re_result.group(2)) if len(time_re_result.group(2))==2 else '0' + str(time_re_result.group(2))
                    day = str(time_re_result.group(3)) if len(time_re_result.group(3))==2 else '0' + str(time_re_result.group(3))
                    re_extracted_time_string = '-'.join([year, month, day])
            return re_extracted_time_string
