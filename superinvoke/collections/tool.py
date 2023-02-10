import os
import stat
import tempfile

from invoke import task
from rich.table import Table

from .. import constants, utils


def has_tool_version(context, tool):
    with constants.console.status(f"Gathering [cyan]{tool.name}[/cyan] version"):
        return context.has(tool, version=tool.version)


@task(default=True)
def list(context):
    """List available tools."""
    from ..main import __TOOLS__

    table = Table(show_header=True, header_style="bold white")
    table.add_column("Name", justify="left")
    table.add_column("Version", justify="right")
    table.add_column("Tags", style="dim", justify="right")

    for tool in __TOOLS__.All:
        table.add_row(
            tool.name,
            f"[bold green3]{tool.version}[/bold green3]"
            if has_tool_version(context, tool)
            else f"[bold red1]{tool.version}[/bold red1]",
            ", ".join(tool.tags),
        )

    constants.console.print(
        "Listing [bold green3]installed[/bold green3] and [bold red1]not installed[/bold red1] tools:\n"
    )
    constants.console.print(table)


@task(variadic=True)
def run(context, args):
    """Execute an available tool."""
    from ..main import __TOOLS__

    tool_name, args = utils.next_arg(args)
    tool = __TOOLS__.ByName(tool_name)

    if not tool:
        context.fail(f"{tool_name} is not a valid tool")
    tool = tool[0]

    install(context, include=tool.name, exclude="", yes=False)

    context.run(f"{tool} {args}")


@task(
    help={
        "include": "Tags, globs or tool names that will be installed. Example: ops,golang-migrate,*...",
        "exclude": "Tags, globs or tool names that will be excluded. Example: golangci-lint,ci,dev*...",
        "yes": "Automatically say yes to all prompts.",
    }
)
def install(context, include, exclude="", yes=False):
    """Install available tools."""
    from ..main import __TOOLS__

    include = {tool for tool in include.split(",") if tool and tool != ","}
    include_tools = set()
    for name_or_tag in include:
        include_tools.update(__TOOLS__.ByName(name_or_tag))
        include_tools.update(__TOOLS__.ByTag(name_or_tag))

    exclude = {tool for tool in exclude.split(",") if tool and tool != ","}
    exclude_tools = set()
    for name_or_tag in exclude:
        exclude_tools.update(__TOOLS__.ByName(name_or_tag))
        exclude_tools.update(__TOOLS__.ByTag(name_or_tag))

    tools = set()
    for tool in include_tools - exclude_tools:
        if tool._managed:
            if not has_tool_version(context, tool):
                tools.add(tool)
            else:
                context.info(f"{tool.name} already installed")
        else:
            context.info(f"{tool.name} not managed")

    if not tools:
        context.warn("No tools to install")
        return

    context.info(f"Tool(s) {', '.join([tool.name for tool in tools])} will be [bold green3]installed[/bold green3]")

    if not yes:
        answer = context.input("      Continue? Y/n: ").lower()
        if answer == "y":
            yes = True
        elif answer == "n":
            yes = False
        elif not answer:
            yes = True
        else:
            yes = False

    if not yes:
        context.exit()

    with tempfile.TemporaryDirectory() as TMP:
        TMP = utils.path(TMP)
        context.create(utils.path(constants.Paths.TOOLS), dir=True)

        for tool in tools:
            if not has_tool_version(context, tool):
                with constants.console.status(
                    f"Installing [cyan]{tool.name}[/cyan] ([green3]{tool.version}[/green3])"
                ) as _:
                    if tool.link is None:
                        context.fail(f"No link set for {tool.name} in platform {constants.Platforms.CURRENT}")
                    elif tool.link[1] != ".":
                        context.download(tool.link[0], utils.path(f"{TMP}/{tool.name}.tar.gz"))
                        context.extract(utils.path(f"{TMP}/{tool.name}.tar.gz"), utils.path(f"{TMP}/{tool.name}"))
                        context.move(utils.path(f"{TMP}/{tool.name}/{tool.link[1]}"), tool.path)
                    else:
                        context.download(tool.link[0], utils.path(f"{TMP}/{tool.name}"))
                        context.move(utils.path(f"{TMP}/{tool.name}"), tool.path)
                        os.chmod(tool.path, os.stat(tool.path).st_mode | stat.S_IEXEC)

                if has_tool_version(context, tool):
                    context.print(f"Installed [cyan]{tool.name}[/cyan] ([bold green3]{tool.version}[/bold green3])")
                else:
                    context.fail(f"Cannot install tool {tool.name}")
            else:
                context.info(f"{tool.name} already installed")


@task(
    help={
        "include": "Tags, globs or tool names that will be uninstalled. Example: ops,golang-migrate,*...",
        "exclude": "Tags, globs or tool names that will be excluded. Example: golangci-lint,ci,dev*...",
        "yes": "Automatically say yes to all prompts.",
    }
)
def remove(context, include, exclude="", yes=False):
    """Remove available tools."""
    from ..main import __TOOLS__

    include = {tool for tool in include.split(",") if tool and tool != ","}
    include_tools = set()
    for name_or_tag in include:
        include_tools.update(__TOOLS__.ByName(name_or_tag))
        include_tools.update(__TOOLS__.ByTag(name_or_tag))

    exclude = {tool for tool in exclude.split(",") if tool and tool != ","}
    exclude_tools = set()
    for name_or_tag in exclude:
        exclude_tools.update(__TOOLS__.ByName(name_or_tag))
        exclude_tools.update(__TOOLS__.ByTag(name_or_tag))

    tools = set()
    for tool in include_tools - exclude_tools:
        if tool._managed:
            if has_tool_version(context, tool):
                tools.add(tool)
            else:
                context.info(f"{tool.name} not installed")
        else:
            context.info(f"{tool.name} not managed")

    if not tools:
        context.warn("No tools to remove")
        return

    context.info(f"Tool(s) {', '.join([tool.name for tool in tools])} will be [bold red1]uninstalled[/bold red1]")

    if not yes:
        answer = context.input("      Continue? Y/n: ").lower()
        if answer == "y":
            yes = True
        elif answer == "n":
            yes = False
        elif not answer:
            yes = True
        else:
            yes = False

    if not yes:
        context.exit()

    for tool in tools:
        if has_tool_version(context, tool):
            with constants.console.status(f"Uninstalling [cyan]{tool.name}[/cyan] ([red1]{tool.version}[/red1])") as _:
                context.remove(tool)

            if not has_tool_version(context, tool):
                context.print(f"Uninstalled [cyan]{tool.name}[/cyan] ([bold red1]{tool.version}[/bold red1])")
            else:
                context.fail(f"Cannot uninstall tool {tool.name}")
        else:
            context.info(f"{tool.name} not installed")
