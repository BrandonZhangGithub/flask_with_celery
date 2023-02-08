# from celery_tasks.celery_app import celery
from celery_tasks.celery_app import celery
from celery.utils.log import worker_logger
from models.research_report_task_model import research_report_task_model


@celery.task(queue="main_queue")
def check_sensitive_words_task(task_id):
    worker_logger.info('开始敏感词检测')
    result, download_url = research_report_task_model.query_and_save_sensitive_result(task_id)
    worker_logger.info('敏感词result：{}，download_url：{}'.format(result, download_url))
    worker_logger.info('敏感词检测成功')

@celery.task(queue="main_queue")
def check_separation_wall_task(task_id):
    worker_logger.info('开始隔离墙检测')
    result, download_url = research_report_task_model.query_and_save_separation_result(task_id)
    worker_logger.info('隔离墙result：{}，download_url：{}'.format(result, download_url))
    worker_logger.info('隔离墙检测成功')