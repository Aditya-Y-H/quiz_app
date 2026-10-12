from typing import Any
from sqlalchemy.pool import ConnectionPoolEntry


def set_sqlite_pragma(
    dbapi_connection: Any,
    _: ConnectionPoolEntry,
) -> None:
    """
    Enable foreign-key enforcement for SQLite connections.

    :param Any dbapi_connection: The database connection object.
    :param ConnectionPoolEntry _: A placeholder for the connection pool entry (not used).
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
