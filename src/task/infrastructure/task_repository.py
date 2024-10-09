from typing import List, Optional
from uuid import UUID

from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from src.task.domain.entity import Task
from src.task.domain.repository.task_repository import TaskRepository
from src.task.infrastructure.task_model import tasks


class TaskSqlAlchemyRepository(TaskRepository):
    def __init__(self, session):
        self.session = session

    def save(self, task: Task) -> Task:
        insert_stmt = insert(tasks).values(
            id=task.id,
            description=task.description,
            status=task.status,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
        try:
            self.session.execute(insert_stmt)
            self.session.commit()
            return task
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(e)

    def get_by_id(self, id: UUID) -> Task:
        raise NotImplementedError

    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    def update(self, task: Task) -> None:
        raise NotImplementedError

    def list(
        self,
        search: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Task]:
        raise NotImplementedError
