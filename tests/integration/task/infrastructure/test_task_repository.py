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

    def test_return_none_when_passing_invalid_uuid(
        self, connection, migrations
    ):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        repository.save(task)

        found = repository.get_by_id("fake id")

        assert found is None

    def test_update_task(self, connection, migrations):
        description_updated = "update description"
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        repository.save(task)

        task.description = description_updated
        repository.update(task)
        updated = repository.get_by_id(task.id)

        assert isinstance(updated.id, UUID) is True
        assert updated.id == task.id
        assert updated.description == description_updated
        assert updated.created_at == task.created_at
        assert updated.updated_at != task.updated_at

    def test_delete_task(self, connection, migrations):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        repository.save(task)

        found = repository.get_by_id(task.id)

        assert isinstance(found.id, UUID) is True
        assert found.id == task.id
        assert found.description == task.description
        assert found.status == task.status
        assert found.created_at == task.created_at
        assert found.updated_at == task.updated_at

        repository.delete(task.id)

        found = repository.get_by_id(task.id)

        assert found is None

    def test_listing_tasks(self, connection, migrations):
        task1 = Task(description="task 1")
        task2 = Task(description="test 2")
        repository = TaskSqliteRepository(connection)
        repository.save(task1)
        repository.save(task2)

        tasks = repository.list()

        assert len(tasks.items) == 2
        assert tasks.page == 1
        assert tasks.per_page == 5
        assert isinstance(tasks.items[0].id, UUID) is True
        assert tasks.items[0].description == task1.description
