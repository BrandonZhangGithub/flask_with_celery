from entities.ideas_entity import IdeaEntity
from .base_model import BaseModel


class IdeasModel(BaseModel[IdeaEntity]):
    # _entity = IdeaEntity  # 可以省略
    # _filter_keys = ["is_done"]

    _like_filter_keys = ["title"]
    _range_filter_keys = ["create_time"]
