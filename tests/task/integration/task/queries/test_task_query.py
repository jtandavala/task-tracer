from task.domain.entity import Task
from task.domain.value_objects.status import Status
from task.infrastructure.task_repository import TaskSqliteRepository
from task.queries.task_query import TaskQuery


class TestTaskQuery:
    def test_list_tasks(self, connection, migrations):
        task1 = Task(description="task 1")
        task2 = Task(description="task 2")

        repository = TaskSqliteRepository(connection)
        task1.id = repository.save(task1)
        task2.id = repository.save(task2)

        query = TaskQuery(connection, page=1, per_page=1)

        tasks = query.execute()
        assert len(tasks.items) == 1
        assert tasks.page == 1
        assert tasks.per_page == 1
        assert isinstance(tasks.items[0].id, int) is True
        assert tasks.items[0].id == task1.id
        assert tasks.items[0].description == task1.description
        assert tasks.items[0].status == task1.status
        assert tasks.items[0].created_at == task1.created_at
        assert tasks.items[0].updated_at == task1.updated_at

    def test_list_tasks_with_default_parameters(self, connection, migrations):
        task1 = Task(description="task 1")
        task2 = Task(description="task 2")

        repository = TaskSqliteRepository(connection)
        task1.id = repository.save(task1)
        task2.id = repository.save(task2)

        query = TaskQuery(connection)

        tasks = query.execute()
        assert len(tasks.items) == 2
        assert tasks.page == 1
        assert tasks.per_page == 5
        assert isinstance(tasks.items[0].id, int) is True
        assert tasks.items[0].id == task1.id
        assert tasks.items[0].description == task1.description
        assert tasks.items[0].status == task1.status
        assert tasks.items[0].created_at == task1.created_at
        assert tasks.items[0].updated_at == task1.updated_at

    def test_list_tasks_with_done_status(self, connection, migrations):
        task1 = Task(description="task 1", status=Status.DONE)
        task2 = Task(description="task 2")

        repository = TaskSqliteRepository(connection)
        task1.id = repository.save(task1)
        task2.id = repository.save(task2)

        query = TaskQuery(connection, filter=Status.DONE.value)

        tasks = query.execute()
        assert len(tasks.items) == 1
        assert tasks.page == 1
        assert tasks.per_page == 5
        assert isinstance(tasks.items[0].id, int) is True
        assert tasks.items[0].id == task1.id
        assert tasks.items[0].description == task1.description
        assert tasks.items[0].status == task1.status
        assert tasks.items[0].created_at == task1.created_at
        assert tasks.items[0].updated_at == task1.updated_at

    def test_list_tasks_with_todo_status(self, connection, migrations):
        task1 = Task(description="task 1", status=Status.DONE)
        task2 = Task(description="task 2")

        repository = TaskSqliteRepository(connection)
        task1.id = repository.save(task1)
        task2.id = repository.save(task2)

        query = TaskQuery(connection, filter=Status.TODO.value)

        tasks = query.execute()
        assert len(tasks.items) == 1
        assert tasks.page == 1
        assert tasks.per_page == 5
        assert isinstance(tasks.items[0].id, int) is True
        assert tasks.items[0].id == task2.id
        assert tasks.items[0].description == task2.description
        assert tasks.items[0].status == task2.status
        assert tasks.items[0].created_at == task2.created_at
        assert tasks.items[0].updated_at == task2.updated_at

    def test_list_tasks_with_in_progress_status(self, connection, migrations):
        task1 = Task(description="task 1", status=Status.IN_PROGRESS)
        task2 = Task(description="task 2")

        repository = TaskSqliteRepository(connection)
        task1.id = repository.save(task1)
        task2.id = repository.save(task2)

        query = TaskQuery(connection, filter=Status.IN_PROGRESS.value)

        tasks = query.execute()
        assert len(tasks.items) == 1
        assert tasks.page == 1
        assert tasks.per_page == 5
        assert isinstance(tasks.items[0].id, int) is True
        assert tasks.items[0].id == task1.id
        assert tasks.items[0].description == task1.description
        assert tasks.items[0].status == task1.status
        assert tasks.items[0].created_at == task1.created_at
        assert tasks.items[0].updated_at == task1.updated_at

    def test_return_empty_list(self, connection, migrations):
        query = TaskQuery(connection)
        tasks = query.execute()

        assert len(tasks.items) == 0
        assert tasks.page == 1
        assert tasks.per_page == 5
        assert tasks.items == []
