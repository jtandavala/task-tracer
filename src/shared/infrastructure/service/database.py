import sqlite3
from contextlib import contextmanager


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
