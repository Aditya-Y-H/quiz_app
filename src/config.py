import os
from datetime import timedelta


class Config:
    # Flask & Core Security
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret")
    DEBUG = os.environ.get("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///quiz_app.db")

    # Sessions
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_PERMANENT = os.environ.get("SESSION_PERMANENT", "True").lower() in (
        "true",
        "1",
        "yes",
    )
    SESSION_TYPE = os.environ.get("SESSION_TYPE", "filesystem")

    # File Uploads / Payload limits
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 25 * 1024 * 1024))


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
