from tangler.library import types
from tangler.library.spaces.config import SpacesConfig
from tangler.library.spaces.filesystem import FilesystemSpace


def test_space_config_with_valid_path():
    space_config = SpacesConfig("tests/assets/spaces.yml")
    expected_config = {
        "spaces": [
            {
                "name": "TanglerTest",
                "directory": "./tangler-test.space/",
            }
        ]
    }

    assert space_config.config == expected_config


def test_filesystem_space():
    fs_space = FilesystemSpace("tests/assets/tangler-test.space")

    assert fs_space.list_types_names() == ["note", "task"]
    assert list(fs_space.list_fields_names(types.TypeName("task"))) == [
        "title",
        "category",
    ]
    assert list(fs_space.list_fields_names(types.TypeName("note"))) == [
        "title",
    ]
