# -*- coding: utf-8 -*-
import warnings
from flask_smorest import Api as _Api
from flask_smorest import Blueprint as _Blueprint
from marshmallow.exceptions import ValidationError
from webargs.flaskparser import FlaskParser
from werkzeug.exceptions import UnprocessableEntity

from configs.base import PROJECT_NAME
from utils.response_container import BaseResponse
from . import app
from .logger_process import logger

app.config['API_TITLE'] = PROJECT_NAME
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['JSON_AS_ASCII'] = False

warnings.simplefilter('ignore', UserWarning)


class Api(_Api):

    def _register_error_handlers(self):
        pass


class Parser(FlaskParser):
    KNOWN_MULTI_FIELDS = []  # 减少 FlaskParser 自己会自己将 request.params 处理成List的问题

    # def _raw_load_json(self, req):
    #     """
    #     兼容不传ContentType的问题
    #     """
    #     return req.get_json(force=True)


class Blueprint(_Blueprint):
    ARGUMENTS_PARSER = Parser()

    def add_resource(self, resource, *urls):
        for url in urls:
            self.route(url)(resource)


@app.errorhandler(422)
def c_422_handler(error: UnprocessableEntity):
    logger.debug(f"error message is {error.data['messages']}")
    return BaseResponse(
        message=" The request was well-formed but was unable to be followed due to semantic errors.",
        data=error.data['messages'],
        status=422,
        code=422,
    ).asdict()


@app.errorhandler(ValidationError)
def c_validate_handler(error: ValidationError):
    return BaseResponse(
        message=" The request was well-formed but was unable to be followed due to semantic errors.",
        data=error.messages,
        status=422,
        code=422,
    ).asdict()


smorest = Api(app)
