import os

from invoke import Collection

from . import collections, objects
from .extensions import context


# Superinvoke root collection initialization.
def init(tools: objects.Tools) -> Collection:
    global __TOOLS__
    __TOOLS__ = tools

    context.init()

    # Root collection
    root = Collection()
    root.configure({
        "run": {
            "shell": os.environ.get("COMSPEC", os.environ.get("SHELL")),
            "encoding": "utf-8"
        }
    })
    root.add_task(collections.misc.help)

    # Tool collection
    tool = Collection()
    tool.add_task(collections.tool.install)
    tool.add_task(collections.tool.list)
    tool.add_task(collections.tool.remove)
    tool.add_task(collections.tool.run)
    root.add_collection(tool, name="tool")

    return root
