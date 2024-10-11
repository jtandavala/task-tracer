from src.task.commands.concrete.add_task_command import AddTaskCommand
from src.task.invoker.task_invoker import TaskInvoker
from src.task.receiver.task_receiver import TaskReceiver


class TestTaskInvoker:
    def test_create_new_task(self, connection, migrations):
        task_dto = {"description": "test"}
        add_task_command = AddTaskCommand(TaskReceiver(connection), task_dto)
        invoker = TaskInvoker()
        task = invoker.execute_command(add_task_command)
        assert task == 1
