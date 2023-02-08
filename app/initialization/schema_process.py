# -*- coding: utf-8 -*-

# 使用你喜欢的验证工具, 在这里注册验证的错误

from marshmallow.exceptions import ValidationError

from utils.response_container import BaseResponse
from . import app


@app.errorhandler(ValidationError)
def validate_error(validate_error: ValidationError):
    """处理Schema带来的报错"""
    return BaseResponse(message=validate_error.messages, code=400, status=400).asdict()
