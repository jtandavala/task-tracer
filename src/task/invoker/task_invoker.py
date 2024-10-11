from src.shared.commands import Command


class TaskInvoker:
    def __init__(self):
        self._history = []

    def execute_command(self, command: Command):
        return command.execute()
        # self._history.append(command)

    def undo_last_command(self):
        if self._history:
            # command = self._history.pop()
            # command.undo()
            pass
