from dataclasses import dataclass
from collections.abc import Iterator
import operator
from pathlib import Path

from .... import types
from ....utils.file import YamlFile


class ConfigFile(YamlFile):
    """FilesystemSpace config file.

    WARNING: methods from this class return internally stored config that gets written to
    the actual file upon `write()` call. Therefore, do not modify results of those method
    calls to avoid invalidating internally stored config. Always copy() result before
    modifing it. Methods of this class do not return a copy() of the result for performance reasons.
    Also, don't modify value passed to `load()` TODO: remove this note if `load()` is safe.
    """

    DEFAULT_FILE_NAME = "_config.yaml"

    def __init__(
        self,
        space_path: str | Path,
        file_name: str = DEFAULT_FILE_NAME,
    ):
        super().__init__(Path(space_path) / file_name, on_init=self.load)

    def load(self, config: dict):
        self.config: types.Config = types.as_config(config)

    def write(self, data=None) -> None:
        if data is not None:
            self.load(data)

        super().write(types.from_config(self.config))

    ## ================================================================================ ##
    ## types order                                                                      ##
    ## ================================================================================ ##

    def get_types_order(self) -> list[types.TypeName]:
        return self.config.order

    def set_types_order(self, new_order: list[types.TypeName]) -> None:
        self.config.order = new_order

    def add_type_to_order(self, new_type_name: types.TypeName):
        if new_type_name not in self.config.order:
            self.config.order.append(new_type_name)

    def remove_type_from_order(self, type_name: types.TypeName):
        self.config.order.remove(type_name)

    ## ================================================================================ ##
    ## types                                                                            ##
    ## ================================================================================ ##

    def list_types_names(self) -> list[types.TypeName]:
        return list(self.config.types.keys())

    def list_types(self) -> list[types.Item.Type]:
        return [
            self.get_type(item_type_name) for item_type_name in self.list_types_names()
        ]

    def exists_type(self, type_name: types.TypeName) -> bool:
        return type_name in self.config.types

    def create_type(self, new_type: dict | types.Item.Type) -> None:
        if isinstance(new_type, dict):
            new_type = types.as_type(new_type)

        self.add_type_to_order(new_type.name)
        self.config.types[new_type.name] = new_type

    def set_type(self, new_item_type: types.Item.Type) -> None:
        raise NotImplemented

    def get_type(self, type_name: types.TypeName) -> types.Item.Type:
        return self.config.types[type_name]

    def rename_type(self, type_name: types.TypeName, new_type_name: types.TypeName):
        if type_name == new_type_name:
            return

        if self.exists_type(new_type_name):
            raise ValueError(
                f'rename of "{type_name}" item type failed because new name "{new_type_name}" already exists'
            )

        type_name_index = self.config.order.index(type_name)
        self.config.order[type_name_index] = new_type_name
        self.config.types[new_type_name] = self.config.types.pop(type_name)

    def update_type(
        self,
        type_name: types.TypeName,
        *,
        new_emoji: types.TypeEmoji | None = None,
        new_fields: types.TypeFields | None = None,
        new_template: types.TypeTemplate | None = None,
    ):
        type_config = self.config.types[type_name]

        if new_emoji is not None:
            type_config.emoji = new_emoji

        if new_fields is not None:
            type_config.fields = new_fields

        if new_template is not None:
            type_config.template = new_template

    def remove_type(self, type_name: types.TypeName):
        self.remove_type_from_order(type_name)
        del self.config.types[type_name]

    ## ================================================================================ ##
    ## fields                                                                           ##
    ## ================================================================================ ##

    def list_fields_names(self, type_name: types.TypeName) -> Iterator[types.FieldName]:
        return (field.name for field in self.get_type(type_name).fields)

    def list_fields(self, type_name: types.TypeName) -> list[types.Item.Type.Field]:
        return self.get_type(type_name).fields

    def index_field(
        self, type_name: types.TypeName, field_name: types.FieldName
    ) -> int:
        return operator.indexOf(self.list_fields_names(type_name), field_name)

    def exists_field(
        self, type_name: types.TypeName, field_name: types.FieldName
    ) -> bool:
        return field_name in self.list_fields_names(type_name)

    def create_field(
        self,
        type_name: types.TypeName,
        new_field: types.Item.Type.Field,
        *,
        _check_if_exists: bool = True,
    ):
        if _check_if_exists and self.exists_field(type_name, new_field.name):
            raise ValueError("field already exists")

        self.get_type(type_name).fields.append(new_field)

    def set_field(self, type_name: types.TypeName, new_field: types.Item.Type.Field):
        try:
            field_index = self.index_field(type_name, new_field.name)
            self.get_type(type_name).fields[field_index] = new_field
        except ValueError:
            self.create_field(type_name, new_field, _check_if_exists=False)

    def get_field(
        self, type_name: types.TypeName, field_name: types.FieldName
    ) -> types.Item.Type.Field:
        for field in self.list_fields(type_name):
            if field.name == field_name:
                return field

        raise KeyError("no such field")

    def rename_field(
        self,
        type_name: types.TypeName,
        field_name: types.FieldName,
        new_field_name: types.FieldName,
    ):
        if field_name == new_field_name:
            return

        if field_name == "title":
            raise ValueError(
                "cannot rename field 'title', this field is special and required (for now, in future version it may be possible)"
            )

        if self.exists_field(type_name, new_field_name):
            raise ValueError(
                f'for type "{type_name}" cannot rename field from "{field_name}" to "{new_field_name}" as the latter is already taken'
            )

        field = self.get_field(type_name, field_name)
        field.name = new_field_name

    def update_field(
        self,
        type_name: types.TypeName,
        field_name: types.FieldName,
        *,
        new_required: types.FieldRequired | None = None,
        new_values: types.FieldValues | None = None,
        new_width: types.FieldWidth | None = None,
    ):
        field = self.get_field(type_name, field_name)

        if new_required is not None:
            field.required = new_required

        if new_values is not None:
            field.values = new_values

        if new_width is not None:
            field.width = new_width

    def remove_field(self, type_name: types.TypeName, field_name: types.FieldName):
        if field_name == "title":
            raise ValueError(
                'cannot remove field "title" as for now this field is special and required'
            )

        field_index = self.index_field(type_name, field_name)
        item_type = self.get_type(type_name)
        del item_type.fields[field_index]
