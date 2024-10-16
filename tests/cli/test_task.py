from src.cli.task import TaskCli


class TestTaskCli:
    def test_create_new_task(self, connection, migrations):
        task_dto = {"description": "test"}
        task = TaskCli(connection)
        task_id = task.create_task(task_dto)

        assert isinstance(task_id, int) is True
