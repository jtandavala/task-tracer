from sqlite3 import Connection

from src.task.domain.entity import Task
from src.task.domain.value_objects.dto import TaskDto
from src.task.infrastructure.task_repository import TaskSqliteRepository


class TaskReceiver:
    def __init__(self, session: Connection):
        self.session = session
        self.repository = TaskSqliteRepository(self.session)

    def add_task(self, task_data: TaskDto):
        task = Task(**task_data)
        return self.repository.save(task)

    def update_task(self, task_data):
        # Logic to update task
        pass
