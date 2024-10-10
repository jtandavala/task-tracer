from uuid import UUID

from src.task.infrastructure.task_repository import TaskSqliteRepository


class TaskQueryById:
    def __init__(self, session):
        self.repository = TaskSqliteRepository(session)

    def execute(self, id: UUID):
        if not isinstance(id, UUID) or id is None:
            raise Exception("id must be a valid UUID")
        task = self.repository.get_by_id(id)
        if task is None:
            raise Exception("Task not found")
        return task
