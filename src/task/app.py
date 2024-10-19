from task.commands.concrete.add_task_command import AddTaskCommand
from task.commands.concrete.delete_task_command import DeleteTaskCommand
from task.commands.concrete.update_task_command import UpdateTaskCommand
from task.domain.value_objects.dto import TaskDto
from task.invoker.task_invoker import TaskInvoker
from task.queries.task_query_by_id import TaskQueryById
from task.receiver.task_receiver import TaskReceiver


class TaskCli:
    def __init__(self, connection):
        self.connection = connection
        self.invoker = TaskInvoker()

    def create_task(self, task_dto: TaskDto):
        try:
            add_task_command = AddTaskCommand(TaskReceiver(self.connection), task_dto)
            result = self.invoker.execute_command(add_task_command)
            return f"Task #{result} added"
        except Exception as e:
            print(e)
            return "invalid input"

    def find_by_id(self, id: int):
        try:
            query = TaskQueryById(self.connection, id)
            return self.invoker.execute_command(query)
        except Exception as e:
            return e

    def update_task(self, task_dto: TaskDto):
        try:
            update_task_command = UpdateTaskCommand(TaskReceiver(self.connection), task_dto)
            return self.invoker.execute_command(update_task_command)
        except Exception:
            return "something went wrong"

    def delete_task(self, id: int):
        try:
            delete_task_command = DeleteTaskCommand(TaskReceiver(self.connection), id)
            return self.invoker.execute_command(delete_task_command)
        except Exception:
            return "something went wrong"
