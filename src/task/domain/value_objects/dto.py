from typing import List, Optional

from pydantic import BaseModel

from task.domain.entity import Task


class TaskDto:
    id: Optional[str]
    description: Optional[str]
    status: Optional[str]


class TaskPaginationResult(BaseModel):
    page: int
    per_page: int
    items: List[Task]
