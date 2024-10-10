from src.task.receiver.task_receiver import TaskReceiver


class TestTaskReceiver:
    def test_create_task(self, connection, migrations):
        task_dto = {"description": "test"}
        task_receiver = TaskReceiver(connection)
        result = task_receiver.add_task(task_dto)
        assert result == 1
