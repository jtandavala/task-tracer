from src.task.commands.concrete.add_task_command import AddTaskCommand
from src.task.domain.value_objects.dto import TaskDto
from src.task.invoker.task_invoker import TaskInvoker
from src.task.queries.task_query_by_id import TaskQueryById
from src.task.receiver.task_receiver import TaskReceiver


class TaskCli:
    def __init__(self, connection):
        self.connection = connection
        self.invoker = TaskInvoker()

    def create_task(self, task_dto: TaskDto):
        add_task_command = AddTaskCommand(TaskReceiver(self.connection), task_dto)
        return self.invoker.execute_command(add_task_command)

    def find_by_id(self, id: int):
        try:
            query = TaskQueryById(self.connection, id)
            return query.execute()
        except Exception as e:
            return e.value
