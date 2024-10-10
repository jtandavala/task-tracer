from src.shared.commands.base import Command


class AddTaskCommand(Command):
    def __init__(self, task_receiver, task_data):
        self.task_receiver = task_receiver
        self.task_data = task_data

    def execute(self):
        return self.task_reciever.add_task(self.task_data)
