from typing import Any, Callable, List, Optional

from .. import constants, utils
from .common import Tags


# Represents an environment.
class Env:
    name: str
    tags: List[Tags]

    def __init__(self, name: str, tags: List[Tags]):
        self.name = name
        self.tags = tags

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Env)
            and self.name == other.name
            and self.tags == other.tags
        )

    def __hash__(self) -> int:
        return hash((self.name, tuple(self.tags)))


# Represents the list of available environments.
class Envs:
    Default: Optional[Callable[[Any], Env]] = None

    @utils.classproperty
    def All(cls) -> List[Env]:
        all = []

        for env in dir(cls):
            if env in ["All", "Default", "Current"]:
                continue

            env = getattr(cls, env)
            if isinstance(env, Env):
                all.append(env)

        return all

    @utils.classproperty
    def Current(cls) -> Optional[Env]:
        if utils.exists(utils.path(constants.Paths.ENV)) == "file":
            return cls.ByName(utils.read(utils.path(constants.Paths.ENV))[0])

        if hasattr(cls, "Default") and cls.Default is not None:
            return cls.Default(cls)

        return None

    @classmethod
    def ByTag(cls, tag) -> List[Env]:
        return [env for env in cls.All if tag in env.tags]

    @classmethod
    def ByName(cls, name) -> Optional[Env]:
        for env in cls.All:
            if name == env.name:
                return env

        return None
