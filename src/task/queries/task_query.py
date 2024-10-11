from typing import Optional

from src.shared.commands.base import Command
from src.task.infrastructure.task_repository import TaskSqliteRepository


class TaskQuery(Command):
    def __init__(
        self,
        session,
        filter: Optional[str] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 5,
    ):
        self.filter = filter
        self.page = page
        self.per_page = per_page
        self.repository = TaskSqliteRepository(session)

    def execute(self):
        return self.repository.list(self.filter, self.page, self.per_page)
