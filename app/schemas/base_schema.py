from typing import Tuple

from marshmallow import EXCLUDE, Schema, fields, pre_load
from marshmallow_sqlalchemy import ModelConverter as _ModelConverter
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.convert import _set_meta_kwarg


class ModelConverter(_ModelConverter):

    def _get_field_kwargs_for_property(self, prop):
        kwargs = super(ModelConverter, self)._get_field_kwargs_for_property(prop)
        if hasattr(prop, "comment") and 'description' not in kwargs:
            _set_meta_kwarg(kwargs, "description", prop.comment)
        return kwargs


class RawBaseSchema(Schema):

    class Meta:
        strict = True
        datetimeformat = "%Y-%m-%d %H:%M:%S"
        unknown = EXCLUDE


class BaseSchema(SQLAlchemyAutoSchema):

    class Meta:
        strict = True
        datetimeformat = "%Y-%m-%d %H:%M:%S"
        unknown = EXCLUDE

    create_time = fields.DateTime(dump_only=True)
    last_update_time = fields.DateTime(dump_only=True)


class PageMixin:
    """Usage

    class SomeSchema(BaseSchema, PageMixin):
        ...

    data = SomeSchema.load(dict(page=0, size=10))
    print(data['limit'], data['offset'])
    """
    page = fields.Int(missing=1, validate=lambda x: x > 0, load_only=True)
    size = fields.Int(missing=10, validate=lambda x: x > 0, load_only=True)

    def load(self, data, *args, **kwargs):
        data = super().load(data, *args, **kwargs)

        limit, offset = self.page_to_limit(data["page"], data["size"])
        data["limit"] = limit
        data["offset"] = offset
        return data

    @staticmethod
    def page_to_limit(page: int, size: int) -> Tuple[int, int]:
        limit = size
        offset = (page - 1) * size
        return limit, offset


class StrToListMixin:
    """Usage
    class SomeSchema(BaseSchema, StrToListMixin):
        _str_fields = ("some_ids", )

        some_ids = fields.List(fields.Int)


    print(SomeSchema().load({'some_ids': '1,2,3,4'}))
    {
        "some_ids": [1, 2, 3, 4]
    }
    """
    _str_fields: tuple = ()
    _delimiter = ","

    @pre_load
    def str_to_list(self, data, *args, **kwargs):
        """这个方法会将ImmuneMulDict转为MulDict"""
        data = data.copy()
        for field in self._str_fields:
            if field in data:
                value = data[field]
                if isinstance(value, (str, bytes)):
                    try:
                        data[field] = data[field].split(self._delimiter)
                    except Exception as e:
                        print(e)
                        continue
        return data
