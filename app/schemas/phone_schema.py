from marshmallow.validate import OneOf
from marshmallow_sqlalchemy import auto_field
from marshmallow import fields
from .base_schema import RawBaseSchema


class PhoneNormalApproveSchema(RawBaseSchema):
    docId = fields.Integer(required=True)
    employeeId = fields.Integer(required=True)
    forwardIds = fields.List(fields.Integer(required=True))

class PhoneFinalApproveSchema(RawBaseSchema):
    docId = fields.Integer(required=True)
    employeeId = fields.Integer(required=True)

class PhoneRejectSchema(RawBaseSchema):
    docId = fields.Integer(required=True)
    employeeId = fields.Integer(required=True)