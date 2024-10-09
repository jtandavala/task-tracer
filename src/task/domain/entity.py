from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field, constr

from src.shared.domain.entity import Entity
from src.task.domain.value_objects.status import Status


class Task(Entity):
    """
    Represents a task entity in the system.

    Attributes:
        id (UUID): Unique indentifier for the task.
        description (str): Brief description of the task
        created_at (datetime): Timestamp when the task was created.
        updated_at (datetime): Timestamp when the task was last updated.

    Notes:
        - The id is generated automatically using  UUID v4.
        - The description must be between 2 and 255 characters long.
        - The status defaults to the default status returned \
        by Status.get_default()
        - Both created_at and updated_at are automatically set \
        to the current time.

    Methods:
        __init__(description: str, status: Status = None) -> None:
            Initializes a new Task instance.

    Example usage:
        >>> task = Task(description="complete the report", \
        status=Status.IN_PROGRESS)
        >>> print(task.description)
        in-progress
        >>> print(task.created_at)
        2023-09-10 12:34:56.789012
    """

    id: UUID = Field(default_factory=uuid4)
    description: constr(min_length=2, max_length=255)
    status: Status = Field(default_factory=Status.get_default)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
