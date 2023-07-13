from __future__ import annotations
from collections import OrderedDict
from enum import Enum
from typing import NewType, TypeAlias, Any
from pydantic import BaseModel, ConfigDict


FieldValuesTypeName = NewType("FieldValuesTypeName", str)
FieldValuesEnum: TypeAlias = dict[str, str]
FieldWidthConstant = NewType("FieldWidthConstant", int)
FieldWidthMode = NewType("FieldWidthMode", bool)
# above width mode is either "auto" or "none", now true/false

FieldName = NewType("FieldName", str)
FieldRequired = NewType("FieldRequired", bool)
FieldValues: TypeAlias = FieldValuesTypeName | FieldValuesEnum
FieldWidth: TypeAlias = FieldWidthConstant | FieldWidthMode

FieldValue: TypeAlias = Any

TypeName = NewType("TypeName", str)
TypeEmoji = NewType("TypeEmoji", str)
TypeFields: TypeAlias = list["Item.Type.Field"]
TypeTemplate = NewType("TypeTemplate", str)

ItemIdentifier = NewType("ItemIdentifier", int)
ItemFields: TypeAlias = dict[FieldName, FieldValue]


class Item(BaseModel):
    class FullId(BaseModel):
        type: Item.Type
        identifier: ItemIdentifier

        def __hash__(self):
            return hash((self.type.name, self.identifier))

    model_config = ConfigDict(strict=True, extra="forbid")

    full_id: FullId
    fields: ItemFields
    parent: Item | None = None
    children: OrderedDict[FullId, Item] = OrderedDict()

    class Type(BaseModel):
        model_config = ConfigDict(strict=True, extra="forbid")

        name: TypeName
        emoji: TypeEmoji
        fields: TypeFields
        template: TypeTemplate

        class Field(BaseModel):
            model_config = ConfigDict(strict=True, extra="forbid")

            name: FieldName
            required: FieldRequired
            values: FieldValues
            width: FieldWidth


class Config(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    formatters: dict
    order: list[TypeName]
    types: dict[TypeName, Item.Type]


def as_field(data: dict) -> Item.Type.Field:
    data = data.copy()

    name = data.pop("name")
    required = data.pop("required")
    values = data.pop("values")
    width = data.pop("width")

    if data:
        unknown_fields = list(data.keys())
        raise ValueError(f"unknown keys in type fields: {unknown_fields}")

    if name[0] == "_":
        raise ValueError("field name cannot start with an underscore")

    return Item.Type.Field(
        name=name,
        required=required,
        values=values,
        width=width,
    )


def from_field(field: Item.Type.Field) -> dict:
    return {
        "name": field.name,
        "required": field.required,
        "values": field.values,
        "width": field.width,
    }


def as_type(data: dict) -> Item.Type:
    name = data.pop("name")
    emoji = data.pop("emoji")
    fields = data.pop("fields")
    template = data.pop("template")

    if data:
        unknown_fields = list(data.keys())
        raise ValueError(f"unknown keys in type: {unknown_fields}")

    if name[0] == "_":
        raise ValueError("type name cannot start with an underscore")

    return Item.Type(
        name=name,
        emoji=emoji,
        fields=[as_field(datum) for datum in fields],
        template=template,
    )


def from_type(type: Item.Type) -> dict:
    return {
        # "name": type.name,
        "emoji": type.emoji,
        "fields": [from_field(datum) for datum in type.fields],
        "template": type.template,
    }


def as_item(data: dict, item_type: Item.Type) -> Item:
    item_id = data.pop("_id")

    for key in data.keys():
        if key[0] == "_":
            raise ValueError(
                "unknown special (starting with underscore) item field value"
            )

    return Item(
        full_id=Item.FullId(type=item_type, identifier=item_id),
        fields=data,
    )


def from_item(item: Item, *, include_metadata=True) -> dict:
    as_dict: dict[Any, Any] = {
        "_id": item.full_id.identifier,
        **item.fields,
    }

    if include_metadata:
        as_dict["_children"] = ([from_item(child) for child in item.children.values()],)
        as_dict["_what"] = (item.full_id.type.name,)

    return as_dict


def as_config(data: dict) -> Config:
    # if data contains more keys it is an error (same for other conversions)
    return Config(
        formatters=data["formatters"],
        order=data["order"],
        types={k: as_type({**v, "name": k}) for k, v in data["types"].items()},
    )


def from_config(config: Config) -> dict:
    return {
        "formatters": config.formatters,
        "order": config.order,
        "types": {k: from_type(v) for k, v in config.types.items()},
    }


class Relationship(Enum):
    ABOVE = 1
    BELOW = 2
    CHILD = 3


def as_relationship(relationship: str) -> "Relationship":
    match relationship:
        case "above":
            return Relationship.ABOVE
        case "below":
            return Relationship.BELOW
        case "child":
            return Relationship.CHILD
        case _:
            raise ValueError("unrecognized relationship value")
