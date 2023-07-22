from collections import OrderedDict
from pathlib import Path

from .....library import types
from ....utils.algorithms import odict_reordered, Placement
from ....utils.file import JsonFile


class ItemsFile(JsonFile):
    @classmethod
    def get_file_name(cls, type_name: types.TypeName) -> str:
        return f"{type_name}.json"

    def __init__(
        self,
        space_path: str | Path,
        items_type: types.Item.Type,
        *,
        allowExisting=True,
        reset=False,
    ):
        self.items_type = items_type
        self.items: OrderedDict[types.ItemIdentifier, types.Item] = OrderedDict()

        path = Path(space_path) / self.get_file_name(items_type.name)

        if not allowExisting and path.exists():
            raise RuntimeError("items file already exists (not allowed)")

        super().__init__(
            path,
            initializer=[] if reset or not path.exists() else None,
            on_init=self.load,
        )

    def load(self, items):
        try:
            self.items = OrderedDict(
                (item["_id"], types.as_item(item, self.items_type)) for item in items
            )
        except ValueError as e:
            raise ValueError(f"while loading file: {self.path} got an error: {str(e)}")

    def write(self, data=None) -> None:
        if data is not None:
            self.load(data)

        super().write(
            list(
                types.from_item(item, include_metadata=False)
                for item in self.items.values()
            )
        )

    def rename_by_type_name(self, new_type_name: types.TypeName) -> None:
        return super().rename(self.get_file_name(new_type_name))

    ## ================================================================================ ##
    ## items                                                                            ##
    ## ================================================================================ ##

    def reset(self):
        pass

    def list_root_items(self) -> list[types.Item]:
        return [item for item in self.items.values() if item.parent is None]

    def exists_item(self, item_id: types.ItemIdentifier) -> bool:
        return item_id in self.items

    def create_item(self, new_item: types.Item):
        new_id = types.ItemIdentifier(1)
        if len(self.items) > 0:
            new_id = types.ItemIdentifier(
                max(item.full_id.identifier for item in self.items.values()) + 1
            )

        new_item.full_id.identifier = new_id
        self.items[new_id] = new_item

    def move_item(
        self, item: types.Item, reference: types.Item, relationship: types.Relationship
    ):
        # warning, this call does not remove possibly existing previous item.parent link,
        # so make sure you remove such if exists
        self.items = odict_reordered(
            self.items,
            item.full_id.identifier,
            reference_key=reference.full_id.identifier,
            placement=Placement.BEFORE
            if relationship == types.Relationship.ABOVE
            else Placement.AFTER,
        )

    def get_item(self, item_id: types.ItemIdentifier) -> types.Item:
        return self.items[item_id]

    def update_item(self, item: types.Item, fields: types.ItemFields):
        for field_name, new_field_value in fields.items():
            if (
                isinstance(new_field_value, dict)
                and field_name in item.fields
                and isinstance(item.fields[field_name], dict)
            ):
                item.fields[field_name].update(
                    {k: v for k, v in new_field_value if v is not None}
                )
            else:
                item.fields[field_name] = new_field_value

    def remove_item(self, item: types.Item):
        del self.items[item.full_id.identifier]

    ## ================================================================================ ##
    ## fields                                                                           ##
    ## ================================================================================ ##

    def rename_field(
        self, field_name: types.FieldName, new_field_name: types.FieldName
    ):
        if field_name == new_field_name:
            return

        for item in self.items.values():
            if field_name in item.fields:
                item.fields[new_field_name] = item.fields.pop(field_name)

    def remove_field(self, field_name: types.FieldName):
        if field_name == "title":
            raise ValueError(
                'cannot remove field "title" as for now this field is special and required'
            )

        for item in self.items.values():
            if field_name in item.fields:
                item.fields.pop(field_name)
