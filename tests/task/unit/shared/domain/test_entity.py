import unittest
from datetime import datetime
from typing import Optional

from pydantic import Field, ValidationError, constr

from shared.domain.entity import Entity
from task.domain.value_objects.status import Status


class StubEntity(Entity):
    id: Optional[int] = None
    description: constr(min_length=2, max_length=255)
    status: Status
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TestEntityUnit(unittest.TestCase):
    def test_create_entity(self):
        task = StubEntity(id=1, description="test", status=Status.TODO)
        self.assertTrue(isinstance(task.id, int))
        self.assertEqual(task.description, "test")
        self.assertEqual(task.status, Status.TODO)
        self.assertTrue(isinstance(task.created_at, datetime))
        self.assertTrue(isinstance(task.updated_at, datetime))

    def test_throw_exception_in_invalid_description(self):
        with self.assertRaises(ValidationError) as e:
            StubEntity(status=Status.TODO)
        self.assertTrue(isinstance(e.exception, ValidationError))
