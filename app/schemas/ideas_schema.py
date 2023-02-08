from marshmallow.validate import OneOf
from marshmallow_sqlalchemy import auto_field
from marshmallow import fields

from .base_schema import RawBaseSchema


class SensitiveWordsSchema(RawBaseSchema):
    task_id = fields.Integer(required=True)

class DeleteResearchReportSchema(RawBaseSchema):
    docId = fields.Integer(required=True)

class FrontendMenuSchema(RawBaseSchema):
    appId = fields.Integer(required=True)

class RedirectTaskDetailSchema(RawBaseSchema):
    docId = fields.Integer(required=True)
    employeeId = fields.Integer(required=True)

class TaskWorkflowTransferSchema(RawBaseSchema):
    task_id = fields.Integer(required=True)
    forward_to_user_ids = fields.List(fields.Integer(), required=False, missing=[])
    flow_status = fields.Integer(required=True)
    customized = fields.Raw(required=True)

class ExportResearchReportSchema(RawBaseSchema):
    task_id = fields.Integer(required=True)
    file_name = fields.String(required=True)
    original_file_path = fields.String(required=True)

# 获取卡片
class TextBasicSchema(RawBaseSchema):
    file_id = fields.Integer(required=True)

# 研报时间schema
class PostResearchReportTimeSchema(RawBaseSchema):
    file_id = fields.Integer(required=True)
    date = fields.String(required=True)

class DeleteResearchReportTimeSchema(RawBaseSchema):
    file_id = fields.Integer(required=True)

class PutResearchReportTimeSchema(RawBaseSchema):
    file_id = fields.Integer(required=True)
    date = fields.String(required=True)