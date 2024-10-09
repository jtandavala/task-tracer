import unittest

from pydantic import ValidationError

from src.shared.domain.entity import Entity
from src.task.domain.value_objects.status import Status


class StubEntity(Entity):
    description: str
    status: Status


class TestEntityUnit(unittest.TestCase):
    def test_create_entity(self):
        task = StubEntity(description="test", status=Status.TODO)
        self.assertEqual(task.description, "test")
        self.assertEqual(task.status, Status.TODO)

    def test_throw_exception_in_invalid_description(self):
        with self.assertRaises(ValidationError) as e:
            StubEntity(status=Status.TODO)
        self.assertTrue(isinstance(e.exception, ValidationError))
