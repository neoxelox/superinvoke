from invoke import task
from rich.table import Table

from .. import constants, utils


@task(default=True)
def list(context):
    """List available enviroments."""
    from ..main import __ENVS__

    table = Table(show_header=True, header_style="bold white")
    table.add_column("Name", justify="left")
    table.add_column("Tags", style="dim", justify="right")

    for env in __ENVS__.All:
        table.add_row(
            f"[bold green3]{env.name}[/bold green3]" if env == __ENVS__.Current else env.name,
            ", ".join(env.tags),
        )

    constants.console.print("Listing [bold green3]current[/bold green3] and other enviroments:\n")
    constants.console.print(table)


@task(
    help={
        "enviroment": "Environment name to switch to. Example: dev",
    }
)
def switch(context, enviroment):
    """Switch current environment."""
    from ..main import __ENVS__

    new_env = __ENVS__.ByName(enviroment)
    old_env = __ENVS__.Current

    if not new_env:
        context.fail(f"{enviroment} is not a valid enviroment")

    if new_env == old_env:
        context.info(f"{enviroment} is already the current enviroment")
        return

    context.create(utils.path(constants.Paths.ENV), data=[new_env], dir=False)

    if new_env != __ENVS__.Current:
        context.fail(f"Cannot switch to enviroment {enviroment}")

    context.print(f"Switched to enviroment [green3]{new_env}[/green3] from {old_env}")
