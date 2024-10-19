from datetime import datetime

import pytest
from pydantic import ValidationError

from task.commands.concrete.add_task_command import AddTaskCommand
from task.commands.concrete.delete_task_command import DeleteTaskCommand
from task.commands.concrete.update_task_command import UpdateTaskCommand
from task.domain.entity import Task
from task.domain.value_objects.status import Status
from task.invoker.task_invoker import TaskInvoker
from task.queries.task_query import TaskQuery
from task.queries.task_query_by_id import TaskQueryById
from task.receiver.task_receiver import TaskReceiver


class TestTaskInvoker:
    def test_create_new_task(self, connection, migrations):
        task_dto = {"description": "test"}
        add_task_command = AddTaskCommand(TaskReceiver(connection), task_dto)
        invoker = TaskInvoker()
        task = invoker.execute_command(add_task_command)
        assert task == 1

    def test_throw_exception_when_creating_with_invalid_description(self, connection, migrations):
        task_dto = {"description": None}
        invoker = TaskInvoker()
        with pytest.raises(ValidationError) as e:
            add_task_command = AddTaskCommand(TaskReceiver(connection), task_dto)
            invoker.execute_command(add_task_command)

        validation_error = e.value
        errors = validation_error.errors()

        assert len(errors) > 0
        assert errors[0]["loc"] == ("description",)
        assert errors[0]["msg"] == "Input should be a valid string"
        assert errors[0]["type"] == "string_type"

    def test_throw_exception_when_creating_with_invalid_uuid(self, connection, migrations):
        task_dto = {"id": "fake id", "description": "test"}
        invoker = TaskInvoker()

        with pytest.raises(ValidationError) as e:
            add_task_command = AddTaskCommand(TaskReceiver(connection), task_dto)
            invoker.execute_command(add_task_command)

        validation_error = e.value
        assert isinstance(validation_error, ValidationError)

        errors = validation_error.errors()

        assert len(errors) > 0
        assert errors[0]["loc"] == ("id",)
        assert "Input should be a valid integer" in errors[0]["msg"]
        assert errors[0]["type"] == "int_parsing"

    def test_list_tasks(self, connection, migrations):
        task_dto = {"description": "test"}
        add_task_command = AddTaskCommand(TaskReceiver(connection), task_dto)
        invoker = TaskInvoker()
        invoker.execute_command(add_task_command)

        task_query = TaskQuery(connection)
        tasks = invoker.execute_command(task_query)

        assert len(tasks.items) == 1
        assert tasks.page == 1
        assert tasks.per_page == 5
        assert isinstance(tasks.items[0].id, int) is True
        assert tasks.items[0].description == task_dto["description"]
        assert tasks.items[0].status == Status.TODO
        assert isinstance(tasks.items[0].created_at, datetime) is True
        assert isinstance(tasks.items[0].updated_at, datetime) is True

    def test_returning_empty_list(self, connection, migrations):
        invoker = TaskInvoker()
        task_query = TaskQuery(connection)

        tasks = invoker.execute_command(task_query)

        assert len(tasks.items) == 0
        assert tasks.items == []

    def test_list_tasks_with_done_status(self, connection, migrations):
        invoker = TaskInvoker()
        task1 = Task(description="test")
        task2 = Task(description="test", status=Status.DONE)
        add_task_command1 = AddTaskCommand(TaskReceiver(connection), task1.__dict__)
        add_task_command2 = AddTaskCommand(TaskReceiver(connection), task2.__dict__)

        task1.id = invoker.execute_command(add_task_command1)
        task2.id = invoker.execute_command(add_task_command2)

        task_query = TaskQuery(connection, filter=Status.DONE)
        tasks = invoker.execute_command(task_query)

        assert len(tasks.items) == 1
        assert tasks.page == 1
        assert tasks.per_page == 5
        assert isinstance(tasks.items[0].id, int) is True
        assert tasks.items[0].description == task2.description
        assert tasks.items[0].status == Status.DONE
        assert isinstance(tasks.items[0].created_at, datetime) is True
        assert isinstance(tasks.items[0].updated_at, datetime) is True

    def test_list_tasks_with_todo_status(self, connection, migrations):
        invoker = TaskInvoker()
        task1 = Task(description="test")
        task2 = Task(description="test", status=Status.DONE)
        add_task_command1 = AddTaskCommand(TaskReceiver(connection), task1.__dict__)
        add_task_command2 = AddTaskCommand(TaskReceiver(connection), task2.__dict__)

        task1.id = invoker.execute_command(add_task_command1)
        task2.id = invoker.execute_command(add_task_command2)

        task_query = TaskQuery(connection, filter=Status.TODO)
        tasks = invoker.execute_command(task_query)

        assert len(tasks.items) == 1
        assert tasks.page == 1
        assert tasks.per_page == 5
        assert isinstance(tasks.items[0].id, int) is True
        assert tasks.items[0].description == task1.description
        assert tasks.items[0].status == Status.TODO
        assert isinstance(tasks.items[0].created_at, datetime) is True
        assert isinstance(tasks.items[0].updated_at, datetime) is True

    def test_list_tasks_with_in_progress_status(self, connection, migrations):
        invoker = TaskInvoker()
        task1 = Task(description="test")
        task2 = Task(description="test", status=Status.IN_PROGRESS)
        add_task_command1 = AddTaskCommand(TaskReceiver(connection), task1.__dict__)
        add_task_command2 = AddTaskCommand(TaskReceiver(connection), task2.__dict__)

        task1.id = invoker.execute_command(add_task_command1)
        task2.id = invoker.execute_command(add_task_command2)

        task_query = TaskQuery(connection, filter=Status.IN_PROGRESS)
        tasks = invoker.execute_command(task_query)

        assert len(tasks.items) == 1
        assert tasks.page == 1
        assert tasks.per_page == 5
        assert isinstance(tasks.items[0].id, int) is True
        assert tasks.items[0].description == task1.description
        assert tasks.items[0].status == Status.IN_PROGRESS
        assert isinstance(tasks.items[0].created_at, datetime) is True
        assert isinstance(tasks.items[0].updated_at, datetime) is True

    def test_update_a_given_task(self, connection, migrations):
        task = Task(description="test")
        invoker = TaskInvoker()
        add_task_command = AddTaskCommand(TaskReceiver(connection), task.__dict__)
        task.id = invoker.execute_command(add_task_command)

        task_query = TaskQueryById(connection, task.id)
        found = invoker.execute_command(task_query)

        assert isinstance(found.id, int) is True
        assert found.id == task.id
        assert found.description == task.description
        assert found.status == Status.TODO
        assert found.created_at == task.created_at
        assert found.updated_at == task.updated_at

        task.status = Status.IN_PROGRESS
        update_command = UpdateTaskCommand(TaskReceiver(connection), task.__dict__)
        invoker.execute_command(update_command)

        found = invoker.execute_command(task_query)

        assert found.id == task.id
        assert found.status == Status.IN_PROGRESS
        assert found.created_at == task.created_at
        assert found.updated_at != task.updated_at

    def test_return_not_found_message(self, connection, migrations):
        task_dto = {
            "id": 33,
            "description": "test",
        }
        invoker = TaskInvoker()

        with pytest.raises(Exception) as e:
            update_command = UpdateTaskCommand(TaskReceiver(connection), task_dto)
            invoker.execute_command(update_command)

        assert str(e.value) == "Task not found"

    def test_throw_exception_when_update_with_invalid_id(self, connection, migrations):
        task_dto = {"id": "fake id", "description": "test"}
        invoker = TaskInvoker()

        with pytest.raises(ValidationError) as e:
            update_command = UpdateTaskCommand(TaskReceiver(connection), task_dto)
            invoker.execute_command(update_command)

        validation_error = e.value
        assert isinstance(validation_error, ValidationError)

        errors = validation_error.errors()

        assert len(errors) > 0
        assert errors[0]["loc"] == ("id",)
        assert "Input should be a valid integer" in errors[0]["msg"]
        assert errors[0]["type"] == "int_parsing"

    def test_delete_a_give_task(self, connection, migrations):
        task = Task(description="test")
        invoker = TaskInvoker()

        add_task_command = AddTaskCommand(TaskReceiver(connection), task.__dict__)
        task.id = invoker.execute_command(add_task_command)

        task_query = TaskQueryById(connection, task.id)
        found = invoker.execute_command(task_query)

        assert isinstance(found.id, int) is True
        assert found.id == task.id
        assert found.status == task.status

        delete_command = DeleteTaskCommand(TaskReceiver(connection), task.id)
        invoker.execute_command(delete_command)

        with pytest.raises(Exception) as e:
            invoker.execute_command(task_query)

        assert str(e.value) == "Task not found"
