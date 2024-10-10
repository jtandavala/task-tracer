from sqlite3 import Connection
from uuid import UUID

from src.task.domain.entity import Task
from src.task.infrastructure.task_repository import TaskSqliteRepository


class TestTaskAlchemyRepository:
    def test_if_we_have_connection(self, connection):
        assert isinstance(connection, Connection)

    def test_create_new_task(self, connection, migrations):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        result = repository.save(task)

        assert isinstance(task.id, UUID) is True
        assert result is not None

    def test_find_task_by_id(self, connection, migrations):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        repository.save(task)

        found = repository.get_by_id(task.id)

        assert isinstance(found.id, UUID) is True
        assert found.description == task.description
        assert found.status == task.status
        assert found.created_at == task.created_at
        assert found.updated_at == task.updated_at

    def test_return_nonde_when_passing_invalid_uuid(
        self, connection, migrations
    ):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        repository.save(task)

        found = repository.get_by_id("fake id")

        assert found is None
