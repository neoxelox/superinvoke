import sys

from rich.console import Console

from . import utils


# Different OS Platforms.
class Platforms(utils.StrEnum):
    LINUX = "linux"
    WINDOWS = "win32"
    MACOS = "darwin"

    @utils.classproperty
    def CURRENT(cls):
        return Platforms(sys.platform)


# Different superinvoke directories.
class Directories(utils.StrEnum):
    CACHE = ".superinvoke_cache"

    @utils.classproperty
    def TOOLS(cls):
        return f"{Directories.CACHE}/tools"


# Global console instance.
console: Console = Console()
