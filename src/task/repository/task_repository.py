from abc import ABC, abstractclassmethod
from typing import List, Optional
from uuid import UUID

from src.task.domain.entity import Task


class TaskRepository(ABC):
    @abstractclassmethod
    def save(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractclassmethod
    def get_by_id(self, id: UUID) -> Task:
        raise NotImplementedError

    @abstractclassmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractclassmethod
    def update(self, task: Task) -> None:
        raise NotImplementedError

    def list(
        self,
        search: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Task]:
        raise NotImplementedError
