from flask import Flask
from sqlalchemy import event

from config import Config, TestConfig
from extensions import db, migrate
from logger import logger_debug_init, logger_init
from events import set_sqlite_pragma

from quiz_app.cli import seed


def create_app(test=False):
    app = Flask(__name__)

    if not test:
        app.config.from_object(Config)
        logger_init(app)
    else:
        app.config.from_object(TestConfig)
        logger_debug_init(app)

    db.init_app(app)
    with app.app_context():
        engine = db.engine
        if engine.dialect.name == "sqlite":
            event.listen(
                engine,
                "connect",
                set_sqlite_pragma,
            )

    migrate.init_app(app, db)

    app.cli.add_command(seed)

    from quiz_app import routes

    app.register_blueprint(routes.bp)

    from quiz_app import models

    return app
