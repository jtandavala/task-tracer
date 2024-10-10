from src.shared.commands.base import Command
from src.task.domain.value_objects.dto import TaskDto
from src.task.receiver.task_receiver import TaskReceiver


class AddTaskCommand(Command):
    def __init__(self, task_reciever: TaskReceiver, task_data: TaskDto):
        self.task_reciever = task_reciever
        self.task_data = task_data

    def execute(self):
        return self.task_reciever.add_task(self.task_data)
