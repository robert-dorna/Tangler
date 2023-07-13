from typing import Any

from tangler.library import types
from tangler.library.spaces.config import SpacesConfig
from tangler.library.spaces.filesystem import FilesystemSpace

from . import utils_assets as assets
from .utils_fixtures import *
from .utils_requests import *


def test_space_config_with_valid_path() -> None:
    space_config = SpacesConfig("tests/assets/spaces.yml")
    assert space_config.config == assets.spaces_config()


def test_filesystem_space(space_copy_path) -> None:
    fs_space = FilesystemSpace(space_copy_path)

    assert fs_space.list_types_names() == [
        assets.exising.type_name_second,
        assets.exising.type_name,
    ]
    assert list(fs_space.list_fields_names(types.TypeName("task"))) == [
        assets.exising.field_name_second,
        assets.exising.field_name,
    ]
    assert list(fs_space.list_fields_names(types.TypeName("note"))) == [
        assets.exising.field_name_second,
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
