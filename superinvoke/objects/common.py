from .. import utils


# Represents the list of available tags.
class Tags(utils.StrEnum):
    @utils.classproperty
    def ALL(cls):
        return "all"
