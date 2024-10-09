from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field, constr

from src.shared.domain.entity import Entity
from src.task.domain.value_objects.status import Status


class Task(Entity):
    id: UUID = Field(default_factory=uuid4)
    description: constr(min_length=2, max_length=255)
    status: Status = Field(default_factory=Status.get_default)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
