from src.task.commands.concrete.add_task_command import AddTaskCommand
from src.task.receiver.task_receiver import TaskReceiver


class TestAddTaskCommand:
    def test_create_task(self, connection, migrations):
        task_dto = {"description": "test"}
        command = AddTaskCommand(TaskReceiver(connection), task_dto)
        result = command.execute()
        assert result == 1
