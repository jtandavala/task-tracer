from enum import Enum


class Status(str, Enum):
    """
    An enumeration representing task statuses.

    This class defines three status values for tasks:
    - TODO: Indicates a task that has not been started yet.
    - IN_PROGRESS: Represents a task currently being worked on.
    - DONE: Signifies a completed task.

    Attributes:
        TODO (str): The status for a task that has not been started yet.
        IN_PROGRESS (str): The status for a task currently in progress.
        DONE (str): The status for a completed task.

    Examples:
        >>> Status.TODO
        'todo'
        >>> str(Status.IN_PROGRESS)
        'in-progress'
        >>> Status.DONE.value
        'done'

    Notes:
        This class inherits from both str and Enum, allowing it to be used as \
        both a string and an enumeration.
        It provides type safety and autocompletion benefits while maintaining \
        string-like behavior.
    """

    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"

    @staticmethod
    def get_default():
        return Status.TODO
