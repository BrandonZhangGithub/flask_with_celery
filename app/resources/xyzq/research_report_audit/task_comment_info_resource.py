# coding=utf-8
from .. import xyzq
from configs.base import *
from utils.response import RF
from flask.views import MethodView
from utils.resource_utils.utils import ConnectTypt
from schemas.ideas_schema import SensitiveWordsSchema
from models.research_report_task_model import research_report_task_model

class TaskCommentInfo(MethodView):
    @xyzq.arguments(SensitiveWordsSchema, as_kwargs=True, location="query")
    def get(self, task_id):
        doc_id = research_report_task_model.get_task_doc_id(task_id)
        comment_info = ConnectTypt().query_task_comment_info(doc_id)
        return RF.success(data=comment_info)