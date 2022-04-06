__version_info__ = (0, 1, 0)
__version__ = ".".join(map(str, __version_info__))


import invoke

from . import utils
from .constants import Paths, Platforms, console
from .extensions.collection import Collection
from .extensions.task import task
from .main import init
from .objects import Env, Envs, Tags, Tool, Tools
