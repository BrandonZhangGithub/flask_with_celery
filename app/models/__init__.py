# 操作entities的方法合集, 如果entities的操作对象从sqlalchemy变为了mongodb, 只需要修改这里面的方法. 可以直接被service调用.
# -*- coding: utf-8 -*-
from contextlib import contextmanager
from functools import wraps

from sqlalchemy.exc import SQLAlchemyError

from initialization.logger_process import logger
from initialization.sqlalchemy_process import session


def commit(fn):
    """
    commit 装饰器，用法:

        @commit
        def trans_func():
            do_something_important()


    commit方法会维护自己的子事务，且不影响外层事务，
    这意味着被commit装饰的方法要么一起成功，要么一起失败
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):

        with safe_commit():
            return fn(*args, **kwargs)

    return wrapper


@contextmanager
def safe_commit():
    """
    安全提交方法, 如果你需要在代码里面手动提交当前事务, 这个方法可以安全处理.

    方法:
       with safe_commit() as session:
            user = User.create()

    使用多层嵌套的safe_commit()将自动开启子事务，即所有事务成功才会提交
    with safe_commit() as session:
        do()
        with safe_commit() as session:
            do()
            with safe_commit() as session:
                do()
            raise SQLAlchemyError  # 内部的提交也不会生效
    """
    try:
        session.begin(subtransactions=True)
        yield session

        # 如果是最上层的事务，保证再做一次提交
        if session().transaction.parent.parent is None:
            session.commit()

        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        logger.exception(e)
        raise e
