from datetime import datetime

from sqlalchemy import TIMESTAMP, UUID, Column, String, Table
from sqlalchemy.orm import registry


class Task:
    def __init__(
        self, id, description, status, created_at=None, updated_at=None
    ):
        self.id = id
        self.description = description
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self):
        return f"<Task(id={self.id}, description={self.description}, \
        status={self.status})>"


mapper_registry = registry()

tasks = Table(
    "tasks",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("description", String(255)),
    Column("status", String(30)),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow),
)


def start_mappers():
    mapper_registry.map_imperatively(Task, tasks)
