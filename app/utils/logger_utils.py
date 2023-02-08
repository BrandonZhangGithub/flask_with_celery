# -*- coding: utf-8 -*-

from functools import wraps
from logging import getLogger
from time import time

logger = getLogger()

BANNER = '{0: ^100}'


def banner(value):
    return BANNER.format(value)


def timer_log(_logger=logger):
    """打印出一个函数的耗时"""

    def wrapper(fn):

        @wraps(fn)
        def inner(*args, **kwargs):
            t1 = time()
            _logger.info(banner(f"函数{fn.__name__}开始运行"))
            try:
                res = fn(*args, **kwargs)
            except BaseException as e:
                _logger.info(banner(f"函数{fn.__name__}出现异常，用时{'{:.4f}'.format(time() - t1)}"))
                _logger.error(e)
                raise e
            finally:
                _logger.info(banner(f"函数{fn.__name__}函数处理结束，用时{'{:.4f}'.format(time() - t1)}"))

            return res

        return inner

    return wrapper


if __name__ == '__main__':
    from logging import basicConfig, getLogger
    basicConfig(level="INFO")
    logger = getLogger()
    from time import sleep

    @timer_log(logger)
    def fn_test():
        """测试函数"""
        logger.info("这是一个测试函数，让我先睡两秒")
        sleep(2)
        logger.info("测试函数结束")

    fn_test()
