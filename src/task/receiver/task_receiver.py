from sqlite3 import Connection
from uuid import UUID

from pydantic import ValidationError

from src.task.domain.entity import Task
from src.task.domain.value_objects.dto import TaskDto
from src.task.infrastructure.task_repository import TaskSqliteRepository


class TaskReceiver:
    def __init__(self, session: Connection):
        self.session = session
        self.repository = TaskSqliteRepository(self.session)

    def add_task(self, task_data: TaskDto):
        task = Task(**task_data)
        try:
            return self.repository.save(task)
        except ValidationError as e:
            raise e

    def update_task(self, task_data: TaskDto):
        task = Task(**task_data)
        try:
            item = self.repository.get_by_id(task.id)
            if item is None:
                raise Exception("Task not found")
            return self.repository.update(task)
        except ValidationError as e:
            raise e

    def delete_task(self, id: UUID):
        task = self.repository.get_by_id(id)
        if task is None:
            raise Exception("Task not found")
        return self.repository.delete(id)
