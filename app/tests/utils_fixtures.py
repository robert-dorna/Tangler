from pathlib import Path
from shutil import copytree, rmtree

import pytest
from flask.testing import FlaskClient
from tangler.library.spaces.config import SpacesConfig
from tangler.library.spaces.filesystem import FilesystemSpace
from tangler.server import Server


@pytest.fixture
def space_copy_path():
    space_path = Path("tests/assets/test.space")
    copy_path = space_path.parent / (str(space_path.name) + ".copy")

    if copy_path.exists() and copy_path.is_dir():
        rmtree(copy_path)

    copytree(space_path, copy_path)

    yield copy_path

    rmtree(copy_path)


@pytest.fixture
def server(space_copy_path) -> Server:
    space_config = SpacesConfig("tests/assets/spaces.yml")
    server = Server(space_config)
    return server


@pytest.fixture
def client(server: Server) -> FlaskClient:
    server.app.testing = True
    return server.app.test_client()


@pytest.fixture
def prod_client(server: Server) -> FlaskClient:
    server.app.testing = False
    return server.app.test_client()
