import pytest
from pydantic import ValidationError

from src.task.commands.concrete.add_task_command import AddTaskCommand
from src.task.receiver.task_receiver import TaskReceiver


class TestAddTaskCommand:
    def test_create_task(self, connection, migrations):
        task_dto = {"description": "test"}
        command = AddTaskCommand(TaskReceiver(connection), task_dto)
        result = command.execute()

        assert result is not None
        assert result == 1

    def test_throw_exception_when_invalid_description(
        self, connection, migrations
    ):
        task_dto = {"description": None}
        with pytest.raises(ValidationError) as e:
            command = AddTaskCommand(TaskReceiver(connection), task_dto)
            command.execute()
        assert isinstance(e.value, ValidationError)
