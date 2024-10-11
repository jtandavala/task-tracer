from src.shared.commands.base import Command
from src.task.domain.value_objects.dto import TaskDto
from src.task.receiver.task_receiver import TaskReceiver


class UpdateTaskCommand(Command):
    def __init__(self, task_receiver: TaskReceiver, task_dto: TaskDto):
        self.task_receiver = task_receiver
        self.task_dto = task_dto

    def execute(self):
        return self.task_receiver.update_task(self.task_dto)
