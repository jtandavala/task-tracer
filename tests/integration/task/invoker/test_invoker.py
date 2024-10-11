from datetime import datetime
from uuid import UUID

from src.task.commands.concrete.add_task_command import AddTaskCommand
from src.task.domain.entity import Task
from src.task.domain.value_objects.status import Status
from src.task.invoker.task_invoker import TaskInvoker
from src.task.queries.task_query import TaskQuery
from src.task.receiver.task_receiver import TaskReceiver


class TestTaskInvoker:
    def test_create_new_task(self, connection, migrations):
        task_dto = {"description": "test"}
        add_task_command = AddTaskCommand(TaskReceiver(connection), task_dto)
        invoker = TaskInvoker()
        task = invoker.execute_command(add_task_command)
        assert task == 1

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
        assert isinstance(tasks.items[0].id, UUID) is True
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
        add_task_command1 = AddTaskCommand(
            TaskReceiver(connection), task1.__dict__
        )
        add_task_command2 = AddTaskCommand(
            TaskReceiver(connection), task2.__dict__
        )

        invoker.execute_command(add_task_command1)
        invoker.execute_command(add_task_command2)

        task_query = TaskQuery(connection, filter=Status.DONE)
        tasks = invoker.execute_command(task_query)

        assert len(tasks.items) == 1
        assert tasks.page == 1
        assert tasks.per_page == 5
        assert isinstance(tasks.items[0].id, UUID) is True
        assert tasks.items[0].description == task2.description
        assert tasks.items[0].status == Status.DONE
        assert isinstance(tasks.items[0].created_at, datetime) is True
        assert isinstance(tasks.items[0].updated_at, datetime) is True

    def test_list_tasks_with_todo_status(self, connection, migrations):
        invoker = TaskInvoker()
        task1 = Task(description="test")
        task2 = Task(description="test", status=Status.DONE)
        add_task_command1 = AddTaskCommand(
            TaskReceiver(connection), task1.__dict__
        )
        add_task_command2 = AddTaskCommand(
            TaskReceiver(connection), task2.__dict__
        )

        invoker.execute_command(add_task_command1)
        invoker.execute_command(add_task_command2)

        task_query = TaskQuery(connection, filter=Status.TODO)
        tasks = invoker.execute_command(task_query)

        assert len(tasks.items) == 1
        assert tasks.page == 1
        assert tasks.per_page == 5
        assert isinstance(tasks.items[0].id, UUID) is True
        assert tasks.items[0].description == task1.description
        assert tasks.items[0].status == Status.TODO
        assert isinstance(tasks.items[0].created_at, datetime) is True
        assert isinstance(tasks.items[0].updated_at, datetime) is True
