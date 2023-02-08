"""
Created on 2020年2月7日

@author: jianzhihua
"""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from configs import sysconf
from . import app

app.logger.debug("MYSQL_CONNECT_URL: " + sysconf.SQLALCHEMY_DATABASE_URI)

app.config["SQLALCHEMY_DATABASE_URI"] = sysconf.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_BINDS"] = dict(db=sysconf.SQLALCHEMY_DATABASE_URI)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

if sysconf.USE_DB_POOL:
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = sysconf.SQLALCHEMY_ENGINE_OPTIONS

db = SQLAlchemy()
db.init_app(app)
session = db.session
migrate = Migrate(app, db, compare_type=True, compare_server_default=True)
