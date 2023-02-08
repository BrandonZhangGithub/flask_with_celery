"""
拓展flask的self
"""

from flask import request
from flask.wrappers import Request as _Request

from utils.common_tools import get_request_id
from . import app


class Request(_Request):

    @property
    def request_id(self):
        if self._request_id:
            return self._request_id

        request_id = self.headers.get("Request-ID")
        if not request_id:
            request_id = get_request_id()

        self._request_id = request_id
        return self._request_id

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._request_id = None
        self._param = None

    @property
    def params(self):
        """
        根据不同类型的请求去获取对应的data
        POST, PUT -> request.data or request.form
        GET, DELETE -> request.args
        """
        if self._param is not None:
            return self._param

        data = {}
        if self.method in ("POST", "PUT"):
            data = self.get_json(force=True) if self.data.strip() else {k: v for k, v in self.form.items()}
        elif self.method in ("DELETE", "GET"):
            data = self.args
        self._param = data
        return data


app.request_class = Request


@app.before_request
def log_request_info():
    """
    打印入参
    """
    app.logger.debug(request.request_id)
    app.logger.debug(request.params)
    ...
