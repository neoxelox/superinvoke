import os
from enum import Enum
from pathlib import Path


# String enumerator.
class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str(self.value)


# Python hack in order to allow static properties.
class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


# Resolves input path and its environment variables
# indistinctly from the current OS.
def path(path: str) -> str:
    return str(Path(os.path.expandvars(path)).resolve())


# Splits input string returning the left-most word
# and the rest of the string.
def next_arg(string: str) -> str:
    lpos = string.find(" ")
    return (string[:lpos], string[lpos + 1 :]) if lpos != -1 else (string, "")
