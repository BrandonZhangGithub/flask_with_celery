#! /usr/bin/env python
# -*- coding:utf-8 -*-
# 为Flask添加sentry支持

from configs import sysconf
from . import app

app.config['SENTRY_ENABLE'] = False if not sysconf.SENTRY_DNS else sysconf.SENTRY_ENABLE  # 如果没有设置DNS默认为False
app.config['SENTRY_DNS'] = sysconf.SENTRY_DNS

if app.config["SENTRY_ENABLE"]:
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(dsn=app.config['SENTRY_DNS'], integrations=[FlaskIntegration()])

    @app.route('/debug-sentry')
    def trigger_error():
        1 / 0
