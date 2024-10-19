import pytest
from pydantic import ValidationError

from task.commands.concrete.add_task_command import AddTaskCommand
from task.receiver.task_receiver import TaskReceiver


class TestAddTaskCommand:
    def test_create_task(self, connection, migrations):
        task_dto = {"description": "test"}
        command = AddTaskCommand(TaskReceiver(connection), task_dto)
        result = command.execute()

        assert result is not None
        assert result == 1

    def test_throw_exception_when_invalid_uuid(self, connection, migrations):
        task_dto = {"id": "fake id", "description": "test"}

        with pytest.raises(ValidationError) as e:
            command = AddTaskCommand(TaskReceiver(connection), task_dto)
            command.execute()

        validation_error = e.value
        assert isinstance(validation_error, ValidationError)

        errors = validation_error.errors()

        assert len(errors) > 0
        assert errors[0]["loc"] == ("id",)
        assert "Input should be a valid integer" in errors[0]["msg"]
        assert errors[0]["type"] == "int_parsing"

    def test_throw_exception_when_invalid_description(self, connection, migrations):
        task_dto = {"description": None}
        with pytest.raises(ValidationError) as e:
            command = AddTaskCommand(TaskReceiver(connection), task_dto)
            command.execute()

        validation_error = e.value
        assert isinstance(validation_error, ValidationError)

        errors = validation_error.errors()
        assert len(errors) > 0
        assert errors[0]["loc"] == ("description",)
        assert errors[0]["msg"] == "Input should be a valid string"
        assert errors[0]["type"] == "string_type"
