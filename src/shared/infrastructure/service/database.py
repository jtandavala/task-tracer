import sqlite3
from contextlib import contextmanager

from shared.util.func import setup_database
from task.infrastructure.task_sql_queries import create_tasks_table


class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        try:
            conn.row_factory = sqlite3.Row
            yield conn
        finally:
            conn.close()

    def run_migrations(self, conn):
        tables = create_tasks_table
        setup_database(conn, tables)
