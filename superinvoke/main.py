import os
from typing import Optional

from invoke import Collection

from . import collections, objects
from .extensions import context


# Superinvoke root collection initialization.
def init(tools: Optional[objects.Tools] = None, envs: Optional[objects.Envs] = None) -> Collection:
    if tools:
        global __TOOLS__
        __TOOLS__ = tools

    if envs:
        global __ENVS__
        __ENVS__ = envs

    context.init()

    # Root collection
    root = Collection()
    root.configure({  # noqa: BLK100
        "run": {
            "shell": os.environ.get("COMSPEC", os.environ.get("SHELL")),
            "encoding": "utf-8"
        }
    })
    root.add_task(collections.misc.help)
    root.add_task(collections.misc.version)

    if tools:
        # Tool collection
        tool = Collection()
        tool.add_task(collections.tool.install)
        tool.add_task(collections.tool.list)
        tool.add_task(collections.tool.remove)
        tool.add_task(collections.tool.run)
        root.add_collection(tool, name="tool")

    if envs:
        # Environment collection
        env = Collection()
        env.add_task(collections.env.list)
        env.add_task(collections.env.switch)
        root.add_collection(env, name="env")

    return root
