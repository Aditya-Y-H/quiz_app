import pytest

from quiz_app import create_app
from extensions import db as _db


@pytest.fixture(scope="session")
def app():
    app = create_app(test=True)
    with app.app_context():
        yield app


@pytest.fixture
def db(app):
    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
