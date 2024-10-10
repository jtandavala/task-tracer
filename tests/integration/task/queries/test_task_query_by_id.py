from uuid import UUID

import pytest

from src.task.domain.entity import Task
from src.task.infrastructure.task_repository import TaskSqliteRepository
from src.task.queries.task_query_by_id import TaskQueryById


class TestTaskQueryById:
    def test_get_task_by_id(self, connection, migrations):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        repository.save(task)

        query = TaskQueryById(connection)
        found = query.execute(task.id)

        assert isinstance(found.id, UUID) is True
        assert found.id == task.id
        assert found.description == task.description
        assert found.status == task.status
        assert found.created_at == task.created_at
        assert found.updated_at == task.updated_at

    def test_return_not_found_message(self, connection, migrations):
        with pytest.raises(Exception) as e:
            query = TaskQueryById(connection)
            query.execute(UUID("5c0a22c4-530b-467e-b896-69d21bdd3cf0"))
        assert str(e.value) == "Task not found"

    def test_throw_exception_with_invalid_uuid(self, connection, migrations):
        with pytest.raises(Exception) as e:
            query = TaskQueryById(connection)
            query.execute("fake id")
        assert str(e.value) == "id must be a valid UUID"
