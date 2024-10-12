import click


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
