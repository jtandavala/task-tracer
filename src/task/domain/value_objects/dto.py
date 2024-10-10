from typing import List

from pydantic import BaseModel

from src.task.domain.entity import Task


class TaskPaginationResult(BaseModel):
    page: int
    per_page: int
    items: List[Task]
