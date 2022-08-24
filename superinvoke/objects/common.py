import fnmatch
from typing import List

from .. import utils


# Represents the list of available tags.
class Tags(utils.StrEnum):
    @utils.classproperty
    def All(cls) -> List[str]:
        all = []

        for tag in dir(cls):
            if tag in ["All", "ALL"]:
                continue

            tag = getattr(cls, tag)
            if isinstance(tag, Tags):
                all.append(tag)

        return all

    @utils.classproperty
    def ALL(cls):
        """
        Deprecated. Use As(<glob>) with unpacking.
        Example: tags=[*Tags.As("*")]
        """
        return "*"

    @classmethod
    def As(cls, tag: str) -> List[str]:
        return [tag_ for tag_ in cls.All if fnmatch.filter([tag_], tag)]
