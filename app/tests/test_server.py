import pytest
from tangler.library.spaces.config import SpacesConfig
from tangler.library.spaces.filesystem import FilesystemSpace
from tangler.server import Server

from . import utils_assets as assets
from .utils_fixtures import *


def test_server_with_spaces_config(space_copy_path):
    space_config = SpacesConfig("tests/assets/spaces.yml")
    server = Server(space_config)

    assert server.spaces_config.config == assets.spaces_config()
    assert isinstance(server.space, FilesystemSpace)
    assert (
        str(server.space.path.absolute()) == "/source/app/tests/assets/test.space.copy"
    )


def test_server_run():
    space_config = SpacesConfig("tests/assets/spaces-wrong.yml")
    with pytest.raises(FileNotFoundError):
        server = Server(space_config)
    assert True
