from uuid import UUID

from src.shared.commands.base import Command
from src.task.infrastructure.task_repository import TaskSqliteRepository


class TaskQueryById(Command):
    def __init__(self, session, id: UUID):
        self.repository = TaskSqliteRepository(session)
        self.id = id

    def execute(self):
        if not isinstance(self.id, UUID) or self.id is None:
            raise Exception("id must be a valid UUID")
        task = self.repository.get_by_id(self.id)
        if task is None:
            raise Exception("Task not found")
        return task
