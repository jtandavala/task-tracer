import pytest

from task.domain.entity import Task
from task.infrastructure.task_repository import TaskSqliteRepository
from task.queries.task_query_by_id import TaskQueryById


class TestTaskQueryById:
    def test_get_task_by_id(self, connection, migrations):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        task.id = repository.save(task)

        query = TaskQueryById(connection, task.id)
        found = query.execute()

        assert isinstance(found.id, int) is True
        assert found.id == task.id
        assert found.description == task.description
        assert found.status == task.status
        assert found.created_at == task.created_at
        assert found.updated_at == task.updated_at

    def test_return_not_found_message(self, connection, migrations):
        with pytest.raises(Exception) as e:
            query = TaskQueryById(connection, 33)
            query.execute()
        assert str(e.value) == "Task not found"

    def test_throw_exception_with_invalid_uuid(self, connection, migrations):
        with pytest.raises(Exception) as e:
            query = TaskQueryById(connection, "fake id")
            query.execute()
        assert str(e.value) == "id must be a valid integer"
