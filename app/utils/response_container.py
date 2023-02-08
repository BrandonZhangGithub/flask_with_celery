"""
新的返回格式，参考
http://wiki.datagrand.com/pages/viewpage.action?pageId=26709261

其中：
    - code    代表业务代码
    - status  保持真实有效的 status_code
    - message 请求成功
"""
from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass
class Base:

    def asdict(self):
        return asdict(self)


@dataclass
class BaseResponse(Base):
    code: int = 200
    status: int = 200
    message: str = "请求成功"
    data: Any = None

    __annotations__ = {
        "code": int,
        "status": int,
        "message": str,
        "data": Any,
    }


@dataclass
class ListData(Base):
    total: int
    items: List[Dict]

    __annotations__ = {
        "total": int,
        "items": List[Dict],
    }


@dataclass
class ListResponse(BaseResponse):
    data: ListData = ListData(0, [])

    __annotations__ = {
        "data": ListData,
    }


# if __name__ == "__main__":
#     import json
#     print(json.dumps(BaseResponse(data=dict()).asdict()))
#     print(json.dumps(ListResponse(data=ListData(total=0, items=[])).asdict()))
