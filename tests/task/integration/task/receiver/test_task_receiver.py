import pytest
from pydantic import ValidationError

from task.domain.entity import Task
from task.domain.value_objects.status import Status
from task.infrastructure.task_repository import TaskSqliteRepository
from task.receiver.task_receiver import TaskReceiver


class TestTaskReceiver:
    def test_create_task(self, connection, migrations):
        task_dto = {"description": "test"}
        task_receiver = TaskReceiver(connection)
        result = task_receiver.add_task(task_dto)
        assert result == 1

    def test_throw_exception_when_creating_task_with_invalid_uuid(self, connection, migrations):
        task_dto = {"id": "fake id", "description": "test"}
        with pytest.raises(ValidationError) as e:
            task_receiver = TaskReceiver(connection)
            task_receiver.add_task(task_dto)

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
            receiver = TaskReceiver(connection)
            receiver.add_task(task_dto)

        validation_error = e.value
        assert isinstance(validation_error, ValidationError)

        errors = validation_error.errors()

        assert len(errors) > 0
        assert errors[0]["loc"] == ("description",)
        assert "Input should be a valid string" in errors[0]["msg"]
        assert errors[0]["type"] == "string_type"

    def test_update_task(self, connection, migrations):
        task_dto = {"description": "test"}
        task = Task(**task_dto)
        repository = TaskSqliteRepository(connection)
        task.id = repository.save(task)

        found = repository.get_by_id(task.id)

        assert isinstance(found.id, int) is True
        assert found.id == task.id
        assert found.description == task.description
        assert found.status == Status.TODO
        assert found.created_at == task.created_at
        assert found.updated_at == task.updated_at

        task_receiver = TaskReceiver(connection)
        task.status = Status.IN_PROGRESS.value

        task_receiver.update_task(task.__dict__)
        found = repository.get_by_id(task.id)

        assert found.id == task.id
        assert found.status == Status.IN_PROGRESS

    def test_throw_exception_on_update_with_invalid_uuid(self, connection, migrations):
        with pytest.raises(Exception) as e:
            task_dto = {"id": "fake id", "description": "test"}
            task_receiver = TaskReceiver(connection)
            task_receiver.update_task(task_dto)

        assert "Input should be a valid integer" in str(e.value)

    def test_return_not_found_message(self, connection, migrations):
        with pytest.raises(Exception) as e:
            task_dto = {
                "id": 5,
                "description": "test",
            }

            task_receiver = TaskReceiver(connection)
            task_receiver.update_task(task_dto)

        assert str(e.value) == "Task not found"

    def test_delete_task(self, connection, migrations):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        task_reciver = TaskReceiver(connection)

        task.id = repository.save(task)
        found = repository.get_by_id(task.id)

        assert isinstance(found.id, int) is True
        assert found.id == task.id
        assert found.description == task.description

        task_reciver.delete_task(found.id)
        found = repository.get_by_id(task.id)

        with pytest.raises(Exception) as e:
            task_reciver.delete_task(task.id)
        assert str(e.value) == "Task not found"
        assert found is None
