# -*- coding: utf-8 -*-
"""
@create_at: 2020/08/22

@author: LuShuYang

@attention: 提供缓存接口的功能, 需要在配置中启用缓存功能
"""

import hashlib
import json
import time
from functools import wraps

from flask import Response, current_app, request


def cache_request(seconds=10):
    """缓存一个请求"""
    redis_cli = current_app.extensions["redis_cli"]

    def outer(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.method != 'GET':
                data = request.data
            else:
                data = bytes(request.url, "utf8")

            # data Must be bytes
            key = hashlib.md5(data).hexdigest()
            flag = "flag_" + key

            # 读到缓存结果返回
            cache_res = redis_cli.get(key)
            if cache_res:
                return json.loads(cache_res)

            # flag代表此时正在某一个地址正在被请求, 防止击穿
            while not redis_cli.set(flag, 1, ex=10, nx=True):
                time.sleep(0.1)

                # 如果读到了其他请求处理的缓存, 返回
                cache_res = redis_cli.get(key)

                if cache_res:
                    redis_cli.delete(flag)  # 删除flag
                    return json.loads(cache_res)

            try:
                res = fn(*args, **kwargs)

                if isinstance(res, Response):
                    data = res.data
                else:
                    data = json.dumps(res)

                redis_cli.setex(
                    key,
                    seconds,
                    data,
                )

                return res
            finally:
                redis_cli.delete(flag)  # 删除flag

        return wrapper

    return outer
