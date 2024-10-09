import unittest
from datetime import datetime
from uuid import UUID

from src.task.domain.entity import Task
from src.task.domain.value_objects.status import Status


class TestTaskUnit(unittest.TestCase):
    def test_create_task(self):
        task = Task(description="test", status=Status.TODO)

        self.assertTrue(isinstance(task.id, UUID))
        self.assertEqual(task.description, "test")
        self.assertEqual(task.status, Status.TODO)
        self.assertTrue(isinstance(task.created_at, datetime))
        self.assertTrue(isinstance(task.updated_at, datetime))
