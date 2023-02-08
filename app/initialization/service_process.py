# -*- coding: utf-8 -*-
from initialization.logger_process import logger
from libs import set_logger, ServiceException
from utils.response_container import BaseResponse
from . import app

set_logger(logger)


@app.errorhandler(ServiceException)
def service_exception(e: ServiceException):
    return BaseResponse(message=f"third party service is unavailable right now, error: {e}", code=500, status=500).asdict()
