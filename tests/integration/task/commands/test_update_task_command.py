from uuid import UUID

from src.task.commands.concrete.update_task_command import UpdateTaskCommand
from src.task.domain.entity import Task
from src.task.domain.value_objects.status import Status
from src.task.infrastructure.task_repository import TaskSqliteRepository
from src.task.queries.task_query_by_id import TaskQueryById
from src.task.receiver.task_receiver import TaskReceiver


class TestUpdateTaskCommand:
    def test_update_task(self, connection, migrations):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        repository.save(task)

        query = TaskQueryById(connection)
        found = query.execute(task.id)

        assert isinstance(found.id, UUID) is True
        assert found.id == task.id
        assert found.status == Status.TODO

        task.status = Status.IN_PROGRESS
        command = UpdateTaskCommand(TaskReceiver(connection), task)
        command.execute()

        found = query.execute(task.id)

        assert found.id == task.id
        assert found.status == Status.IN_PROGRESS
