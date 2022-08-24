import fnmatch
from typing import List, Optional

from .. import constants, utils
from .common import Tags


# Represents an executable tool.
class Tool:
    name: str
    version: Optional[str]
    tags: List[Tags]
    path: str
    links: dict
    _managed: bool

    def __init__(
        self,
        name: str,
        version: Optional[str],
        tags: List[Tags],
        links: Optional[dict] = {},
        path: Optional[str] = None,
    ):
        self.name = name
        self.version = version
        self.tags = tags
        self.links = links
        self._managed = True

        if path is None:
            self.path = utils.path(f"{constants.Paths.TOOLS}/{self.name}")
        else:
            self.path = str(path)
            self._managed = False

    def __str__(self) -> str:
        return self.path

    @property
    def link(self) -> tuple:
        current_link = self.links.get(constants.Platforms.CURRENT, None)
        if current_link:
            return current_link

        default_link = self.links.get(constants.Platforms.LINUX, None)
        if default_link:
            return default_link

        return None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Tool) and self.name == other.name and self.version == other.version

    def __hash__(self) -> int:
        return hash((self.name, self.version))


# Represents the list of available tools.
class Tools:
    @utils.classproperty
    def All(cls) -> List[Tool]:
        all = []

        for tool in dir(cls):
            if tool == "All":
                continue

            tool = getattr(cls, tool)
            if isinstance(tool, Tool):
                all.append(tool)

        return all

    @classmethod
    def ByTag(cls, tag: str) -> List[Tool]:
        return [tool for tool in cls.All if fnmatch.filter(tool.tags, tag) or Tags.ALL in tool.tags]

    @classmethod
    def ByName(cls, name: str) -> List[Tool]:
        return [tool for tool in cls.All if fnmatch.filter([tool.name], name)]
