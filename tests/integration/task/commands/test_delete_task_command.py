from uuid import UUID

import pytest

from src.task.commands.concrete.add_task_command import AddTaskCommand
from src.task.commands.concrete.delete_task_command import DeleteTaskCommand
from src.task.domain.entity import Task
from src.task.queries.task_query_by_id import TaskQueryById
from src.task.receiver.task_receiver import TaskReceiver


class TestDeleteTaskCommand:
    def test_delete_task(self, connection, migrations):
        task = Task(description="test")

        command = AddTaskCommand(TaskReceiver(connection), task.__dict__)
        command.execute()

        query = TaskQueryById(connection)
        found = query.execute(task.id)

        assert isinstance(found.id, UUID) is True
        assert found.id == task.id

        delete_command = DeleteTaskCommand(TaskReceiver(connection))
        delete_command.execute(task.id)

        with pytest.raises(Exception) as e:
            found = query.execute(task.id)
        assert str(e.value) == "Task not found"
