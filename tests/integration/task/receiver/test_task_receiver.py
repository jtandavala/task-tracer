import pytest
from pydantic import ValidationError

from src.task.receiver.task_receiver import TaskReceiver


class TestTaskReceiver:
    def test_create_task(self, connection, migrations):
        task_dto = {"description": "test"}
        task_receiver = TaskReceiver(connection)
        result = task_receiver.add_task(task_dto)
        assert result == 1

    def test_throw_exception_when_creating_task_with_invalid_uuid(
        self, connection, migrations
    ):
        task_dto = {"id": "fake id", "description": "test"}
        with pytest.raises(ValidationError) as e:
            task_receiver = TaskReceiver(connection)
            task_receiver.add_task(task_dto)

        validation_error = e.value
        assert isinstance(validation_error, ValidationError)

        errors = validation_error.errors()

        assert len(errors) > 0
        assert errors[0]["loc"] == ("id",)
        assert "Input should be a valid UUID" in errors[0]["msg"]
        assert errors[0]["type"] == "uuid_parsing"
