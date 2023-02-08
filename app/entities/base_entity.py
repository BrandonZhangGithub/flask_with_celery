from datetime import datetime

from sqlalchemy import BOOLEAN, DATETIME, INTEGER, Column, true

from initialization.sqlalchemy_process import db, session


class ActiveQuery:

    def __set__(self, instance):
        return

    def __get__(self, instance, owner):
        return owner.query.filter_by(active=True)


class BaseEntity(db.Model):
    __abstract__ = True

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    active = Column(BOOLEAN, server_default=true(), nullable=False)
    create_time = Column(DATETIME, default=datetime.now, comment="修改时间")
    last_update_time = Column(DATETIME, default=datetime.now, onupdate=datetime.now, comment="最近修改时间", index=True)

    active_query = ActiveQuery()

    def auto_set_attr(self, **data):
        session.refresh(self)
        for k, v in data.items():
            if hasattr(self, k) and k != "id":
                setattr(self, k, v)
