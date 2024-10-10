from sqlite3 import Connection
from typing import List, Optional
from uuid import UUID

from src.task.domain.entity import Task
from src.task.domain.repository.task_repository import TaskRepository


class TaskSqliteRepository(TaskRepository):
    def __init__(self, session: Connection):
        self.session = session

    def save(self, task: Task) -> Task:
        c = self.session.cursor()
        c.execute(
            "INSERT INTO tasks (id, description, status, \
            created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (
                str(task.id),
                task.description,
                task.status.value,
                task.created_at,
                task.updated_at,
            ),
        )
        self.session.commit()

        return c.lastrowid

    def get_by_id(self, id: UUID) -> Task:
        c = self.session.cursor()

        c.execute("SELECT * FROM tasks WHERE id = ?", (str(id),))
        row = c.fetchone()
        if row is not None:
            return Task(
                id=row[0],
                description=row[1],
                status=row[2],
                created_at=row[3],
                updated_at=row[4],
            )
        return None

    def delete(self, id: UUID) -> None:
        c = self.session.cursor()
        c.execute("DELETE FROM tasks WHERE id = ?", (str(id),))
        self.session.commit()
        return None

    def update(self, task: Task) -> None:
        c = self.session.cursor()
        c.execute(
            "UPDATE tasks set description=?, status=?, \
            updated_at= CURRENT_TIMESTAMP WHERE id = ?",
            (task.description, task.status, str(task.id)),
        )
        self.session.commit()
        return None

    def list(
        self,
        search: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Task]:
        raise NotImplementedError
