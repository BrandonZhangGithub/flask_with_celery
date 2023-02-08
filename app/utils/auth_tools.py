from functools import wraps

from flask import abort
from flask_jwt_extended import current_user


def admin_required(fn):
    """
    规定某一个接口只能对管理员开放
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):

        if current_user.is_superuser:
            abort(403)

        return fn(*args, **kwargs)

    return wrapper


def login_required(fn):
    """
    只授权给登录的人
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):

        if current_user.is_anonymous:
            abort(403)

        return fn(*args, **kwargs)

    return wrapper
