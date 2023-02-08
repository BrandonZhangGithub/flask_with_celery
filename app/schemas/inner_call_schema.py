from marshmallow import fields
from .base_schema import RawBaseSchema


class DraftFileNameSchema(RawBaseSchema):
    file_id = fields.Integer(required=True)