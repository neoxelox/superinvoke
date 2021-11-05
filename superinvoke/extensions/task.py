from typing import Tuple

import invoke

from .. import collections, objects


# Pyinvoke task wrapper, allows global task configuration.
def task(*args, **kwargs):
    args, kwargs = __pre_hook_tools(*args, **kwargs)

    return invoke.task(*args, **kwargs)


# TODO: Option to only check if task's required tools are installed
# with the correct version, but not automatically install them.

# Pre hook task's tool dependencies to automatically install them.
def __pre_hook_tools(*args, **kwargs) -> Tuple[list, dict]:
    tools = [tool.name if type(tool) == objects.Tool else str(tool) for tool in kwargs.get("tools", [])]

    if tools:

        @invoke.task(name=f"pre_hook_tools_{'_'.join(tools)}")
        def pre_hook(context):
            collections.tool.install(context, include=",".join(tools), exclude="", yes=True)

        kwargs["pre"] = [*(kwargs.get("pre", [])), pre_hook]
        kwargs.pop("tools")

    return args, kwargs
