from tangler import Tangler
from tangler.library.spaces.config import SpacesConfig

from . import utils_assets as assets


def test_tangler_server():
    space_config = SpacesConfig("tests/assets/spaces.yml")
    tangler = Tangler(space_config)

    assert space_config.config == assets.spaces_config()

    # tangler.run(["tangler", "server"])
    assert True
