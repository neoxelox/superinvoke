import sys

from rich.console import Console

from . import utils


# Different OS Platforms.
# TODO: Add architechtures.
class Platforms(utils.StrEnum):
    LINUX = "linux"
    WINDOWS = "win32"
    MACOS = "darwin"

    @utils.classproperty
    def CURRENT(cls):
        return Platforms(sys.platform)


# Different superinvoke paths.
class Paths(utils.StrEnum):
    CACHE = ".superinvoke_cache"

    @utils.classproperty
    def TOOLS(cls):
        return f"{Paths.CACHE}/tools"

    @utils.classproperty
    def ENV(cls):
        return f"{Paths.CACHE}/env"


# Global console instance.
console: Console = Console()
