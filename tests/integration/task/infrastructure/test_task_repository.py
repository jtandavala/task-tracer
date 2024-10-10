from sqlite3 import Connection

from src.task.domain.entity import Task
from src.task.infrastructure.task_repository import TaskSqliteRepository


class TestTaskAlchemyRepository:
    def test_if_we_have_connection(self, connection):
        assert isinstance(connection, Connection)

    def test_create_new_task(self, connection, migrations):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        result = repository.save(task)
        assert result is not None
