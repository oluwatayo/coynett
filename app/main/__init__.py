import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from raven.contrib.flask import Sentry

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

s_dsn = os.getenv('SENTRY_DSN')
sentry = Sentry(dsn=s_dsn)


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    sentry.init_app(app)
    flask_bcrypt.init_app(app)

    return app
