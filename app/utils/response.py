# -*- coding: utf-8 -*-
# @Date: 2021/2/7 5:11 PM
# @Author: nilei
# @Email: nilei@datagrand.com
# @Company: datagrand

from typing import List

class CodeStatus:
    SUC = 2_00_00_00  # success
    ERR = 4_00_00_00  # client error
    EXC = 5_00_00_00  # internal exception


class CodeBusiness:
    DEFAULT = 0


class CodeOperation:
    DEFAULT = 0
    CREATE = 1_00
    READ = 2_00
    UPDATE = 3_00
    DELETE = 4_00
    RECREATE = 5_00
    SYNC = 6_00  # sync create task
    MISS = 7_00
    INVALID = 8_00
    REVOKE = 9_00
    EXPIRE = 10_00
    UPLOAD = 11_00


class CodeAny:
    DEFAULT = 0
    TASK = 1
    LIST = 2  # list page
    MQ = 3  # message queue
    SERVICE = 4  # downstream service
    JWT = 5  # json web token
    FILE = 6
    SCHEMA = 7  # marshmallow schema
    AUTH = 8  # user's auth
    LICENSE = 9  # datagrand license
    URL = 10  # request url
    MESSAGE = 11  # 提示信息


class Base:
    Code = CodeStatus.EXC + CodeBusiness.DEFAULT + CodeOperation.DEFAULT + CodeAny.DEFAULT
    Status = 500
    Message = '服务器内部错误或网络错误'

    def __init__(self, message=None):
        self.code = self.Code
        self.message = message if message else self.Message
        self.status = self.Status

    def asdict(self):
        return dict(code=self.Code, status=self.Status, message=getattr(self, 'message', self.Message))


class Response(Base):
    Code = CodeStatus.SUC + CodeBusiness.DEFAULT + CodeOperation.DEFAULT + CodeAny.DEFAULT
    Status = 200
    Message = '请求成功'

    def __init__(self, message=None):
        self.items = None
        self.total = None
        self.item = None
        self.data = None
        super().__init__(message)

    def set_item(self, item):
        self.item = item
        return self

    def set_data(self, data):
        self.data = data
        return self

    def set_items(self, items: List, total: int = None):
        self.items = items
        self.total = total if total is not None else len(items)
        return self

    def asdict(self):
        ret = super().asdict()
        if self.item is not None:
            ret['item'] = self.item
        elif self.items is not None:
            ret['items'] = self.items
            ret['total'] = self.total
        return ret


class ClientError(Base):
    Code = CodeStatus.ERR + CodeBusiness.DEFAULT + CodeOperation.DEFAULT + CodeAny.DEFAULT
    Status = 400
    Message = '请求参数错误'


class ServerException(Base):
    pass


class ExportSuccess(Response):
    Code = Response.Code + CodeOperation.CREATE
    Message = '导出成功'


class ExportFailed(Response):
    Code = ServerException.Code + CodeOperation.INVALID
    Message = '导出失败'


class CreateObjectSucceed(Response):
    Code = Response.Code + CodeOperation.CREATE
    Status = 201
    Message = '对象创建成功'


class CreateObjectFailed(ServerException):
    Code = ServerException.Code + CodeOperation.CREATE
    Message = '对象创建失败'


class GetObjectSucceed(Response):
    Code = Response.Code + CodeOperation.READ
    Message = '对象获取成功'


class GetObjectFailed(ServerException):
    Code = ServerException.Code + CodeOperation.READ
    Message = '对象获取失败'


class UpdateObjectSucceed(Response):
    Code = Response.Code + CodeOperation.UPDATE
    Message = '对象更新成功'


class UpdateObjectFailed(ServerException):
    Code = ServerException.Code + CodeOperation.UPDATE
    Message = '对象更新失败'


class DeleteObjectSucceed(Response):
    Code = Response.Code + CodeOperation.DELETE
    Message = '对象删除成功'


class DeleteObjectFailed(ServerException):
    Code = ServerException.Code + CodeOperation.DELETE
    Message = '对象删除失败'


class CreateTaskSucceed(CreateObjectSucceed):
    Code = CreateObjectSucceed.Code + CodeAny.TASK
    Message = '任务创建成功'


class CreateTaskFailed(CreateObjectFailed):
    Code = CreateObjectFailed.Code + CodeAny.TASK
    Message = '任务创建失败'


class CreateRetryTaskSucceed(Response):
    Code = Response.Code + CodeOperation.RECREATE + CodeAny.TASK
    Message = '重试任务创建成功'


class CreateRetryTaskFailed(ServerException):
    Code = ServerException.Code + CodeOperation.RECREATE + CodeAny.TASK
    Message = '重试任务创建失败'


class GetListSucceed(GetObjectSucceed):
    Code = GetObjectSucceed.Code + CodeAny.LIST
    Message = '列表获取成功'


class GetFileSucceed(GetObjectSucceed):
    Code = GetObjectSucceed.Code + CodeAny.LIST
    Message = '文件获取成功'

    def __init__(self, export_file_path):
        super().__init__()
        if not self.items:
            self.items = []
        self.export_file_path = export_file_path


class GetListWithInfoSucceed(GetObjectSucceed):
    Code = GetObjectSucceed.Code + CodeAny.LIST
    Message = '列表获取成功'

    def __init__(self, extra_info):
        super().__init__()
        if not self.items:
            self.items = []
        self.extra_info = extra_info


class GetListFailed(GetObjectFailed):
    Code = GetObjectFailed.Code + CodeAny.LIST
    Message = '列表获取失败'


class BulkDeleteSucceed(DeleteObjectSucceed):
    Code = DeleteObjectSucceed.Code + CodeAny.LIST
    Message = '批量删除对象成功'


class BulkDeleteFailed(DeleteObjectFailed):
    Code = DeleteObjectFailed.Code + CodeAny.LIST
    Message = '批量删除对象失败'


class BusinessLayerTimeout(ServerException):
    Code = ServerException.Code + CodeOperation.SYNC + CodeAny.TASK
    Message = '同步任务处理超时'


class MessageQueueException(ServerException):
    Code = ServerException.Code + CodeAny.MQ
    Message = '消息队列异常'


class MicroServiceException(ServerException):
    Code = ServerException.Code + CodeAny.SERVICE
    Message = '请求下游服务失败'


class FileNotFound(ServerException):
    Code = ServerException.Code + CodeOperation.READ + CodeAny.FILE
    Message = '文件未找到'


class TokenError(ClientError):
    Code = ClientError.Code + CodeAny.JWT
    Status = 401
    Message = '身份验证错误'


class MissingTokenError(TokenError):
    Code = TokenError.Code + CodeOperation.MISS
    Message = '未检测到 Authorization 请求头'


class InvalidTokenError(TokenError):
    Code = TokenError.Code + CodeOperation.INVALID
    Message = '身份验证信息格式错误'


class ExpiredTokenError(TokenError):
    Code = TokenError.Code + CodeOperation.EXPIRE
    Message = '身份验证信息已过期'


class RevokedTokenError(TokenError):
    Code = TokenError.Code + CodeOperation.REVOKE
    Message = '身份验证信息已失效'


class MarshMallowError(ClientError):
    Code = ClientError.Code + CodeOperation.INVALID + CodeAny.SCHEMA
    Status = 422
    Message = '参数校验出错'


class ForbiddenError(ClientError):
    Code = ClientError.Code + CodeOperation.INVALID + CodeAny.AUTH
    Status = 403
    Message = '用户未授权'


class ObjectNotFound(ClientError):
    Code = ClientError.Code + CodeOperation.MISS
    Status = 404
    Message = '对象未找到'


class LicenseError(ClientError):
    Code = ClientError.Code + CodeOperation.INVALID + CodeAny.LICENSE
    Message = '证书错误'


class URLNotFound(ClientError):
    Code = ClientError.Code + CodeOperation.INVALID + CodeAny.URL
    Status = 404
    Message = '请求路径错误'


class UploadFileFailed(ClientError):
    Code = ClientError.Code + CodeOperation.UPLOAD + CodeAny.FILE
    Message = '文件上传错误'


class SaveDocumentSucceed(Response):
    Code = Response.Code + CodeOperation.CREATE
    Message = '文件保存成功'


class SaveDocumentFailed(ServerException):
    Code = ServerException.Code + CodeOperation.CREATE
    Message = '文件保存失败'


class EditElementSucceed(Response):
    Code = Response.Code + CodeOperation.UPDATE
    Message = '编辑元素成功'


class EditElementFailed(ServerException):
    Code = ServerException.Code + CodeOperation.UPDATE
    Message = '编辑元素失败'


class RF:
    """
    response factory 工厂类 方便构造response
    """

    @staticmethod
    def success(data: any = None, message='请求成功', code: int = CodeStatus.SUC, status: int = 200):
        return dict(message=message, code=code, data=data, status=status)

    @staticmethod
    def success_item(item: any, message='请求成功', code: int = CodeStatus.SUC, status: int = 200):
        """
        构造item
        """
        return RF.success(dict(item=item), message, code, status)

    @staticmethod
    def success_items(items: list, total: int = None, message='请求成功', code: int = CodeStatus.SUC, status: int = 200):
        """
        构造items
        """
        return RF.success(dict(items=items, total=total or len(items)), message, code, status)

    @staticmethod
    def success_file(export_file_path: any = None, message='请求成功', code: int = CodeStatus.SUC, status: int = 200):
        """
        构造file_path
        """
        return RF.success(dict(export_file_path=export_file_path, items=[]), message, code, status)

    @staticmethod
    def failed(message='请求失败', code: int = CodeStatus.EXC, data: any = None, status: int = 500):
        return dict(message=message, code=code, data=data, status=status)

    @staticmethod
    def create_response(msg, status: int = None, item: any = None):
        """
        自定义返回对象 message status item
        注意此status 不是http status
        """
        res = Response(msg)
        if status:
            res.status = status
        if item:
            res.set_item(item)
        return res

    @staticmethod
    def create_object_succeed() -> CreateObjectSucceed:
        return CreateObjectSucceed()

    @staticmethod
    def get_file_succeed(file_path: str) -> GetFileSucceed:
        return GetFileSucceed(file_path)

    @staticmethod
    def get_object_succeed(item=None) -> GetObjectSucceed:
        return GetObjectSucceed().set_item(item)

    @staticmethod
    def update_object_succeed() -> UpdateObjectSucceed:
        return UpdateObjectSucceed()

    @staticmethod
    def delete_object_succeed() -> DeleteObjectSucceed:
        return DeleteObjectSucceed()

    @staticmethod
    def create_task_succeed() -> CreateTaskSucceed:
        return CreateTaskSucceed()

    @staticmethod
    def create_retry_task_succeed() -> CreateRetryTaskSucceed:
        return CreateRetryTaskSucceed()

    @staticmethod
    def get_list_succeed(items: List = None, total: int = None) -> GetListSucceed:
        return GetListSucceed().set_items(items, total)

    @staticmethod
    def get_list_with_info_succeed(extra_info: any = None, items: List = None,
                                   total: int = None) -> GetListWithInfoSucceed:
        return GetListWithInfoSucceed(extra_info).set_items(items, total)

    @staticmethod
    def bulk_delete_succeed() -> BulkDeleteSucceed:
        return BulkDeleteSucceed()


class EF:
    """
    error factory 工厂类 方便构造error
    """

    @staticmethod
    def file_not_found():
        return FileNotFound()

    @staticmethod
    def message_queue_exception():
        return MessageQueueException()

    @staticmethod
    def bulk_delete_failed():
        return BulkDeleteFailed()

    @staticmethod
    def micro_service_exception():
        return MicroServiceException()

    @staticmethod
    def business_layer_timeout():
        return BusinessLayerTimeout()

    @staticmethod
    def get_list_failed():
        return GetListFailed()

    @staticmethod
    def create_retry_task_failed():
        return CreateRetryTaskFailed()

    @staticmethod
    def create_task_failed(msg=None):
        res = CreateTaskFailed()
        if msg:
            res.Message = msg
        return res

    @staticmethod
    def delete_object_failed():
        return DeleteObjectFailed()

    @staticmethod
    def update_object_failed():
        return UpdateObjectFailed()

    @staticmethod
    def get_object_failed():
        return GetObjectFailed()

    @staticmethod
    def create_object_failed():
        return CreateObjectFailed()


