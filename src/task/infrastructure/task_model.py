from datetime import datetime

from sqlalchemy import TIMESTAMP, UUID, Column, String, Table
from sqlalchemy.orm import registry

from src.task.domain.entity import Task

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
