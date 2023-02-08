import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from app import app as _app

os.environ["MYSQL_DATABASE"] = "test"

# _app.extensions["sqlalchemy"].db.drop_all()
with _app.app_context():
    _app.extensions["sqlalchemy"].db.drop_all()
    _app.extensions["sqlalchemy"].db.create_all()


@pytest.fixture(scope="session")
def app():
    return _app


@pytest.yield_fixture(scope="session")
def app_ctx(app):
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def session(app):
    return app.extensions["sqlalchemy"].db.session
