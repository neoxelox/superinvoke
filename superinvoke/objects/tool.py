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

    def __init__(self, name: str, version: Optional[str], tags: List[Tags], links: dict):
        self.name = name
        self.version = version
        self.tags = tags
        self.path = utils.path(f"{constants.Paths.TOOLS}/{self.name}")
        self.links = links

    def __str__(self) -> str:
        return self.path

    @property
    def link(self) -> tuple:
        return self.links.get(constants.Platforms.CURRENT, constants.Platforms.LINUX)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Tool)
            and self.name == other.name
            and self.version == other.version
        )

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
    def ByTag(cls, tag) -> List[Tool]:
        return [tool for tool in cls.All if tag in tool.tags]

    @classmethod
    def ByName(cls, name) -> Optional[Tool]:
        for tool in cls.All:
            if name == tool.name:
                return tool

        return None
