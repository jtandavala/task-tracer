from uuid import UUID

import pytest
from pydantic import ValidationError

from src.task.commands.concrete.add_task_command import AddTaskCommand
from src.task.commands.concrete.update_task_command import UpdateTaskCommand
from src.task.domain.entity import Task
from src.task.domain.value_objects.status import Status
from src.task.queries.task_query_by_id import TaskQueryById
from src.task.receiver.task_receiver import TaskReceiver


class TestUpdateTaskCommand:
    def test_update_task(self, connection, migrations):
        task = Task(description="test")

        command = AddTaskCommand(TaskReceiver(connection), task.__dict__)
        command.execute()

        query = TaskQueryById(connection, task.id)
        found = query.execute()

        assert isinstance(found.id, UUID) is True
        assert found.id == task.id
        assert found.status == Status.TODO

        task.status = Status.IN_PROGRESS
        command = UpdateTaskCommand(TaskReceiver(connection), task.__dict__)
        command.execute()

        found = query.execute()

        assert found.id == task.id
        assert found.status == Status.IN_PROGRESS

    def test_throw_exception_update_task_with_invalid(
        self, connection, migrations
    ):
        with pytest.raises(ValidationError) as e:
            command = UpdateTaskCommand(
                TaskReceiver(connection),
                {"id": "fake id", "description": "test"},
            )
            command.execute()
            validation_error = e.value
            assert isinstance(validation_error, ValidationError)

            errors = validation_error.errors()

            assert len(errors) > 0
            assert errors[0]["loc"] == ("id",)
            assert "Input should be a valid UUID" in errors[0]["msg"]
            assert errors[0]["type"] == "uuid_parsing"

    def test_return_not_found_message(self, connection, migrations):
        with pytest.raises(Exception) as e:
            command = UpdateTaskCommand(
                TaskReceiver(connection),
                {
                    "id": "a5388723-5698-43af-9d32-88c1d43af4ba",
                    "description": "test",
                },
            )
            command.execute()

        assert str(e.value) == "Task not found"
