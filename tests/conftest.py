import pytest

from src.shared.infrastructure.service.database import DatabaseConnection


@pytest.fixture(scope="session")
def db_connection():
    db_conn = DatabaseConnection()
    db_conn.setup("sqlite:///:memory:")
    yield db_conn
    db_conn.teardown()


@pytest.fixture
def db_session(db_connection):
    return db_connection.create_session()
