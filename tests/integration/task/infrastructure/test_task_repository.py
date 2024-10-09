from uuid import UUID

from src.task.domain.entity import Task
from src.task.infrastructure.task_repository import TaskSqlAlchemyRepository


class TestTaskAlchemyRepository:
    def test_create_new_task(self, db_session):
        task = Task(description="test")
        repository = TaskSqlAlchemyRepository(db_session)
        result = repository.save(task)
        assert isinstance(task.id, UUID) is True
        assert task.description == result.description
