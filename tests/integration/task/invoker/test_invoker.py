from datetime import datetime
from uuid import UUID

from src.task.commands.concrete.add_task_command import AddTaskCommand
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
