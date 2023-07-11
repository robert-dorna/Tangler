import json

import pytest
from flask.testing import FlaskClient
from tangler.library.spaces.config import SpacesConfig
from tangler.library.spaces.filesystem import FilesystemSpace
from tangler.server import Server


@pytest.fixture
def server() -> Server:
    space_config = SpacesConfig("tests/assets/spaces.yml")
    server = Server(space_config)
    return server


@pytest.fixture
def client(server: Server) -> FlaskClient:
    server.app.testing = True
    return server.app.test_client()


def test_server_with_spaces_config():
    space_config = SpacesConfig("tests/assets/spaces.yml")
    server = Server(space_config)

    assert server.spaces_config.config == {
        "spaces": [
            {
                "name": "TanglerTest",
                "directory": "./tangler-test.space/",
            }
        ]
    }

    assert isinstance(server.space, FilesystemSpace)
    assert (
        str(server.space.path.absolute())
        == "/source/app/tests/assets/tangler-test.space"
    )


def test_server_run():
    space_config = SpacesConfig("tests/assets/spaces-wrong.yml")
    with pytest.raises(FileNotFoundError):
        server = Server(space_config)
    assert True


def test_server_config_request(client: FlaskClient):
    with open("tests/assets/config.json", "r") as f:
        expected = {
            "result_summary": "request processed",
            "result": json.load(f),
        }

    response = client.get("/config")

    assert response.status_code == 200
    assert response.json == expected
