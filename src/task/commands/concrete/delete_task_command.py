from uuid import UUID

from src.shared.commands.base import Command
from src.task.receiver.task_receiver import TaskReceiver


class DeleteTaskCommand(Command):
    def __init__(self, task_receiver: TaskReceiver, id: UUID):
        self.task_receiver = task_receiver
        self.id = id

    def execute(self):
        return self.task_receiver.delete_task(self.id)
