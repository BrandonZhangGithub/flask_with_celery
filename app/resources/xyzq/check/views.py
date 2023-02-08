import random
from flask.views import MethodView

from .. import xyzq
from configs.base import *
from utils.response import RF
from utils.resource_utils.utils import InterfaceForwardServices, ConnectTypt, ConnectDgauth
from schemas.ideas_schema import SensitiveWordsSchema, FrontendMenuSchema
from configs.static_variables import TyptResponseStatusEnum, TyptTaskStatusEnum
from schemas.response_schema import BaseResponseSchema, ListResponseSchema
from utils.exceptions import TipResponse
from models.research_report_task_model import research_report_task_model
from utils.response_container import BaseResponse, ListData, ListResponse
from configs.static_variables import XYZQTaskWorkflowRequestStatus

class CheckSensitiveWords(MethodView):
    @xyzq.arguments(SensitiveWordsSchema, as_kwargs=True, location="query")
    def get(self, task_id):
        if CURRENT_ENV == 'SAAS':
            if random.random() > 0.5:
                return RF.success(data={
                    "result":"您的报告附件存在敏感字词：最出现1次;",
                    "download_url":"http://192.20.103.97:8080/anaplatform/downlodDWFile.do?fileName=edc42d04-4bae-4d4a-b5cd-7da868410368.docx"
                    })
            else:
                return RF.success(data={
                    "result":"本报告附件不存在合规限制名单",
                    "download_url":""
                    })
        else:
            result, download_url = research_report_task_model.get_sensitive_result(task_id)
            return RF.success(data={
                "result": result,
                "download_url": download_url
            })

class CheckSeparationWall(MethodView):
    @xyzq.arguments(SensitiveWordsSchema, as_kwargs=True, location="query")
    def get(self, task_id):
        if CURRENT_ENV == 'SAAS':
            if random.random() > 0.5:
                return RF.success(data={
                    "result":"您的报告附件存在隔离字词：最出现1次;",
                    "download_url":"http://192.20.103.97:8080/anaplatform/downlodDWFile.do?fileName=edc42d04-4bae-4d4a-b5cd-7da868410368.docx"
                    })
            else:
                return RF.success(data={
                    "result":"本报告附件不存在合规限制名单",
                    "download_url":""
                    })
        else:
            result, download_url = research_report_task_model.get_separation_result(task_id)
            return RF.success(data={
                "result": result,
                "download_url": download_url
            })

class CheckIfCallBack(MethodView):
    @xyzq.arguments(SensitiveWordsSchema, as_kwargs=True, location="query")
    def get(self, task_id):
        if CURRENT_ENV == 'SAAS':
            random_float = random.random()
            if random_float < 0.33:
                return RF.success(data={
                    "result": True,
                    "jump_direct": False,
                    "message": "调用成功"
                    },
                    )
            elif random_float >= 0.33 and random_float <= 0.66:
                return RF.success(data={
                    "result": False,
                    "jump_direct": False,
                    "message":"暂无权限"
                    },
                    )
            else:
                return RF.success(data={
                    "jump_direct": True,
                    "result": True,
                    "message":"调用成功"
                    },
                    )
        else:
            # 为了让自审阶段的撤回直接跳转投研平台
            if research_report_task_model.check_three_in_one(task_id) \
                    and research_report_task_model.get_task_status != XYZQTaskWorkflowRequestStatus.CALL_BACK \
                      and ConnectTypt().get_task_detail(research_report_task_model.get_task_doc_id(task_id)).get('taskStatus') != TyptTaskStatusEnum.IN_FLOW:
                return RF.success(data={
                    "jump_direct": True,
                    "result": True,
                    "message": "调用成功"
                },
                )
            elif research_report_task_model.get_typt_task_status(task_id) in [TyptTaskStatusEnum.CALL_BACK, TyptTaskStatusEnum.IN_BOX]:
                return RF.success(data={
                    "jump_direct": False,
                    "result": False,
                    "message": "暂无权限"
                },
                )
            else:
                return RF.success(data={
                "jump_direct": False,
                "result": True,
                "message": "调用成功"
                })

class FrontendMenu(MethodView):
    @xyzq.arguments(FrontendMenuSchema, as_kwargs=True, location="query")
    def get(self, appId):
        response_json = ConnectDgauth().get_all_menu(appId)
        return response_json