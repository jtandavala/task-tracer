import unittest
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field, ValidationError, constr

from src.shared.domain.entity import Entity
from src.task.domain.value_objects.status import Status


class StubEntity(Entity):
    id: UUID = Field(default_factory=uuid4)
    description: constr(min_length=2, max_length=255)
    status: Status
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TestEntityUnit(unittest.TestCase):
    def test_create_entity(self):
        task = StubEntity(description="test", status=Status.TODO)
        self.assertTrue(isinstance(task.id, UUID))
        self.assertEqual(task.description, "test")
        self.assertEqual(task.status, Status.TODO)
        self.assertTrue(isinstance(task.created_at, datetime))
        self.assertTrue(isinstance(task.updated_at, datetime))

    def test_throw_exception_in_invalid_description(self):
        with self.assertRaises(ValidationError) as e:
            StubEntity(status=Status.TODO)
        self.assertTrue(isinstance(e.exception, ValidationError))
