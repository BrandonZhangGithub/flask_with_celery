import random
from flask.views import MethodView

import os
import requests
import datetime
from .. import xyzq
from configs.base import *
from utils.response import RF
from schemas.anaplatform_schema import SyncCallBackSchema
from initialization.sqlalchemy_process import session



class InitCustomizedTables(MethodView):
    def get(self):
        CREATE_TYPT_TASK_CON_SQL = "CREATE TABLE `research_report_typt_task_con` (`id` int(11) NOT NULL AUTO_INCREMENT COMMENT '默认ID',`task_id` int(11) DEFAULT NULL COMMENT '任务ID',`doc_id` int(11) DEFAULT NULL COMMENT '投研平台文档ID', `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP, `last_update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"
        CREATE_TYPT_USERS = "CREATE TABLE `research_report_typt_users` (`id` int(11) NOT NULL AUTO_INCREMENT COMMENT '默认ID',`user_id` int(11) DEFAULT NULL COMMENT '投研平台ID',`username` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '工号-账户名',`nickname` varchar(100) COLLATE utf8mb4_unicode_ci,`certificate` varchar(100) COLLATE utf8mb4_unicode_ci,`email` varchar(100) COLLATE utf8mb4_unicode_ci,`isdisable` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否生效',PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"

        session.execute(CREATE_TYPT_TASK_CON_SQL)
        session.execute(CREATE_TYPT_USERS)

        return RF.success()