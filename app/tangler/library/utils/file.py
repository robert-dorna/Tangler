import json
import os
from typing import Any
from pathlib import Path

import yaml

# from os import Pathlike ? (Protocol)


def read_yaml(path: str | Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def write_yaml(path: str | Path, data: dict) -> None:
    with open(path, "w") as f:
        yaml.safe_dump(data, f)


def read_json(path: str | Path) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def write_json(path: str | Path, data: dict | list, *, indent: int = 4):
    with open(path, "w") as f:
        f.write(json.dumps(data, indent=indent))


class File:
    def __init__(
        self, path: str | Path, *, read_func, write_func, initializer=None, on_init=None
    ):
        self.path = Path(path)
        self._read_func = read_func
        self._write_func = write_func

        if initializer is not None:
            self.write(initializer)
        elif on_init is not None:
            on_init(self.read())

    def read(self) -> Any:
        if self.path.exists():
            return self._read_func(self.path)
        else:
            raise FileNotFoundError(f"path {self.path.absolute()} does not exist")

    def write(self, data) -> None:
        self._write_func(self.path, data)

    def rename(self, new_file_name: str):
        self.path = self.path.rename(self.path.parent / new_file_name)

    def remove(self):
        self.path.unlink()


class JsonFile(File):
    def __init__(self, path: str | Path, *, initializer=None, on_init=None):
        super().__init__(
            path,
            read_func=read_json,
            write_func=write_json,
            initializer=initializer,
            on_init=on_init,
        )


class YamlFile(File):
    def __init__(self, path: str | Path, *, initializer=None, on_init=None):
        super().__init__(
            path,
            read_func=read_yaml,
            write_func=write_yaml,
            initializer=initializer,
            on_init=on_init,
        )


# class FileWatcher(File):
#     def __init__(
#         self, path: str | Path, on_change, read_func, write_func, *, initialize=None
#     ):
#         super().__init__(path, read_func, write_func, initialize=initialize)

#         # TODO: it should actually watch filesystem for changes like with watchdog python module, inotify or smth
#         self.on_change = on_change
#         self.on_change(self.data)

#     def silent_write(self, data: dict) -> None:
#         # now this is just a write, but when this class will actually watch a file,
#         # this should ignore the corresponding to that file write operation change event
#         return self.write(data)


# class YamlWatcher(FileWatcher):
#     def __init__(self, path: str | Path, on_change) -> None:
#         super().__init__(path, on_change, read_yaml, write_yaml)


# class JsonWatcher(FileWatcher):
#     def __init__(self, path: str | Path, on_change) -> None:
#         super().__init__(path, on_change, read_json, write_json)
