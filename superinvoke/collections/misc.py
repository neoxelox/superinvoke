from invoke import task


@task(variadic=True)
def help(context, collection):
    """Show available commands."""
    context.run(f"invoke --list {collection}")
