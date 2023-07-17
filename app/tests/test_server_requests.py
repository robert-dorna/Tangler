from flask.testing import FlaskClient

from . import utils_assets as assets
from . import utils_requests as asserted_rq
from . import utils_named_asserts as named_asserts
from .utils_fixtures import *

# TODO: assert that GET requests fail if they contain unused json data etc.


## ================================================================================ ##
## config                                                                           ##
## ================================================================================ ##


def test_server_config_read(client: FlaskClient):
    config = asserted_rq.get(client, "/config")
    config_sections_names = list(config.keys())

    assert config_sections_names == ["formatters", "order", "types"]
    assert config == assets.initial_fsspace.config_file()
    assert config == assets.current_fsspace.config_file()


def test_server_config_read_section(client: FlaskClient):
    config = asserted_rq.get(client, "/config")
    config_section_types = asserted_rq.get(client, "/config/types")
    config_section_order = asserted_rq.get(client, "/config/order")
    config_section_formatters = asserted_rq.get(client, "/config/formatters")

    assert config_section_types == config["types"]
    assert config_section_order == config["order"]
    assert config_section_formatters == config["formatters"]


def test_server_config_read_section_not_existing(prod_client: FlaskClient):
    unknown_section = assets.not_exising.config_section_name

    assert unknown_section not in asserted_rq.get(prod_client, "/config")
    asserted_rq.get(prod_client, f"/config/{unknown_section}", code=500)


def test_server_config_create_disallowed():
    pass  # config and both known and unknown sections


def test_server_config_set_order(client: FlaskClient):
    old_order = asserted_rq.get(client, "/config/order")
    new_order = list(reversed(old_order))

    asserted_rq.put(client, "/config/order", json=new_order)

    order = asserted_rq.get(client, "/config/order")

    assert order == new_order
    assert order != old_order
    assert order == list(reversed(old_order))

    assert old_order == assets.initial_fsspace.config_file()["order"]
    assert new_order == assets.current_fsspace.config_file()["order"]


def test_server_config_set_disallowed(client: FlaskClient):
    pass


def test_server_config_update_disallowed(client: FlaskClient):
    pass


def test_server_config_remove_disallowed(client: FlaskClient):
    pass


## ================================================================================ ##
## config - types                                                                   ##
## ================================================================================ ##

## config - types - read


def test_server_type_read(client: FlaskClient):
    config_section_types = asserted_rq.get(client, "/config/types")
    config_section_types_names = list(config_section_types.keys())

    assert config_section_types_names == [
        assets.exising.type_name_second,
        assets.exising.type_name,
    ]

    for type_name in config_section_types_names:
        type_definition = asserted_rq.get(client, f"/config/types/{type_name}")

        assert type_definition == config_section_types[type_name]


def test_server_type_read_not_existing(prod_client: FlaskClient):
    config_section_types = asserted_rq.get(prod_client, "/config/types")
    config_section_types_names = list(config_section_types.keys())

    assert assets.not_exising.type_name not in config_section_types_names

    asserted_rq.get(
        prod_client, f"/config/types/{assets.not_exising.type_name}", code=500
    )


## config - types - create


def test_server_type_create(client: FlaskClient):
    asserted_rq.post(
        client,
        f"/config/types/{assets.not_exising.type_name}",
        json=assets.definition_new_type_correct,
    )

    named_asserts.config_has_extra_type(
        client, assets.not_exising.type_name, assets.definition_new_type_correct
    )


def test_server_type_create_existing(prod_client: FlaskClient):
    # TODO: It should return correct error code and mention
    # that type 'note' is already taken in description.
    asserted_rq.post(
        prod_client,
        f"/config/types/{assets.exising.type_name}",
        json=assets.definition_new_type_correct,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


def test_server_type_create_invalid_key(prod_client: FlaskClient):
    asserted_rq.post(
        prod_client,
        f"/config/types/{assets.not_exising.type_name}",
        json=assets.definition_new_type_invalid_key,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


def test_server_type_create_invalid_key_value(prod_client: FlaskClient):
    asserted_rq.post(
        prod_client,
        f"/config/types/{assets.not_exising.type_name}",
        json=assets.definition_new_type_invalid_key_value,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


def test_server_type_create_resource_is_usable(prod_client: FlaskClient):
    pass  # creaet list items and assert .json was created


## config - types - set


def test_server_type_set(client: FlaskClient):
    asserted_rq.put(
        client,
        f"/config/types/{assets.not_exising.type_name}",
        json=assets.definition_new_type_correct,
    )

    named_asserts.config_has_extra_type(
        client, assets.not_exising.type_name, assets.definition_new_type_correct
    )


def test_server_type_set_existing(prod_client: FlaskClient):
    asserted_rq.put(
        prod_client,
        f"/config/types/{assets.exising.type_name}",
        json=assets.definition_new_type_correct,
    )

    named_asserts.config_has_overridden_type(
        prod_client, assets.exising.type_name, assets.definition_new_type_correct
    )


def test_server_type_set_invalid_key(prod_client: FlaskClient):
    asserted_rq.put(
        prod_client,
        f"/config/types/{assets.not_exising.type_name}",
        json=assets.definition_new_type_invalid_key,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


def test_server_type_set_invalid_key_value(prod_client: FlaskClient):
    asserted_rq.put(
        prod_client,
        f"/config/types/{assets.not_exising.type_name}",
        json=assets.definition_new_type_invalid_key_value,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


## config - types - rename


def test_server_type_rename(prod_client: FlaskClient):
    # TODO: Validate requests in handlers and test that unknown (.e.g "_name")
    # fields raise errors and are not just silently ignored.
    asserted_rq.patch(
        prod_client,
        f"/config/types/{assets.exising.type_name}",
        json={"name": assets.not_exising.type_name},
    )

    named_asserts.config_has_renamed_type(
        prod_client, assets.exising.type_name, assets.not_exising.type_name
    )


def test_server_type_rename_not_existing(prod_client: FlaskClient):
    asserted_rq.patch(
        prod_client,
        f"/config/types/{assets.not_exising.type_name}",
        json={"name": assets.not_exising.type_name_second},
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


def test_server_type_rename_to_existing(prod_client: FlaskClient):
    asserted_rq.patch(
        prod_client,
        f"/config/types/{assets.exising.type_name}",
        json={"name": assets.exising.type_name_second},
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


## config - types - update


def test_server_type_update(prod_client: FlaskClient):
    # TODO: Test that update can also rename a resource.
    # TODO: Test that updating fields array overrides it instead of patching.
    asserted_rq.patch(
        prod_client,
        f"/config/types/{assets.exising.type_name}",
        json=assets.patch_type_correct,
    )

    named_asserts.config_has_updated_type(
        prod_client, assets.exising.type_name, assets.patch_type_correct
    )


def test_server_type_update_not_existing(prod_client: FlaskClient):
    asserted_rq.patch(
        prod_client,
        f"/config/types/{assets.not_exising.type_name}",
        json=assets.patch_type_correct,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


def test_server_type_update_invalid_key(prod_client: FlaskClient):
    asserted_rq.patch(
        prod_client,
        f"/config/types/{assets.exising.type_name}",
        json=assets.patch_type_invalid_key,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


def test_server_type_update_invalid_key_value(prod_client: FlaskClient):
    # TODO: all type keys and their allowed values should be checked.
    # For now there is no checking or berly any implemented.
    pass


## config - types - remove


def test_server_type_remove(prod_client: FlaskClient):
    asserted_rq.delete(prod_client, f"/config/types/{assets.exising.type_name}")

    named_asserts.config_is_missing_type(prod_client, assets.exising.type_name)


def test_server_type_remove_not_existing(client: FlaskClient):
    asserted_rq.delete(client, f"/config/types/{assets.not_exising.type_name}")

    named_asserts.config_did_not_change(client)


## ================================================================================ ##
## config - fields                                                                  ##
## ================================================================================ ##

## config - fields - read


def test_server_field_read_all(client: FlaskClient):
    fields = asserted_rq.get(client, f"/config/fields/{assets.exising.type_name}")

    initial_types = assets.initial_fsspace.config_file()["types"]
    current_types = assets.current_fsspace.config_file()["types"]

    assert fields == initial_types[assets.exising.type_name]["fields"]
    assert fields == current_types[assets.exising.type_name]["fields"]


def test_server_field_read_all_not_existing_type(prod_client: FlaskClient):
    # TODO: assert nothing changed?
    initial_types = assets.initial_fsspace.config_file()["types"]

    assert assets.not_exising.type_name not in initial_types

    asserted_rq.get(
        prod_client, f"/config/fields/{assets.not_exising.type_name}", code=500
    )


def test_server_field_read(client: FlaskClient):
    initial_fields: list = assets.initial_fsspace.config_file()["types"][
        assets.exising.type_name
    ]["fields"]

    field = asserted_rq.get(
        client, f"/config/fields/{assets.exising.type_name}/{assets.exising.field_name}"
    )

    field_index = initial_fields.index(field)

    assert initial_fields[field_index] == field


def test_server_field_read_not_existing(prod_client: FlaskClient):
    initial_fields: list = assets.initial_fsspace.config_file()["types"][
        assets.exising.type_name
    ]["fields"]

    with pytest.raises(StopIteration):
        next(
            field
            for field in initial_fields
            if field["name"] == assets.not_exising.field_name
        )

    asserted_rq.get(
        prod_client,
        f"/config/fields/{assets.exising.type_name}/{assets.not_exising.field_name}",
        code=500,
    )


def test_server_field_read_not_existing_type(prod_client: FlaskClient):
    asserted_rq.get(
        prod_client,
        f"/config/fields/{assets.not_exising.type_name}/{assets.exising.field_name}",
        code=500,
    )


## config - fields - create


def test_server_field_create(client: FlaskClient):
    asserted_rq.post(
        client,
        f"/config/fields/{assets.exising.type_name}/{assets.not_exising.field_name}",
        json=assets.definition_new_field_correct,
    )

    named_asserts.config_has_extra_field(
        client,
        assets.exising.type_name,
        assets.not_exising.field_name,
        assets.definition_new_field_correct,
    )


def test_server_field_create_existing(prod_client: FlaskClient):
    asserted_rq.post(
        prod_client,
        f"/config/fields/{assets.exising.type_name}/{assets.exising.field_name}",
        json=assets.definition_new_field_correct,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


def test_server_field_create_invalid_key(prod_client: FlaskClient):
    asserted_rq.post(
        prod_client,
        f"/config/fields/{assets.exising.type_name}/{assets.not_exising.field_name}",
        json=assets.definition_new_field_invalid_key,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


def test_server_field_create_invalid_key_value(prod_client: FlaskClient):
    # TODO: Right now server and library has it barely implemented, improve this.
    pass


def test_server_field_create_not_existing_type(prod_client: FlaskClient):
    asserted_rq.post(
        prod_client,
        f"/config/fields/{assets.not_exising.type_name}/{assets.not_exising.field_name}",
        json=assets.definition_new_field_correct,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


## config - fields - set


def test_server_field_set(client: FlaskClient):
    asserted_rq.put(
        client,
        f"/config/fields/{assets.exising.type_name}/{assets.not_exising.field_name}",
        json=assets.definition_new_field_correct,
    )

    named_asserts.config_has_extra_field(
        client,
        assets.exising.type_name,
        assets.not_exising.field_name,
        assets.definition_new_field_correct,
    )


def test_server_field_set_existing(prod_client: FlaskClient):
    asserted_rq.put(
        prod_client,
        f"/config/fields/{assets.exising.type_name}/{assets.exising.field_name}",
        json=assets.definition_new_field_correct,
    )

    named_asserts.config_has_overridden_field(
        prod_client,
        assets.exising.type_name,
        assets.exising.field_name,
        assets.definition_new_field_correct,
    )


def test_server_field_set_invalid_key(prod_client: FlaskClient):
    asserted_rq.put(
        prod_client,
        f"/config/fields/{assets.exising.type_name}/{assets.not_exising.field_name}",
        json=assets.definition_new_field_invalid_key,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


def test_server_field_set_invalid_key_value(prod_client: FlaskClient):
    # TODO: implement better key value validation in library and server
    pass


def test_server_field_set_not_existing_type(prod_client: FlaskClient):
    asserted_rq.put(
        prod_client,
        f"/config/fields/{assets.not_exising.type_name}/{assets.exising.field_name}",
        json=assets.definition_new_field_correct,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


## config - fields - rename


def test_server_field_rename(prod_client: FlaskClient):
    asserted_rq.patch(
        prod_client,
        f"/config/fields/{assets.exising.type_name}/{assets.exising.field_name}",
        json={"name": assets.not_exising.field_name},
    )

    named_asserts.config_has_renamed_field(
        prod_client,
        assets.exising.type_name,
        assets.exising.field_name,
        assets.not_exising.field_name,
    )


# TODO: check renaming to the same name (no-op)


def test_server_field_rename_not_existing(prod_client: FlaskClient):
    asserted_rq.patch(
        prod_client,
        f"/config/fields/{assets.exising.type_name}/{assets.not_exising.field_name}",
        json={"name": assets.not_exising.field_name_second},
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


def test_server_field_rename_to_existing(prod_client: FlaskClient):
    asserted_rq.post(
        prod_client,
        f"/config/fields/{assets.exising.type_name}/{assets.not_exising.field_name}",
        json=assets.definition_new_field_correct,
    )

    asserted_rq.patch(
        prod_client,
        f"/config/fields/{assets.exising.type_name}/{assets.not_exising.field_name}",
        json={"name": assets.exising.field_name},
        code=500,
    )

    named_asserts.config_has_extra_field(
        prod_client,
        assets.exising.type_name,
        assets.not_exising.field_name,
        assets.definition_new_field_correct,
    )


def test_server_field_rename_not_existing_type(prod_client: FlaskClient):
    asserted_rq.patch(
        prod_client,
        f"/config/fields/{assets.not_exising.type_name}/{assets.exising.field_name}",
        json={"name": assets.not_exising.field_name},
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


## config - fields - update


def test_server_field_update(client: FlaskClient):
    asserted_rq.patch(
        client,
        f"/config/fields/{assets.exising.type_name}/{assets.exising.field_name}",
        json=assets.patch_field_correct,
    )

    named_asserts.config_has_updated_field(
        client,
        assets.exising.type_name,
        assets.exising.field_name,
        assets.patch_field_correct,
    )


def test_server_field_update_not_existing(prod_client: FlaskClient):
    asserted_rq.patch(
        prod_client,
        f"/config/fields/{assets.exising.type_name}/{assets.not_exising.field_name}",
        json=assets.patch_field_correct,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


def test_server_field_update_invalid_key(prod_client: FlaskClient):
    asserted_rq.patch(
        prod_client,
        f"/config/fields/{assets.exising.type_name}/{assets.exising.field_name}",
        json=assets.patch_field_invalid_key,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


def test_server_field_update_invalid_key_value(prod_client: FlaskClient):
    asserted_rq.patch(
        prod_client,
        f"/config/fields/{assets.exising.type_name}/{assets.exising.field_name}",
        json=assets.patch_field_invalid_key_value,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


def test_server_field_update_not_existing_type(prod_client: FlaskClient):
    asserted_rq.patch(
        prod_client,
        f"/config/fields/{assets.not_exising.type_name}/{assets.exising.field_name}",
        json=assets.patch_field_correct,
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


## config - fields - remove


# TODO: test "title" deletion prevention


def test_server_field_remove(prod_client: FlaskClient):
    asserted_rq.delete(
        prod_client,
        f"/config/fields/{assets.exising.type_name}/{assets.exising.field_name}",
    )

    named_asserts.config_is_missing_field(
        prod_client, assets.exising.type_name, assets.exising.field_name
    )


def test_server_field_remove_not_existing(prod_client: FlaskClient):
    asserted_rq.delete(
        prod_client,
        f"/config/fields/{assets.exising.type_name}/{assets.not_exising.field_name}",
    )

    named_asserts.config_did_not_change(prod_client)


def test_server_field_remove_not_existing_type(prod_client: FlaskClient):
    asserted_rq.delete(
        prod_client,
        f"/config/fields/{assets.not_exising.type_name}/{assets.exising.field_name}",
        code=500,
    )

    named_asserts.config_did_not_change(prod_client)


## ================================================================================ ##
## items                                                                            ##
## ================================================================================ ##

## items - read


def test_server_item_read_all(client: FlaskClient):
    items = asserted_rq.get(client, f"/data/{assets.exising.type_name}")

    named_asserts.raw_items_eqaul_items_with_metadata(
        assets.initial_fsspace.items_file(assets.exising.type_name),
        assets.exising.type_name,
        items,
    )
    named_asserts.raw_items_eqaul_items_with_metadata(
        assets.current_fsspace.items_file(assets.exising.type_name),
        assets.exising.type_name,
        items,
    )


def test_server_item_read_all_not_existing_type(prod_client: FlaskClient):
    asserted_rq.get(prod_client, f"/data/{assets.not_exising.type_name}", code=500)


def test_server_item_read(prod_client):
    item = asserted_rq.get(prod_client, f"/data/{assets.exising.type_name}/{7}")

    named_asserts.raw_item_equals_item_with_metadata(
        assets.initial_fsspace.items_file(assets.exising.type_name)[2],
        assets.exising.type_name,
        item,
    )
    named_asserts.raw_item_equals_item_with_metadata(
        assets.current_fsspace.items_file(assets.exising.type_name)[2],
        assets.exising.type_name,
        item,
    )


def test_server_item_read_not_existing(prod_client: FlaskClient):
    asserted_rq.get(prod_client, f"/data/{assets.exising.type_name}/{8}", code=500)


def test_server_item_read_not_existing_type(prod_client: FlaskClient):
    asserted_rq.get(prod_client, f"/data/{assets.not_exising.type_name}/{0}", code=500)


## items - create


def test_server_item_create(client: FlaskClient):
    asserted_rq.post(
        client,
        f"/data/{assets.exising.type_name}",
        json=assets.definition_new_item_correct,
    )

    named_asserts.items_file_has_extra_item(
        client, assets.exising.type_name, assets.definition_new_item_correct, new_id=8
    )


# TODO: Test create with mentioned id in resource path (url).


def test_server_item_create_invalid_key(prod_client: FlaskClient):
    # TODO: Implement validation in library and server.

    # asserted_rq.post(
    #     prod_client,
    #     f"/data/{assets.exising.type_name}",
    #     json=assets.definition_new_item_invalid_key,
    #     code=500,
    # )

    # named_asserts.items_did_not_change(prod_client, assets.exising.type_name)
    pass


def test_server_item_create_invalid_key_value(prod_client: FlaskClient):
    # TODO: Implement validation in library and server.
    pass


def test_server_item_create_not_existing_type(prod_client: FlaskClient):
    asserted_rq.post(
        prod_client,
        f"/data/{assets.not_exising.type_name}",
        json=assets.definition_new_item_correct,
        code=500,
    )

    named_asserts.space_did_not_change(prod_client)


# TODO: Test creating with specified place.

## items - set


def test_server_item_set():
    # TODO: test items do not have set, only post works for them
    # (as identifier cannot be manually specified, at least for now).
    pass


## items - move


# root above root same type
# root below root same type
# root under root same type

# root above root other type  X
# root below root other type  X
# root under root other type

# root above leaf same type
# root below leaf same type
# root under leaf same type

# root above leaf other type
# root below leaf other type
# root under leaf other type


# leaf above root same type
# leaf below root same type
# leaf under root same type

# leaf above root other type  X
# leaf below root other type  X
# leaf under root other type

# leaf above leaf same type
# leaf below leaf same type
# leaf under leaf same type

# leaf above leaf other type
# leaf below leaf other type
# leaf under leaf other type


def test_server_item_place_root_above_root_same_type(client: FlaskClient):
    id_source = 7
    id_reference = 4

    asserted_rq.patch(
        client,
        f"/data/{assets.exising.type_name}/{id_source}",
        json={
            "_place": {
                "relationship": "above",
                "reference": {
                    "what": assets.exising.type_name,
                    "_id": id_reference,
                },
            },
        },
    )

    named_asserts.items_file_has_item_placed_above_another(
        client,
        assets.exising.type_name,
        id_source,
        id_reference,
    )


## items - update


def test_server_item_update(client: FlaskClient):
    asserted_rq.patch(
        client,
        f"/data/{assets.exising.type_name}/{4}",
        json=assets.patch_item_correct,
    )

    named_asserts.items_file_has_updated_item(
        client,
        assets.exising.type_name,
        4,
        assets.patch_item_correct,
    )


def test_server_item_update_not_existing(prod_client: FlaskClient):
    asserted_rq.patch(
        prod_client,
        f"/data/{assets.exising.type_name}/{5}",
        json=assets.patch_item_correct,
        code=500,
    )

    named_asserts.space_did_not_change(prod_client)


# TODO: inplement key validation and Test update with invalid key.
# TODO: inplement value validation and Test update with invalid key value.


def test_server_item_update_not_existing_type(prod_client: FlaskClient):
    asserted_rq.patch(
        prod_client,
        f"/data/{assets.not_exising.type_name}/{4}",
        json=assets.patch_item_correct,
        code=500,
    )

    named_asserts.space_did_not_change(prod_client)


## items - remove


def test_server_item_remove(prod_client: FlaskClient):
    asserted_rq.delete(
        prod_client,
        f"/data/{assets.exising.type_name}/{4}",
    )

    named_asserts.items_file_is_missing_item(prod_client, assets.exising.type_name, 4)


def test_server_item_remove_not_existing(prod_client: FlaskClient):
    asserted_rq.delete(
        prod_client,
        f"/data/{assets.exising.type_name}/{5}",
    )

    named_asserts.space_did_not_change(prod_client)


def test_server_item_remove_not_existing_type(prod_client: FlaskClient):
    asserted_rq.delete(
        prod_client,
        f"/data/{assets.not_exising.type_name}/{4}",
        code=500,
    )

    named_asserts.space_did_not_change(prod_client)


## ================================================================================ ##
## spaces                                                                           ##
## ================================================================================ ##


def test_server_spaces_read(client: FlaskClient):
    spaces = asserted_rq.get(client, "/spaces")

    assert spaces == {
        "all": [
            assets.space_name,
            assets.space_name_second,
        ],
        "selected": assets.space_name,
    }


def test_server_spaces_set(client: FlaskClient):
    asserted_rq.put(
        client,
        "/spaces",
        json={"selected": assets.space_name_second},
    )

    spaces = asserted_rq.get(client, "/spaces")

    assert spaces == {
        "all": [
            assets.space_name,
            assets.space_name_second,
        ],
        "selected": assets.space_name_second,
    }

    initial_items = assets.initial_fsspace.items_file(assets.exising.type_name)
    current_items = assets.second_fsspace.items_file(assets.exising.type_name)

    actual_items = asserted_rq.get(client, f"/data/{assets.exising.type_name}")

    named_asserts.raw_items_eqaul_items_with_metadata(
        current_items,
        assets.exising.type_name,
        actual_items,
    )

    assert current_items != initial_items

    for item in initial_items:
        item["title"] += " from second space"

    assert current_items == initial_items


def test_server_spaces_set_invalid(prod_client: FlaskClient):
    all_spaces_names = [entry["name"] for entry in assets.spaces_config()["spaces"]]

    assert assets.space_name_invalid in all_spaces_names

    asserted_rq.put(
        prod_client, "/spaces", json={"selected": assets.space_name_invalid}, code=500
    )

    spaces = asserted_rq.get(prod_client, "/spaces")

    assert spaces == {
        "all": [
            assets.space_name,
            assets.space_name_second,
        ],
        "selected": assets.space_name,
    }


def test_server_spaces_set_not_existing(prod_client: FlaskClient):
    all_spaces_names = [entry["name"] for entry in assets.spaces_config()["spaces"]]

    assert assets.space_name_not_existing not in all_spaces_names

    asserted_rq.put(
        prod_client,
        "/spaces",
        json={"selected": assets.space_name_not_existing},
        code=500,
    )

    spaces = asserted_rq.get(prod_client, "/spaces")

    assert spaces == {
        "all": [
            assets.space_name,
            assets.space_name_second,
        ],
        "selected": assets.space_name,
    }
