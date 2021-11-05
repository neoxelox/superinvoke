import os
import shutil
import sys
from typing import List, Optional

from download import download as fetch
from invoke.context import Context

from .. import constants


# Writes to stdout and flushes.
def print(message: str) -> None:
    constants.console.print(f"[default on default][not bold]{message}[/not bold][/default on default]")


# Reads from stdout.
def input(message: str) -> str:
    return constants.console.input(f"[default on default][not bold]{message}[/not bold][/default on default]")


# Terminates the current task immediately with error.
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
        result = context.run(command, warn=True, hide="both")
    except Exception:
        return ""

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    return stdout or stderr


# Checks whether a certain version of a program is installed.
def has(context: Context, program: str, version: Optional[str] = None) -> bool:
    if version:
        return version in context.attempt(f"{program} --version") or version in context.attempt(f"{program} version")
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


# Gets the N last changes.
def changes(context: Context, scope: int = 1) -> List[str]:
    return context.attempt(f"git diff --name-only HEAD HEAD~{scope}").split("\n")


# TODO: CRUD for files and directories:
#               FILE    DIR
# - copy
# - move        X       X
# - create              X
# - remove
# - read
# - write
# - extract     X       X
# - download    X       X

# Creates a file or a directory in the specified path.
def create(context: Context, path: str, data: List[str] = [""], dir: bool = False) -> None:
    if dir:
        os.makedirs(str(path), exist_ok=True)


# Moves a file or a directory to the specified path.
def move(context: Context, source_path: str, dest_path: str) -> None:
    shutil.move(str(source_path), str(dest_path))


# Removes a file or a directory in the specified path.
def remove(context: Context, path: str, dir: bool = False) -> None:
    if dir:
        shutil.rmtree(str(path))
    else:
        os.remove(str(path))


# Extracts a zip, tar, gztar, bztar, or xztar file in the specified path.
def extract(context: Context, source_path: str, dest_path: str) -> None:
    shutil.unpack_archive(str(source_path), str(dest_path))


# Downloads a file to the specified path.
def download(context: Context, url: str, path: str) -> None:
    fetch(str(url), str(path), progressbar=False, replace=True, verbose=False)


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
    Context.changes = changes
    Context.create = create
    Context.move = move
    Context.remove = remove
    Context.extract = extract
    Context.download = download
