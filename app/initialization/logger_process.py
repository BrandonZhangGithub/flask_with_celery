"""
Created on 2019年1月14日
@author: ljbai

comment by LuShuYang:
    Flask的log分为两个部分, 一个是在业务代码里面使用的app.logger, 一个是werkzueg的logger,

    在本地的时候我们将werkzueg的logger和app.logger重定向到标注输出中,

    如果在部署的时候, 使用gunicorn部署, 再将gunicorn的logger和app的logger都重定向到File中.

    因此不修改werkzeug的logger, 且不要使用werkzueg进行部署.
"""
import logging

from configs.base import PROJECT_NAME
from configs.sysconf import LOG_LEVEL

logger = logging.getLogger(PROJECT_NAME)  # same as app.logger
logger.setLevel(LOG_LEVEL)


formatter = logging.Formatter('%(asctime)s %(levelname)s %(pathname)s:%(lineno)s %(funcName)s %(message)s')

for handler in logger.handlers:
    handler.formatter = formatter
