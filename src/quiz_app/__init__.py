from flask import Flask

from config import Config, TestConfig
from extensions import db, migrate


def create_app(test=False):
    app = Flask(__name__)

    if not test:
        app.config.from_object(Config)
    else:
        app.config.from_object(TestConfig)

    db.init_app(app)
    migrate.init_app(app, db)

    from quiz_app import routes

    app.register_blueprint(routes.bp)

    return app
