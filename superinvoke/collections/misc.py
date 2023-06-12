from importlib import metadata

from invoke import task


@task(variadic=True)
def help(context, collection):
    """Show available commands."""
    context.run(f"invoke --list {collection}")


@task
def version(context):
    """Show superinvoke version."""
    context.print(f"Superinvoke: v{metadata.version('superinvoke')}")
    context.print(f"Invoke (neoxelox fork): v{metadata.version('neoxelox-invoke')}")
