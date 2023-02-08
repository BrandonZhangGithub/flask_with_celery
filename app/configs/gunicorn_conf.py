import multiprocessing
import os
from sys import stdout

from configs import base, sysconf

if not os.path.exists(sysconf.LOG_DIR):
    os.makedirs(sysconf.LOG_DIR)

bind = sysconf.BIND

# 启动的进程数
workers = sysconf.WORK_NUMS or multiprocessing.cpu_count()

x_forwarded_for_header = 'X-FORWARDED-FOR'

loglevel = sysconf.LOG_LEVEL

# timeout
timeout = 30

file_name = os.path.join(sysconf.LOG_DIR, "log.log")

# 这里的logging会直接复写掉app的logger.
logconfig_dict = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {},
    'loggers': {
        "gunicorn.error": {
            "handlers": ["file_handler", "stream"],  # 对应下面的键
            "qualname": "gunicorn.error",
            "level": loglevel,
        },
        "gunicorn.access": {
            "handlers": ["file_handler", "stream"],
            "qualname": "gunicorn.access",
            "level": loglevel
        },
        base.PROJECT_NAME: {
            "handlers": ["dg_file_handler", "stream"],
            "level": loglevel
        }
    },
    'handlers': {
        "file_handler": {
            "class": "dg_logging.templates.config_dicts.MultiprocessSafeTimedRotatingFileHandler",
            "backupCount": 10,
            "when": "d",
            "filename": file_name,
        },
        "dg_file_handler": {
            "class": "dg_logging.templates.config_dicts.MultiprocessSafeTimedRotatingFileHandler",
            "backupCount": 10,
            "when": "d",
            "filename": file_name,
        },
        "stream": {
            "class": "logging.StreamHandler",
            "stream": stdout
        }
    }
}

# 如果部署的时候开启了debug模式, 可以启用auto_reload
reload = sysconf.AUTO_RELOAD
