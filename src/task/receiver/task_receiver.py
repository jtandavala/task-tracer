from sqlite3 import Connection

from pydantic import ValidationError

from src.task.domain.entity import Task
from src.task.infrastructure.task_repository import TaskSqliteRepository


class TaskReceiver:
    def __init__(self, session: Connection):
        self.session = session
        self.repository = TaskSqliteRepository(self.session)

    def add_task(self, task_data: Task):
        task = Task(**task_data)
        try:
            return self.repository.save(task)
        except ValidationError as e:
            raise e

    def update_task(self, task_data: Task):
        task = self.repository.get_by_id(task_data.id)
        if task is None:
            raise Exception("Task not found")
        return self.repository.update(task_data)
