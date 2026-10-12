from sqlalchemy import inspect

from extensions import db


def test_migrations_build_current_schema(app, runner):
    result = runner.invoke(args=["db", "upgrade"])

    assert result.exit_code == 0, result.output

    with app.app_context():
        inspector = inspect(db.engine)
        tables = set(inspector.get_table_names())
        assert {"users", "decks", "questions", "alembic_version"} <= tables

        deck_columns = {
            column["name"]: column for column in inspector.get_columns("decks")
        }
        assert "slug" in deck_columns
        assert deck_columns["user_id"]["nullable"] is True
