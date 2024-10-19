import os

import click

from src.shared.infrastructure.service.database import DatabaseConnection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "src/data", "db.sqlite")
database = DatabaseConnection(DATABASE)

# with database.get_connection() as conn: # type: ignore
#     cli = TaskCli(conn)


@click.group()
def cli():
    """
    Task Tracer CLI

    This CLI allows you to manage tasks such as creating, updating, listing,
    and deleting tasks. Each command corresponds to an action you can perform
    on a task in the Task App.

    Example usage:

    $ task add --description "Finish homework" --status "in-progress"\n
    $ task list \n
    $ task update --id 123 --description "Complete project"\n
    $ task delete --id 123
    """
    pass


@cli.command()
@click.argument("description")
def add(description):
    """
    This command allows you to add a new task to your task manager.

    Args:\n
        description (str): The description of the task you want to add. It should be a brief text describing the task.

    Example: \n
        $ task-cli add "Buy groceries"\n
        Task 'Buy groceries' added successfully!

    If no description is provided, the task will not be added, and you will
    see an error message.

    """
    """ with database.get_connection() as conn:
        pass """
    click.echo(DATABASE)


@cli.command()
@click.argument("id")
@click.argument("description")
def update(id, description):
    """
    This command allows you to update the description of an existing task
    by providing its unique ID and a new description.

    Args:\n
        id (int): The unique identifier (ID) of the task you want to update.\n
        description (str): The new description for the task. It should brief text describing the task.

    Example:\n
        $ task-cli 1 "Buy groceries"\n
        Task with ID '1' updated to 'Buy groceries'!

    If the task with the provided ID does not exist, you will receive an error
    message indicating that the update failed.

    """
    click.echo(f"{id} - {description}")


@cli.command()
@click.argument("id")
def delete(id):
    """
    Delete an existing task by its unique ID.

    This command removes a task from the task list by specifying its
    unique identifier. Once deleted, the task cannot be recovered.

    Args:\n
        id (int): The unique identifier  of the task you want to delete.\n

    Example:\n
        $ task-cli delete 1\n
        Task with ID '1' deleted successfully.\n

    If the task with the provided ID does not exist, you will receive an
    error message indicating that the deletion failed.

    Warnings:\n
        Be cautious when using this command as it will permanently delete the task.
    """
    click.echo("Deleted")


@cli.command()
@click.option("--page", "-p", default=1, help="Page number for pagination.")
@click.option("--per_page", "-pr", default=5, help="Number of tasks to display per page.")
@click.option("--done", "-d", is_flag=True, help="List tasks with 'done' status.")
@click.option("--todo", "-f", is_flag=True, help="List tasks with 'todo' status.")
@click.option(
    "--in-progress",
    "-i",
    is_flag=True,
    help="List tasks with 'in-progress' status.",
)
def list(page, per_page, done, todo, in_progress):
    """
    List tasks with optional filters and pagination.

    This command lists tasks based on their status ('done', 'todo', or 'in-progress')
    and allows you to paginate through them. You can specify which page and how
    many tasks to show per page.

    Options:\n
        --page, -p: The page number to display (default is 1).\n
        --per_page, -pr: The number of tasks to show per page (default is 5).\n
        --done, -d: If set, lists only tasks that are marked as 'done'.\n
        --todo, -f: If set, lists only tasks that are marked as 'todo'.\n
        --in-progress, -i: If set, lists only tasks that are marked as 'in-progress'.\n

    Example usage:\n
        $ task-cli list --page 2 --per_page 10 --done
        Displays the second page of tasks, 10 tasks per page, filtered by 'done' status.

    If no filter is provided, it will list all tasks. Pagination allows you to
    control the number of tasks displayed at once, improving readability.

    Notes:\n
        - Only one status filter can be used at a time (e.g., --done, --todo, or --in-progress).\n
        - If multiple filters are provided, the first one encountered will be used.\n

    """
    pass


@cli.command()
@click.argument("id")
def mark_in_progress():
    """
    Mark a task as 'in progress' by its unique ID.

    This command updates the status of a task to 'in progress',
    allowing you to track tasks that are currently being worked on.

    Args:\n
        id (int): The unique identifier  of the task to be marked as 'in progress'.

    Example:\n
        $ task-cli mark-in-progress 1\n
        Task with ID '1' marked as 'in progress'.\n

    If the task with the provided ID does not exist, you will receive an
    error message indicating that the update failed.

    Notes:\n
        This action does not affect tasks with completed or canceled status.
        It only marks tasks that are pending or not yet started.

    Warnings:\n
        Ensure the task is in a valid state before marking it as 'in progress'.
    """


@cli.command()
@click.argument("id")
def mark_done():
    """
    Mark a task as 'done' by its unique ID.

    This command updates the status of a task to 'done', indicating that the task
    has been completed successfully.

    Args:\n
        id (str): The unique identifier  of the task to be marked as 'done'.

    Example:\n
        $ task-cli mark-done 1\n
        Task with ID '1' marked as 'done'.\n

    If the task with the provided ID does not exist, you will receive an
    error message indicating that the task could not be found or updated.

    Notes:\n
        This action is final and cannot be undone. Once a task is
        marked as 'done',
        it is considered completed.

    Warnings:\n
        Ensure that the task is actually completed before marking it as 'done'.
    """
    click.echo("Done")


if __name__ == "__main__":
    cli()
