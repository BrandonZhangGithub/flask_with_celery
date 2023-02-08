# -*- coding: utf-8 -*-
from .. import FlaskClient
from .api import some_api


class SomeServiceClient(FlaskClient):

    def do_something(self, signal: str) -> dict:
        return self._post(some_api, data=dict(signal=signal))
