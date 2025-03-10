import unittest
from datetime import datetime

from pydantic import ValidationError

from task.domain.entity import Task
from task.domain.value_objects.status import Status


class TestTaskUnit(unittest.TestCase):
    def test_create_task(self):
        task = Task(id=1, description="test", status=Status.IN_PROGRESS)

        self.assertTrue(isinstance(task.id, int))
        self.assertEqual(task.description, "test")
        self.assertEqual(task.status, Status.IN_PROGRESS)
        self.assertTrue(isinstance(task.created_at, datetime))
        self.assertTrue(isinstance(task.updated_at, datetime))

    def test_add_default_status(self):
        task = Task(id=1, description="Test")

        self.assertTrue(isinstance(task.id, int))
        self.assertEqual(task.description, "Test")
        self.assertEqual(task.status, Status.TODO)

    def test_throw_exception_when_invalid_description(self):
        with self.assertRaises(ValidationError) as e:
            Task(status=Status.DONE)
        self.assertTrue(isinstance(e.exception, ValidationError))

    def test_update_task(self):
        task = Task(id=1, description="test")

        self.assertTrue(isinstance(task.id, int))
        self.assertEqual(task.description, "test")
        self.assertEqual(task.status, Status.TODO)
        self.assertTrue(isinstance(task.created_at, datetime))
        self.assertTrue(isinstance(task.updated_at, datetime))

        task.status = Status.IN_PROGRESS
        task.description = "task updated"

        self.assertEqual(task.description, "task updated")
        self.assertEqual(task.status, Status.IN_PROGRESS)
