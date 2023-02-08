import pytest
import time
from werkzeug.test import Client
from pytest import mark

from entities.ideas_entity import IdeaEntity


@mark.usefixtures("app", "client", "app_ctx")
class TestIdeaV2:

    def test_for_creation_v2(self, client):
        response = client.post("/api/v2/ideas", json=dict(title="title1", text="text1"))
        assert response.status_code == 201, response.json
        content = response.json["data"]
        assert content["title"] == "title1"
        assert content["text"] == "text1"
        return response.json["data"]["id"]

    def test_for_update_v2(self, client, app_ctx):
        self.reserver_record()
        time.sleep(1)
        response = client.put("/api/v2/ideas/1", json=dict(title="new_title", text="new_text"))
        assert response.status_code == 201
        content = response.json["data"]
        assert content["id"] == 1
        assert content["last_update_time"] > content["create_time"]
        assert content["title"] == "new_title"
        assert content["text"] == "new_text"

    def test_for_delete_v2(self, client, _id=1):
        response = client.delete(f"/api/v2/ideas/{_id}", )
        assert response.status_code == 204

        # read for success
        response = client.get(f"/api/v2/ideas/{_id}")
        response.status_code == 200
        response.json["data"] == ""

    def test_for_read_detail_v2(self, client, app_ctx):
        self.reserver_record()
        response = client.get("/api/v2/ideas/1")
        assert response.status_code == 200
        content = response.json
        assert content["data"]["id"] == 1

    def test_for_read_list_v2(self, client, app_ctx):
        _id = self.test_for_creation_v2(client)
        response = client.get("/api/v2/ideas", query_string=dict(title="title1", page=1, size=10))
        assert response.status_code == 200
        assert isinstance(response.json["data"]["items"], list)
        assert response.json["data"]["total"] == 1
        self.test_for_delete_v2(client, _id)
        response = client.get("/api/v2/ideas", query_string=dict(title="title1", page=1, size=10))
        assert response.status_code == 200
        assert isinstance(response.json["data"]["items"], list)
        assert response.json["data"]["total"] == 0

    def reserver_record(self):
        instance = IdeaEntity.query.get(1)
        instance.active = True
        IdeaEntity.query.session.commit()

    @pytest.mark.skip(msg="this test belongs to template itself")
    def test_for_new_model(self):
        from models.ideas_model import IdeasModel
        import datetime

        IdeasModel.bulk_delete_by_filter()

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        IdeasModel.bulk_create([{
            "title": "title1",
            "text": "text1",
            "create_time": now
        }, {
            "title": "title2",
            "text": "text2",
            "create_time": now
        }], )

        assert len(IdeasModel.get_all_by_filter(title="title")) == 2
        assert len(IdeasModel.get_all_by_filter(title="title", _filter_keys=["title"])) == 0
        assert len(IdeasModel.get_all_by_filter(text="text")) == 0  # 没有设置 filter_key, text 自动会成为 filter_key
        assert len(IdeasModel.get_all_by_filter(text="text", _like_filter_keys=["text"])) == 2  # 动态设置

        assert len(IdeasModel.get_all_by_filter(create_time=now, _filter_keys=["create_time"])) == 2  # 不会报错
        assert len(IdeasModel.get_all_by_filter(create_time=(now, now))) == 2  # 不会报错

        IdeasModel._filter_keys = ["title", "text"]  # 重新设置 _filter_keys

        assert len(IdeasModel.get_all_by_filter(text="text1")) == 1  # 精准查询可以命中
        assert len(IdeasModel.get_all_by_filter(text="text", _like_filter_keys=["text"])) == 2  # 命中模糊查询
        assert len(IdeasModel.get_all_by_filter(title="title1", text="text", _like_filter_keys=["text"])) == 1  # 原过滤条件任然生效
