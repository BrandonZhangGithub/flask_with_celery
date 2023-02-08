from marshmallow import fields
from .base_schema import RawBaseSchema


class CreateTaskSchema(RawBaseSchema):
    employeeId = fields.Integer(required=True)
    docId = fields.Integer(required=True)

class JumpDatagrandHomeSchema(RawBaseSchema):
    employeeId = fields.Integer(required=True)


class SyncCallBackSchema(RawBaseSchema):
    update_date = fields.String(required=False, missing='', default='')
    increase = fields.String(required=False, missing='', default='')