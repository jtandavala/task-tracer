from typing import Optional

from src.task.infrastructure.task_repository import TaskSqliteRepository


class TaskQuery:
    def __init__(self, session):
        self.repository = TaskSqliteRepository(session)

    def execute(
        self,
        filter: Optional[str] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 5,
    ):
        return self.repository.list(filter, page, per_page)
