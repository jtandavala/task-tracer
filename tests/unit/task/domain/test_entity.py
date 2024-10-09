import unittest
from datetime import datetime
from uuid import UUID

from pydantic import ValidationError

from src.task.domain.entity import Task
from src.task.domain.value_objects.status import Status


class TestTaskUnit(unittest.TestCase):
    def test_create_task(self):
        task = Task(description="test", status=Status.IN_PROGRESS)

        self.assertTrue(isinstance(task.id, UUID))
        self.assertEqual(task.description, "test")
        self.assertEqual(task.status, Status.IN_PROGRESS)
        self.assertTrue(isinstance(task.created_at, datetime))
        self.assertTrue(isinstance(task.updated_at, datetime))

    def test_add_default_status(self):
        task = Task(description="Test")

        self.assertTrue(isinstance(task.id, UUID))
        self.assertEqual(task.description, "Test")
        self.assertEqual(task.status, Status.TODO)

    def test_throw_exception_when_invalid_description(self):
        with self.assertRaises(ValidationError) as e:
            Task(status=Status.DONE)
        self.assertTrue(isinstance(e.exception, ValidationError))
