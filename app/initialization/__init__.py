from flask import Flask
from configs import base

from celery import Celery
from celery.schedules import crontab
class CelertTaskConf():
    imports = (
        'celery_tasks.task.flask_check_tasks',
        'celery_tasks.task.sync_typt_users'
    )
    timezone = "Asia/Shanghai"
    enable_utc = False
    worker_concurrency = 2
    task_ignore_result = True
    beat_schedule = {
        "every-5-seconds-task": {
            "task": "celery_tasks.task.sync_typt_users.sync_typt_users_task",
            "schedule": crontab(minute=0, hour=2),
            "args": ()
        }}

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=base.BROKER,
        backend=base.BACKEND,
    )
    celery.config_from_object(CelertTaskConf)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app: Flask

def _init_custom():
    """
    非强制导入, 使用到就打开注释
    """
    from . import (  # 这里开始, 选择性导入;; sentry_process,; ,; mongodb_process,; permission_process,
        # session_process,
        jwtextend_process,
        redis_process,
        )


def _init():
    """
    初始化所有APP的配置, 导入自己所需要使用的功能, 一些初始化必须要的, 不可以删掉
    """
    from . import (command_process, exception_process, health_check_process, logger_process, request_process,
                   sqlalchemy_process, smorest_process)


class Config:
    SECRET_KEY = "secret$%^&*key!@#$%^774##$%^&*(you#!!@%never!@#$%^&guess"

def create_app() -> Flask:
    global app
    app = Flask(base.PROJECT_NAME)

    app.config.from_object(Config)

    app.secret_key = "secret$%^&*key!@#$%^774##$%^&*(you#!!@%never!@#$%^&guess"
    _init()
    _init_custom()


    return app


def register_blueprints():
    from . import blueprint_process
