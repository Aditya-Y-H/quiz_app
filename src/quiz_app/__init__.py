from flask import Flask

from config import Config, TestConfig
from extensions import db, migrate
from logger import logger_debug_init, logger_init


def create_app(test=False):
    app = Flask(__name__)

    if not test:
        app.config.from_object(Config)
        logger_init(app)
    else:
        app.config.from_object(TestConfig)
        logger_debug_init(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from quiz_app import routes

    app.register_blueprint(routes.bp)

    from quiz_app import models

    return app
