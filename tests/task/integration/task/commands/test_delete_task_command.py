import pytest

from task.commands.concrete.add_task_command import AddTaskCommand
from task.commands.concrete.delete_task_command import DeleteTaskCommand
from task.domain.entity import Task
from task.queries.task_query_by_id import TaskQueryById
from task.receiver.task_receiver import TaskReceiver


class TestDeleteTaskCommand:
    def test_delete_task(self, connection, migrations):
        task = Task(description="test")

        command = AddTaskCommand(TaskReceiver(connection), task.__dict__)
        task.id = command.execute()

        query = TaskQueryById(connection, task.id)
        found = query.execute()

        assert isinstance(found.id, int) is True
        assert found.id == task.id

        delete_command = DeleteTaskCommand(TaskReceiver(connection), task.id)
        delete_command.execute()

        with pytest.raises(Exception) as e:
            found = query.execute()
        assert str(e.value) == "Task not found"
