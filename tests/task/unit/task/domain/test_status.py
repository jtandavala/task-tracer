from task.domain.value_objects.status import Status


class TestStatus:
    def test_done_status(self):
        assert Status.DONE.value == "done"

    def test_in_progress_status(self):
        assert Status.IN_PROGRESS.value == "in-progress"

    def test_todo_status(self):
        assert Status.TODO.value == "todo"
