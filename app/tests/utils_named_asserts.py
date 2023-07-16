from flask.testing import FlaskClient

from . import utils_assets as assets
from . import utils_requests as asserted_rq

# TODO: assert named asserts work? (at the beggining of testing and at the end?)
# TODO: assert assets work? (existing actually exists, not_existing actually does not exist etc.)

## ================================================================================ ##
## config                                                                           ##
## ================================================================================ ##


def config_did_not_change(client: FlaskClient) -> None:
    initial_config: dict = assets.initial_fsspace.config_file()
    current_config: dict = assets.current_fsspace.config_file()

    api_get_config: dict = asserted_rq.get(client, "/config")

    assert current_config == initial_config
    assert current_config == api_get_config


## ================================================================================ ##
## config - types                                                                   ##
## ================================================================================ ##


def config_has_extra_type(
    client: FlaskClient, extra_type_name, extra_type_definition
) -> None:
    initial_types: dict = assets.initial_fsspace.config_file()["types"]
    initial_types_names = list(initial_types.keys())
    initial_types_names_len = len(initial_types_names)

    current_types: dict = assets.current_fsspace.config_file()["types"]
    current_types_names = list(current_types.keys())
    current_types_names_len = len(current_types_names)

    api_get_type = asserted_rq.get(client, f"/config/types/{extra_type_name}")
    api_get_types = asserted_rq.get(client, "/config/types")

    assert current_types[extra_type_name] == api_get_type
    assert current_types == api_get_types

    assert current_types_names_len == initial_types_names_len + 1
    assert current_types_names == [extra_type_name] + initial_types_names
    assert current_types != initial_types
    assert current_types == {
        **initial_types,
        extra_type_name: extra_type_definition,
    }


def config_has_overridden_type(client: FlaskClient, type_name, type_definition) -> None:
    initial_types: dict = assets.initial_fsspace.config_file()["types"]
    initial_types_names = list(initial_types.keys())
    initial_types_names_len = len(initial_types_names)

    current_types: dict = assets.current_fsspace.config_file()["types"]
    current_types_names = list(current_types.keys())
    current_types_names_len = len(current_types_names)

    api_get_type = asserted_rq.get(client, f"/config/types/{type_name}")
    api_get_types = asserted_rq.get(client, "/config/types")

    assert current_types[type_name] == api_get_type
    assert current_types == api_get_types

    assert current_types[type_name] != initial_types[type_name]

    assert current_types_names_len == initial_types_names_len
    assert current_types_names == initial_types_names
    assert current_types != initial_types
    assert current_types == {
        **initial_types,
        type_name: type_definition,
    }


def config_has_renamed_type(client: FlaskClient, old_type_name, new_type_name) -> None:
    initial_types: dict = assets.initial_fsspace.config_file()["types"]
    initial_types_names = list(initial_types.keys())
    initial_types_names_len = len(initial_types_names)

    current_types: dict = assets.current_fsspace.config_file()["types"]
    current_types_names = list(current_types.keys())
    current_types_names_len = len(current_types_names)

    api_get_type = asserted_rq.get(client, f"/config/types/{new_type_name}")
    api_get_types = asserted_rq.get(client, "/config/types")

    asserted_rq.get(client, f"/config/types/{old_type_name}", code=500)

    assert current_types[new_type_name] == api_get_type
    assert current_types == api_get_types

    assert current_types[new_type_name] == initial_types[old_type_name]

    assert new_type_name not in initial_types
    assert old_type_name not in current_types

    assert current_types_names_len == initial_types_names_len
    assert current_types_names != initial_types_names
    assert current_types != initial_types

    initial_type = initial_types.pop(old_type_name)
    current_type = current_types.pop(new_type_name)

    assert current_types == initial_types
    assert current_type == initial_type


def config_has_updated_type(client: FlaskClient, type_name, type_patch) -> None:
    initial_types: dict = assets.initial_fsspace.config_file()["types"]
    initial_types_names = list(initial_types.keys())
    initial_types_names_len = len(initial_types_names)

    current_types: dict = assets.current_fsspace.config_file()["types"]
    current_types_names = list(current_types.keys())
    current_types_names_len = len(current_types_names)

    api_get_type = asserted_rq.get(client, f"/config/types/{type_name}")
    api_get_types = asserted_rq.get(client, "/config/types")

    assert current_types[type_name] == api_get_type
    assert current_types == api_get_types

    assert current_types[type_name] != initial_types[type_name]

    assert current_types_names_len == initial_types_names_len
    assert current_types_names == initial_types_names
    assert current_types != initial_types

    initial_type = initial_types.pop(type_name)
    current_type = current_types.pop(type_name)

    assert current_types == initial_types
    assert current_type != initial_type
    assert current_type == {
        **initial_type,
        **type_patch,
    }


def config_is_missing_type(client: FlaskClient, type_name) -> None:
    initial_types: dict = assets.initial_fsspace.config_file()["types"]
    initial_types_names = list(initial_types.keys())
    initial_types_names_len = len(initial_types_names)

    current_types: dict = assets.current_fsspace.config_file()["types"]
    current_types_names = list(current_types.keys())
    current_types_names_len = len(current_types_names)

    api_get_types = asserted_rq.get(client, "/config/types")

    asserted_rq.get(client, f"/config/types/{type_name}", code=500)

    assert current_types == api_get_types

    assert type_name in initial_types
    assert type_name not in current_types

    assert current_types_names_len + 1 == initial_types_names_len
    assert current_types_names + [type_name] == initial_types_names
    assert current_types != initial_types

    initial_types.pop(type_name)

    assert current_types == initial_types


## ================================================================================ ##
## config - fields                                                                  ##
## ================================================================================ ##


def config_has_extra_field(
    client: FlaskClient, type_name, extra_field_name, extra_field_definition
) -> None:
    expected_field = {
        **extra_field_definition,
        "name": extra_field_name,
    }

    expected_config: dict = assets.initial_fsspace.config_file()
    expected_types: dict = expected_config["types"]
    expected_type: dict = expected_types[type_name]
    expected_fields: list = expected_type["fields"]

    expected_fields.append(expected_field)

    actual_config = asserted_rq.get(client, "/config")
    actual_types = asserted_rq.get(client, "/config/types")
    actual_type = asserted_rq.get(client, f"/config/types/{type_name}")
    actual_fields = asserted_rq.get(client, f"/config/fields/{type_name}")
    actual_field = asserted_rq.get(
        client, f"/config/fields/{type_name}/{extra_field_name}"
    )

    assert actual_config == expected_config
    assert actual_types == expected_types
    assert actual_type == expected_type
    assert actual_fields == expected_fields
    assert actual_field == expected_field

    assert actual_config == assets.current_fsspace.config_file()


# TODO: Thinks of such solution that is not causing many config file
# reads and safe to modify expected_config e.g. for comparisons.
# def types_did_not_change(client: FlaskClient) -> None:
#     expected_config: dict = assets.test_space_config()
#     expected_types: dict = expected_config['types']

#     actual_types = asserted_rq.get(client, "/config/types")

#     assert actual_types == expected_types


def config_has_overridden_field(
    client: FlaskClient, type_name, field_name, field_definition
) -> None:
    expected_field = {
        **field_definition,
        "name": field_name,
    }

    expected_config: dict = assets.initial_fsspace.config_file()
    expected_types: dict = expected_config["types"]
    expected_type: dict = expected_types[type_name]
    expected_fields: list = expected_type["fields"]

    field_index = next(
        i for i, e in enumerate(expected_fields) if e["name"] == field_name
    )
    previous_field = expected_fields[field_index]
    expected_fields[field_index] = expected_field

    actual_config = asserted_rq.get(client, "/config")
    actual_types = asserted_rq.get(client, "/config/types")
    actual_type = asserted_rq.get(client, f"/config/types/{type_name}")
    actual_fields = asserted_rq.get(client, f"/config/fields/{type_name}")
    actual_field = asserted_rq.get(client, f"/config/fields/{type_name}/{field_name}")

    assert actual_config == expected_config
    assert actual_types == expected_types
    assert actual_type == expected_type
    assert actual_fields == expected_fields
    assert actual_field == expected_field

    assert expected_field != previous_field

    assert actual_config == assets.current_fsspace.config_file()


def config_has_renamed_field(
    client: FlaskClient, type_name, old_field_name, new_field_name
) -> None:
    expected_config: dict = assets.initial_fsspace.config_file()
    expected_types: dict = expected_config["types"]
    expected_type: dict = expected_types[type_name]
    expected_fields: list = expected_type["fields"]

    field_index = next(
        i for i, e in enumerate(expected_fields) if e["name"] == old_field_name
    )

    previous_field: dict = expected_fields[field_index].copy()
    expected_field: dict = expected_fields[field_index]
    expected_field["name"] = new_field_name

    actual_config = asserted_rq.get(client, "/config")
    actual_types = asserted_rq.get(client, "/config/types")
    actual_type = asserted_rq.get(client, f"/config/types/{type_name}")
    actual_fields = asserted_rq.get(client, f"/config/fields/{type_name}")
    actual_field = asserted_rq.get(
        client, f"/config/fields/{type_name}/{new_field_name}"
    )

    asserted_rq.get(client, f"/config/fields/{type_name}/{old_field_name}", code=500)

    assert actual_config == expected_config
    assert actual_types == expected_types
    assert actual_type == expected_type
    assert actual_fields == expected_fields
    assert actual_field == expected_field

    assert len(actual_fields) == len(expected_fields)

    assert expected_field != previous_field

    prev_name = previous_field.pop("name")
    curr_name = actual_field.pop("name")

    assert old_field_name == prev_name
    assert new_field_name == curr_name

    assert previous_field == actual_field

    assert actual_config == assets.current_fsspace.config_file()


def config_has_updated_field(
    client: FlaskClient, type_name, field_name, field_patch
) -> None:
    expected_config: dict = assets.initial_fsspace.config_file()
    expected_types: dict = expected_config["types"]
    expected_type: dict = expected_types[type_name]
    expected_fields: list = expected_type["fields"]

    field_index = next(
        i for i, e in enumerate(expected_fields) if e["name"] == field_name
    )
    previous_field: dict = expected_fields[field_index].copy()
    expected_fields[field_index] |= field_patch
    expected_field: dict = expected_fields[field_index]

    actual_config = asserted_rq.get(client, "/config")
    actual_types = asserted_rq.get(client, "/config/types")
    actual_type = asserted_rq.get(client, f"/config/types/{type_name}")
    actual_fields = asserted_rq.get(client, f"/config/fields/{type_name}")
    actual_field = asserted_rq.get(client, f"/config/fields/{type_name}/{field_name}")

    assert actual_config == expected_config
    assert actual_types == expected_types
    assert actual_type == expected_type
    assert actual_fields == expected_fields
    assert actual_field == expected_field

    assert len(actual_fields) == len(expected_fields)

    assert expected_field != previous_field

    assert actual_config == assets.current_fsspace.config_file()


def config_is_missing_field(client: FlaskClient, type_name, field_name) -> None:
    expected_config: dict = assets.initial_fsspace.config_file()
    expected_types: dict = expected_config["types"]
    expected_type: dict = expected_types[type_name]
    expected_fields: list = expected_type["fields"]

    previous_fields_length = len(expected_fields)

    field_index = next(
        i for i, e in enumerate(expected_fields) if e["name"] == field_name
    )
    del expected_fields[field_index]

    actual_config = asserted_rq.get(client, "/config")
    actual_types = asserted_rq.get(client, "/config/types")
    actual_type = asserted_rq.get(client, f"/config/types/{type_name}")
    actual_fields = asserted_rq.get(client, f"/config/fields/{type_name}")

    asserted_rq.get(client, f"/config/fields/{type_name}/{field_name}", code=500)

    assert actual_config == expected_config
    assert actual_types == expected_types
    assert actual_type == expected_type
    assert actual_fields == expected_fields

    assert len(actual_fields) == previous_fields_length - 1

    assert actual_config == assets.current_fsspace.config_file()


## ================================================================================ ##
## items                                                                            ##
## ================================================================================ ##


def raw_item_equals_item_with_metadata(raw_item, type_name, item_with_metadata) -> None:
    raw_item_with_metadata = {
        **raw_item,
        "_what": type_name,
        "_children": [],
    }

    assert raw_item_with_metadata == item_with_metadata


def raw_items_eqaul_items_with_metadata(
    raw_items, type_name, items_with_metadata
) -> None:
    index = 0
    for raw_item, item_with_metadata in zip(raw_items, items_with_metadata):
        raw_item_equals_item_with_metadata(raw_item, type_name, item_with_metadata)
        index += 1


def items_file_did_not_change(client: FlaskClient, type_name) -> None:
    initial_items = assets.initial_fsspace.items_file(type_name)
    initial_items_len = len(initial_items)

    current_items = assets.current_fsspace.items_file(type_name)
    current_items_len = len(current_items)

    api_get_items = asserted_rq.get(client, f"/data/{type_name}")

    raw_items_eqaul_items_with_metadata(current_items, type_name, api_get_items)

    assert current_items_len == initial_items_len
    assert current_items == initial_items


def items_file_has_extra_item(
    client: FlaskClient, type_name, item_definition, *, new_id
) -> None:
    initial_items = assets.initial_fsspace.items_file(type_name)
    initial_items_len = len(initial_items)

    current_items = assets.current_fsspace.items_file(type_name)
    current_items_len = len(current_items)

    api_get_items = asserted_rq.get(client, f"/data/{type_name}")

    raw_items_eqaul_items_with_metadata(current_items, type_name, api_get_items)

    assert "_id" not in item_definition

    item_definition["_id"] = new_id

    assert current_items_len == initial_items_len + 1
    assert current_items == initial_items + [item_definition]


def items_file_has_updated_item(
    client: FlaskClient, type_name, item_id, item_patch
) -> None:
    initial_items: list = assets.initial_fsspace.items_file(type_name)
    initial_items_len = len(initial_items)

    current_items: list = assets.current_fsspace.items_file(type_name)
    current_items_len = len(current_items)

    api_get_items = asserted_rq.get(client, f"/data/{type_name}")
    apt_get_item = asserted_rq.get(client, f"/data/{type_name}/{item_id}")

    raw_items_eqaul_items_with_metadata(current_items, type_name, api_get_items)

    # assert "_id" not in item_definition

    assert current_items_len == initial_items_len
    assert current_items != initial_items

    item_index = next(i for i, e in enumerate(initial_items) if e["_id"] == item_id)

    initial_item = initial_items.pop(item_index)
    current_item = current_items.pop(item_index)

    raw_item_equals_item_with_metadata(current_item, type_name, apt_get_item)

    assert current_items == initial_items
    assert current_item != initial_item

    initial_item |= item_patch

    assert current_item == initial_item


def items_file_is_missing_item(client: FlaskClient, type_name, item_id) -> None:
    initial_items: list = assets.initial_fsspace.items_file(type_name)
    initial_items_len = len(initial_items)

    current_items: list = assets.current_fsspace.items_file(type_name)
    current_items_len = len(current_items)

    api_get_items = asserted_rq.get(client, f"/data/{type_name}")

    asserted_rq.get(client, f"/data/{type_name}/{item_id}", code=500)

    raw_items_eqaul_items_with_metadata(current_items, type_name, api_get_items)

    assert current_items_len == initial_items_len - 1
    assert current_items != initial_items

    item_index = next(i for i, e in enumerate(initial_items) if e["_id"] == item_id)

    initial_items.pop(item_index)

    assert current_items == initial_items


## ================================================================================ ##
## items & links (stuff related to parent-child relationships)                      ##
## ================================================================================ ##

# TODO: Define it and use in other named assets, e.g. when checking
# that items did not change.


def links_file_did_not_change():
    initial_links = assets.initial_fsspace.links_file()
    currect_links = assets.current_fsspace.links_file()

    assert currect_links == initial_links


# TODO: this is only for root to root same type, write others and split them + combine
# to avoid duplications
def items_file_has_item_placed_above_another(
    client: FlaskClient, type_name, moving_item_id, reference_item_id
) -> None:
    initial_items: list = assets.initial_fsspace.items_file(type_name)
    initial_items_len = len(initial_items)

    current_items: list = assets.current_fsspace.items_file(type_name)
    current_items_len = len(current_items)

    api_get_items = asserted_rq.get(client, f"/data/{type_name}")

    raw_items_eqaul_items_with_metadata(current_items, type_name, api_get_items)

    assert current_items_len == initial_items_len
    assert current_items != initial_items

    initial_item_index = next(
        i for i, e in enumerate(initial_items) if e["_id"] == moving_item_id
    )

    current_item_index = next(
        i for i, e in enumerate(current_items) if e["_id"] == moving_item_id
    )

    assert current_item_index != initial_item_index

    assert initial_items[current_item_index]["_id"] == reference_item_id
    assert current_items[current_item_index + 1]["_id"] == reference_item_id

    initial_item = initial_items.pop(initial_item_index)
    current_item = current_items.pop(current_item_index)

    assert current_items == initial_items
    assert current_item == initial_item


## ================================================================================ ##
## space                                                                            ##
## ================================================================================ ##


def space_did_not_change(client: FlaskClient) -> None:
    config_did_not_change(client)
    items_file_did_not_change(client, assets.exising.type_name)
    items_file_did_not_change(client, assets.exising.type_name_second)
