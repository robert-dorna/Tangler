import pytest
from shutil import copytree, rmtree
from pathlib import Path
from typing import Any
from tangler.library import types
from tangler.library.spaces.config import SpacesConfig
from tangler.library.spaces.filesystem import FilesystemSpace


@pytest.fixture
def space_copy_path():
    space_path = Path("tests/assets/tangler-test.space")
    copy_path = space_path.parent / (str(space_path.name) + "-copy")

    copytree(space_path, copy_path)

    yield copy_path

    rmtree(copy_path)


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


def test_filesystem_space_create_item(space_copy_path) -> None:
    fs_space = FilesystemSpace(space_copy_path)

    type_name = types.TypeName("task")

    new_item_type = fs_space.get_type(type_name)
    new_item = types.Item(
        full_id=types.Item.FullId(
            type=new_item_type,
            identifier=types.ItemIdentifier(-1),
        ),
        fields=types.ItemFields(
            {
                types.FieldName("title"): "hello there",
            }
        ),
    )

    created_item = fs_space.create_item(type_name, new_item, place=None)
    read_item = fs_space.get_item(type_name, types.ItemIdentifier(1))

    assert id(created_item) != id(new_item)
    assert id(created_item) == id(read_item)
    assert fs_space.list_root_items(type_name) == [created_item]
    assert new_item.full_id.identifier == -1
    assert read_item.full_id.identifier == 1
    assert created_item.full_id.identifier == 1

    created_item = fs_space.create_item(type_name, new_item, place=None)

    assert id(created_item) != id(new_item)
    assert id(created_item) != id(read_item)
    assert fs_space.list_root_items(type_name) == [read_item, created_item]
    assert new_item.full_id.identifier == -1
    assert read_item.full_id.identifier == 1
    assert created_item.full_id.identifier == 2
