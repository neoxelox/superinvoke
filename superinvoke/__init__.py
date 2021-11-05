__version_info__ = (0, 1, 0)
__version__ = ".".join(map(str, __version_info__))


import invoke

from .constants import Directories, Platforms, console
from .extensions.task import task
from .main import init
from .objects import Tags, Tool, Tools
from .utils import path
