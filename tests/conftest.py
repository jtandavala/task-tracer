import pytest

from shared.infrastructure.service.database import DatabaseConnection
from shared.util.func import setup_database
from task.infrastructure.task_sql_queries import create_tasks_table


@pytest.fixture(scope="function")
def connection():
    db_conn = DatabaseConnection(":memory:")
    with db_conn.get_connection() as conn:
        yield conn
        conn.close()


@pytest.fixture(scope="function")
def migrations(connection):
    tables = create_tasks_table
    setup_database(connection, tables)
