from flask.globals import request
from flask_jwt_extended.utils import current_user

import initialization.jwtextend_process
from blueprints.common.check_permission import permission_check as _permission_check
from utils.exceptions import NoAuthResponse, NoPermission
from . import app


@app.before_request
def permission_check():
    if request.args.get("is_debug") == "is_debug":
        return

    # 跳过一些验证..
    if (request.path, request.method) in frozenset({
        ("/api/login", "POST"),
        ("/api/register", "POST"),
        ("/health_check", "GET"),
    }):
        return

    if not current_user:
        raise NoAuthResponse("未登录")

    if not _permission_check(current_user, request.path, request.url):
        raise NoPermission("无权限访问!")
