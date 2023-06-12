import fnmatch
import os
import sys
from typing import List, Literal, Optional

from invoke.context import Context

from .. import constants, utils


# Writes to stdout and flushes.
def print(message: str) -> None:
    constants.console.print(f"[default on default][not bold]{message}[/not bold][/default on default]")


# Reads from stdout.
def input(message: str) -> str:
    return constants.console.input(f"[default on default][not bold]{message}[/not bold][/default on default]")


# Terminates the current task immediately with an error.
def fail(message: Optional[str] = None) -> None:
    if message:
        constants.console.print(
            f"[bold red1]FAIL:[/bold red1] [default on default][not bold]{message}[/not bold][/default on default]"
        )
    sys.exit(1)


# Terminates the current task immediately without an error.
def exit(message: Optional[str] = None) -> None:
    if message:
        constants.console.print(
            f"[bold cyan]EXIT:[/bold cyan] [default on default][not bold]{message}[/not bold][/default on default]"
        )
    sys.exit(0)


# Prints to stdout and flushes.
def info(message: str) -> None:
    constants.console.print(
        f"[bold cyan]INFO:[/bold cyan] [default on default][not bold]{message}[/not bold][/default on default]"
    )


# Prints to stdout and flushes.
def warn(message: str) -> None:
    constants.console.print(
        f"[bold yellow]WARN:[/bold yellow] [default on default][not bold]{message}[/not bold][/default on default]"
    )


# Runs the specified command hiding its output, continuing if fails and returns stdout or stderr.
def attempt(context: Context, command: str) -> str:
    try:
        # TODO: If input is required fail directly
        result = context.run(command, warn=True, hide="both", pty=False)
    except Exception:
        return ""

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    return stdout or stderr


# Checks whether a certain version of a program is installed.
def has(context: Context, program: str, version: Optional[str] = None) -> bool:
    if version:
        version = f"*{version}*"
        return (  # noqa: BLK100
            fnmatch.fnmatchcase(context.attempt(f"{program} --version"), version)
            or fnmatch.fnmatchcase(context.attempt(f"{program} version"), version)
        )
    else:
        result = context.attempt(f"which {program}")
        return result and "not found" not in result


# Gets the root path of the current repository.
def repository(context: Context) -> str:
    return context.attempt("git rev-parse --show-toplevel")


# Gets the current commit hash.
def commit(context: Context) -> str:
    return context.attempt("git rev-parse --short HEAD")


# Gets the current branch name.
def branch(context: Context) -> str:
    return context.attempt("git rev-parse --abbrev-ref HEAD")


# Gets the current or latest commit tag if any.
def tag(context: Context, current: bool = True) -> Optional[str]:
    if current:
        result = context.attempt("git name-rev --name-only --tags HEAD").replace("^0", "")
    else:
        result = context.attempt("git describe --tags --abbrev=0").replace("^0", "")

    if not result or "undefined" in result or "fatal" in result:
        result = None

    return result


# Gets the N last file changed.
def changes(context: Context, scope: int = 1) -> List[str]:
    return context.attempt(f"git diff --name-only HEAD HEAD~{scope}").split("\n")


# TODO: CRUD for files and directories:
#               FILE    DIR
# - copy
# - move        X       X
# - create      X       X
# - remove      X       X
# - read        X       -
# - write
# - exists      X       X
# - extract     X       X
# - download    X       X

# Creates a file or a directory in the specified path.
def create(context: Context, path: str, data: List[str] = [""], dir: bool = False) -> None:
    prev_cwd = os.getcwd()
    if context.cwd:
        os.chdir(context.cwd)

    utils.create(path, data, dir=dir)

    os.chdir(prev_cwd)


# Reads a file in the specified path.
def read(context: Context, path: str) -> List[str]:
    prev_cwd = os.getcwd()
    if context.cwd:
        os.chdir(context.cwd)

    result = utils.read(path)

    os.chdir(prev_cwd)

    return result


# Checks if the specified path exists and whether it is a file or a directory.
def exists(context: Context, path: str) -> Optional[Literal["file", "dir"]]:
    prev_cwd = os.getcwd()
    if context.cwd:
        os.chdir(context.cwd)

    result = utils.exists(path)

    os.chdir(prev_cwd)

    return result


# Moves a file or a directory to the specified path.
def move(context: Context, source_path: str, dest_path: str) -> None:
    prev_cwd = os.getcwd()
    if context.cwd:
        os.chdir(context.cwd)

    utils.move(source_path, dest_path)

    os.chdir(prev_cwd)


# Removes a file or a directory in the specified path.
def remove(context: Context, path: str, dir: bool = False) -> None:
    prev_cwd = os.getcwd()
    if context.cwd:
        os.chdir(context.cwd)

    utils.remove(path, dir=dir)

    os.chdir(prev_cwd)


# Extracts a zip, tar, gztar, bztar, or xztar file in the specified path.
def extract(context: Context, source_path: str, dest_path: str) -> None:
    prev_cwd = os.getcwd()
    if context.cwd:
        os.chdir(context.cwd)

    utils.extract(source_path, dest_path)

    os.chdir(prev_cwd)


# Downloads a file to the specified path.
def download(context: Context, url: str, path: str) -> None:
    prev_cwd = os.getcwd()
    if context.cwd:
        os.chdir(context.cwd)

    utils.download(url, path)

    os.chdir(prev_cwd)


# Extends Pyinvoke's Context methods.
def init() -> None:
    Context.print = staticmethod(print)
    Context.input = staticmethod(input)
    Context.fail = staticmethod(fail)
    Context.exit = staticmethod(exit)
    Context.info = staticmethod(info)
    Context.warn = staticmethod(warn)
    Context.attempt = attempt
    Context.has = has
    Context.repository = repository
    Context.commit = commit
    Context.branch = branch
    Context.tag = tag
    Context.changes = changes
    Context.create = create
    Context.read = read
    Context.exists = exists
    Context.move = move
    Context.remove = remove
    Context.extract = extract
    Context.download = download
