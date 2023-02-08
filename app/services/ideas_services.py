import datetime
from typing import List, Optional, Tuple

from models import commit
from models.ideas_model import IdeasModel
from utils.constant.idea_enum import StateEnum


class IdeasService:

    @staticmethod
    def get_ideas_list(limit: int = 10,
                       offset: int = 0,
                       title: str = None,
                       is_done: bool = None,
                       start_time=None,
                       end_time=None,
                       **kwargs) -> Tuple[int, List["IdeaEntity"]]:
        count, query_list = IdeasModel.get_by_filter(
            limit=limit,
            offset=offset,
            title=title,
            is_done=is_done,
            create_time=(start_time, end_time),
        )
        return count, query_list

    @staticmethod
    def get_an_idea(_id: int, ) -> Optional["IdeaEntity"]:
        idea = IdeasModel.get_by_id(_id)
        if not idea:
            return None
        return idea

    @staticmethod
    @commit
    def create_an_idea(
        title: str,
        text: str = "",
        level: int = StateEnum.normal.value,
    ):
        idea = IdeasModel.create(
            title=title,
            text=text,
            level=level,
        )
        return idea

    @staticmethod
    @commit
    def update_an_idea(_id: int, **data) -> Optional["IdeaEntity"]:
        idea = IdeasModel.update(_id, **data)
        if not idea:
            return None
        return idea

    @staticmethod
    @commit
    def delete_an_idea(_id: int):
        IdeasModel.delete(_id)
        return _id

    @classmethod
    def get_overtimed_ideas(cls, gap: int = 24 * 60 * 60) -> List["IdeaEntity"]:
        """获取超过 $gap 秒未完成的任务

        :param gap: 获取超过n秒的任务，默认一天
        """
        end_time = datetime.datetime.now() - datetime.timedelta(seconds=gap)
        ideas = IdeasModel.get_all_by_filter(create_time=(None, end_time), is_done=False)
        return ideas

    @classmethod
    def send_mail_task(cls, tasks_list: List[dict]):
        from tasks.send_overtime_message import send_message
        send_message.delay(tasks_list)
