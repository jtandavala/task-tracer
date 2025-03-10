from datetime import datetime

from task.app import TaskCli
from task.domain.entity import Task
from task.domain.value_objects.status import Status


class TestTaskCli:
    def test_create_new_task(self, connection, migrations):
        task_dto = {"description": "test"}
        task = TaskCli(connection)
        task_id = task.create_task(task_dto)

        assert isinstance(task_id, int) is True

    def test_throw_exception_on_create_with_invalid_description(self, connection, migrations):
        task_dto = {"description": None}
        cli = TaskCli(connection)
        task = cli.create_task(task_dto)

        assert str(task) == "invalid input"

    def test_find_task_by_id(self, connection, migrations):
        cli = TaskCli(connection)
        task_id = cli.create_task({"description": "test"})

        task: Task = cli.find_by_id(task_id)

        assert isinstance(task.id, int) is True
        assert task.id == task_id
        assert task.description == "test"
        assert task.status == Status.TODO
        assert isinstance(task.created_at, datetime) is True
        assert isinstance(task.updated_at, datetime) is True

    def test_can_update_task(self, connection, migrations):
        task_dto = {"description": "test"}
        cli = TaskCli(connection)
        task_id = cli.create_task(task_dto)

        task_dto["id"] = task_id
        task_dto["description"] = "test updated"

        cli.update_task(task_dto)

        task: Task = cli.find_by_id(task_id)

        assert isinstance(task.id, int) is True
        assert task.id == task_id
        assert task.description == task_dto["description"]
        assert task.status == Status.TODO
        assert isinstance(task.created_at, datetime) is True
        assert isinstance(task.updated_at, datetime) is True

    def test_delete_task(self, connection, migrations):
        task_dto = {"description": "test"}
        cli = TaskCli(connection)
        task_id = cli.create_task(task_dto)

        task: Task = cli.find_by_id(task_id)

        assert isinstance(task.id, int) is True
        assert task.id == task_id
        assert task.description == "test"

        cli.delete_task(task_id)

        task = cli.find_by_id(task_id)
        assert str(task) == "Task not found"
