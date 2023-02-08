from celery.utils.log import worker_logger
import requests
import json
from celery_tasks.celery_app import celery
from resources.xyzq.anaplatform.sync_users_first_resource import SyncUsers

@celery.task(queue="main_queue")
def sync_typt_users_task():
    worker_logger.info('开始同步投研平台用户数据')
    sync_users = SyncUsers(None, True, worker_logger)
    worker_logger.info('开始同步research_report_typt_users')
    sync_users.sync_research_report_typt_users()
    worker_logger.info('research_report_typt_users同步完成')
    worker_logger.info('开始同步dg_oauth_users')
    sync_users.sync_dg_oauth_users()
    worker_logger.info('dg_oauth_users同步完成')
    worker_logger.info('投研平台用户数据同步成功')