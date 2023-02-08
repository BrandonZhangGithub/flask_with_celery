import random
from flask.views import MethodView

from .. import xyzq
from configs.base import *
from utils.response import RF
from schemas.inner_call_schema import DraftFileNameSchema
from models.research_report_file_model import research_report_file_model
from models.check_user_stock_info_model import check_user_stock_info_model

class DraftFileName(MethodView):
    @xyzq.arguments(DraftFileNameSchema, as_kwargs=True, location="query")
    def get(self, file_id):
        file_name = research_report_file_model.query_excel_name_by_draft_id(file_id)
        return RF.success(data={"file_name": file_name})

class AllUserInfo(MethodView):
    def get(self):
        users = check_user_stock_info_model.query_all_users()
        return RF.success(data={"user_info": [{
            'nickname': user.nickname,
            'certificate': user.certificate,
            'email': user.email
        } for user in users]
        })