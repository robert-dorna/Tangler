from tangler import Tangler
from tangler.library.spaces.config import SpacesConfig


def test_tangler_server():
    space_config = SpacesConfig("tests/assets/spaces.yml")
    tangler = Tangler(space_config)

    assert space_config.config == {
        "spaces": [
            {
                "name": "TanglerTest",
                "directory": "./tangler-test.space/",
            }
        ]
    }

    # tangler.run(["tangler", "server"])
    assert True
