import os
import shutil
from enum import Enum
from pathlib import Path
from typing import List, Literal, Optional

from download import download as fetch


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


# Creates a file or a directory in the specified path (overwritting).
def create(path: str, data: List[str] = [""], dir: bool = False) -> None:
    if dir:
        os.makedirs(str(path), exist_ok=True)
    else:
        data = [str(line) + "\n" for line in data]
        with open(str(path), "w") as f:
            f.writelines(data)


# Reads a file in the specified path.
def read(path: str) -> List[str]:
    with open(str(path), "r") as f:
        return f.read().splitlines()


# Checks if the specified path exists and whether it is a file or a directory.
def exists(path: str) -> Optional[Literal["file", "dir"]]:
    if not os.path.exists(str(path)):
        return None
    elif os.path.isdir(str(path)):
        return "dir"
    elif os.path.isfile(str(path)):
        return "file"
    else:
        return None


# Moves a file or a directory to the specified path.
def move(source_path: str, dest_path: str) -> None:
    shutil.move(str(source_path), str(dest_path))


# Removes a file or a directory in the specified path.
def remove(path: str, dir: bool = False) -> None:
    if dir:
        shutil.rmtree(str(path))
    else:
        os.remove(str(path))


# Extracts a zip, tar, gztar, bztar, or xztar file in the specified path.
def extract(source_path: str, dest_path: str) -> None:
    shutil.unpack_archive(str(source_path), str(dest_path))


# Downloads a file to the specified path.
def download(url: str, path: str) -> None:
    fetch(str(url), str(path), progressbar=False, replace=True, verbose=False)
