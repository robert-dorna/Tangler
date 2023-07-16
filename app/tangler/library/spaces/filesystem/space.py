from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from ....library import types
from ..space import Space
from .files import ConfigFile, ItemsFile, LinksFile


@dataclass
class FilesystemSpaceFiles:
    config: ConfigFile
    links: LinksFile
    items: dict[types.TypeName, ItemsFile]


class FilesystemSpace(Space):
    def __init__(self, space_path: str | Path):
        super().__init__(space_path)

        self.files = FilesystemSpaceFiles(
            config=ConfigFile(space_path),
            links=LinksFile(space_path),
            items={},
        )

        self.files.items = {
            item_type.name: ItemsFile(space_path, item_type)
            for item_type in self.list_types()
        }

        for link in self.files.links.list_links():
            parent_info, child_info = link["from"], link["to"]

            child = self.files.items[child_info["what"]].get_item(child_info["_id"])
            if child.parent is not None:
                raise ValueError(
                    "link breaks one-parent tree rule or redefines existing link"
                )
            parent = self.files.items[parent_info["what"]].get_item(parent_info["_id"])

            parent.children[child.full_id] = child
            child.parent = parent

    ## ================================================================================ ##
    ## config                                                                           ##
    ## ================================================================================ ##

    def get_config(self) -> types.Config:
        if self.files.config.config is None:
            raise ValueError("Config is missing")
        return self.files.config.config

    ## ================================================================================ ##
    ## config - types order                                                             ##
    ## ================================================================================ ##

    def set_types_order(self, new_order: list[types.TypeName]) -> None:
        self.files.config.set_types_order(new_order)
        self.files.config.write()

    def get_types_order(self) -> list[types.TypeName]:
        return self.files.config.get_types_order()

    ## ================================================================================ ##
    ## config - types                                                                   ##
    ## ================================================================================ ##

    def exists_type(self, type_name: types.TypeName) -> bool:
        # TODO: check for partial existing? e.g. file handle present or .json file present?
        return self.files.config.exists_type(type_name)

    def list_types_names(self) -> list[types.TypeName]:
        return self.files.config.list_types_names()

    def list_types(self) -> list[types.Item.Type]:
        return self.files.config.list_types()

    def create_type(self, new_type: types.Item.Type) -> None:
        if self.exists_type(new_type.name):
            raise ValueError(f"type {new_type.name} already exists")

        if new_type.name in self.files.items:
            raise RuntimeError(
                f"type {new_type.name} does not exist but space already has a .json file handle"
            )

        self.files.config.create_type(new_type)
        self.files.config.write()

        self.files.items[new_type.name] = ItemsFile(
            space_path=self.path,
            items_type=new_type,
            allowExisting=True,
            reset=False,
        )

    def set_type(self, new_type: types.Item.Type) -> None:
        # TODO: check if this is correct, I just copied create without much thinking
        # do not cross reference this with old set handler, just analize current code meaning and sense

        self.files.config.set_type(new_type)
        self.files.config.write()

        self.files.items[new_type.name] = ItemsFile(
            space_path=self.path,
            items_type=new_type,
            allowExisting=True,
            reset=True,
        )

    def get_type(self, type_name: types.TypeName) -> types.Item.Type:
        return self.files.config.get_type(type_name)

    def rename_type(
        self, type_name: types.TypeName, new_type_name: types.TypeName
    ) -> None:
        if type_name == new_type_name:
            return

        self.files.config.rename_type(type_name, new_type_name)
        self.files.config.write()

        self.files.links.rename_type(type_name, new_type_name)
        self.files.links.write()

        self.files.items[new_type_name] = self.files.items.pop(type_name)
        self.files.items[new_type_name].rename_by_type_name(new_type_name)

    def update_type(
        self,
        type_name: types.TypeName,
        *,
        new_name: types.TypeName | None = None,
        new_emoji: types.TypeEmoji | None = None,
        new_fields: types.TypeFields | None = None,
        new_template: types.TypeTemplate | None = None,
    ):
        if not self.exists_type(type_name):
            raise ValueError(f"type '{type_name}' does not exist")

        if new_name is not None:
            self.rename_type(type_name, new_name)
            type_name = new_name

        self.files.config.update_type(
            type_name,
            new_emoji=new_emoji,
            new_fields=new_fields,
            new_template=new_template,
        )
        self.files.config.write()

        # Currently we don't update items (data) and do not care if some
        # existing entries become invalid. We also do not try to convert any
        # already existing values to a new field type etc. Everything in .json
        # just stays as it was defined previously.

        # also, notes about performance and safety:
        # todo: this entire set of not atomic operations is very bad and error prone
        # e.g. an error <somewhere> (lets say permission denied) will result in partial resource rename and maybe "unrecoverable" (conveniently) state

    def remove_type(self, type_name: types.TypeName):
        # NOTE: from previous handler:
        # terrible again: no locks, no transactions, shit performance etc.
        # probably should move soon to NoSQL (probably best option), or SQL, or implement DATADIR support properly
        # (I guess ideally NoSQL + DATADIR implemented properly to have two options for convenience but that
        # will most probably require a lot more maintainance and overall commitment)
        # (btw. this entire loop is horrible, refactor it no matter what, it's already too much with this CORS
        # duplications, ulgy response constructions, and raw plus poorly chosen exceptions; to name a few)

        self.files.links.remove_type(type_name, cascade=False)
        self.files.links.write()

        self.files.config.remove_type(type_name)
        self.files.config.write()

        if type_name in self.files.items:
            self.files.items[type_name].remove()
            del self.files.items[type_name]

    ## ================================================================================ ##
    ## config - fields                                                                  ##
    ## ================================================================================ ##

    def exists_field(
        self, type_name: types.TypeName, field_name: types.FieldName
    ) -> bool:
        return self.files.config.exists_field(type_name, field_name)

    def list_fields_names(self, type_name: types.TypeName) -> Iterator[types.FieldName]:
        return self.files.config.list_fields_names(type_name)

    def list_fields(self, type_name: types.TypeName) -> list[types.Item.Type.Field]:
        return self.files.config.list_fields(type_name)

    def create_field(
        self, type_name: types.TypeName, new_field: types.Item.Type.Field
    ) -> None:
        self.files.config.create_field(type_name, new_field)
        self.files.config.write()

    def set_field(self, type_name: types.TypeName, new_field: types.Item.Type.Field):
        self.files.config.set_field(type_name, new_field)
        self.files.config.write()
        # some old notes (first is valid, second idk)
        # todo: "required" spec checking and updating {what}.json
        # idea: raise an error if name is specified in json but differs from path's <field>

    def get_field(
        self, type_name: types.TypeName, field_name: types.FieldName
    ) -> types.Item.Type.Field:
        return self.files.config.get_field(type_name, field_name)

    def rename_field(
        self,
        type_name: types.TypeName,
        field_name: types.FieldName,
        new_field_name: types.FieldName,
    ) -> None:
        if field_name == new_field_name:
            return

        self.files.config.rename_field(type_name, field_name, new_field_name)
        self.files.config.write()

        self.files.items[type_name].rename_field(field_name, new_field_name)
        self.files.items[type_name].write()

    def update_field(
        self,
        type_name: types.TypeName,
        field_name: types.FieldName,
        *,
        new_name: types.FieldName | None = None,
        new_required: types.FieldRequired | None = None,
        new_values: types.FieldValues | None = None,
        new_width: types.FieldWidth | None = None,
    ) -> None:
        if not self.exists_field(type_name, field_name):
            raise ValueError("can't update field which does not exist")

        if new_name is not None:
            self.rename_field(type_name, field_name, new_name)
            field_name = new_name

        self.files.config.update_field(
            type_name,
            field_name,
            new_required=new_required,
            new_values=new_values,
            new_width=new_width,
        )
        self.files.config.write()

    def remove_field(
        self, type_name: types.TypeName, field_name: types.FieldName
    ) -> None:
        self.files.config.remove_field(type_name, field_name)
        self.files.config.write()

        self.files.items[type_name].remove_field(field_name)
        self.files.items[type_name].write()

    ## ================================================================================ ##
    ## items                                                                            ##
    ## ================================================================================ ##

    def exists_item(
        self, type_name: types.TypeName, item_id: types.ItemIdentifier
    ) -> bool:
        return self.files.items[type_name].exists_item(item_id)

    def list_root_items(self, type_name: types.TypeName) -> list[types.Item]:
        return self.files.items[type_name].list_root_items()

    def move_item(
        self,
        item: types.Item,
        reference: types.Item,
        relationship: types.Relationship,
        *,
        _ommit_existing_link_removal=False,
    ):
        updated_links = False

        if not _ommit_existing_link_removal:
            if item.parent is not None:
                self.files.links.remove_parent_link(item)
                updated_links = True

        if relationship != types.Relationship.CHILD and reference.parent is None:
            if item.full_id.type != reference.full_id.type:
                raise ValueError(
                    "cannot move item above or below top level item of different type"
                )

            self.files.items[item.full_id.type.name].move_item(
                item, reference, relationship
            )
            self.files.items[item.full_id.type.name].write()
        else:
            self.files.links.create_link(item, reference, relationship)
            updated_links = True

        if updated_links:
            self.files.links.write()

    def _parse_place(self, place: dict) -> tuple[types.Relationship, types.Item]:
        relationship = types.as_relationship(place["relationship"])
        reference_info = place["reference"]
        reference = self.files.items[reference_info["what"]].get_item(
            reference_info["_id"]
        )
        return relationship, reference

    def create_item(
        self, type_name: types.TypeName, new_item: types.Item, place: dict | None = None
    ) -> types.Item:
        new_item = new_item.model_copy(deep=True)
        self.files.items[type_name].create_item(new_item)
        self.files.items[type_name].write()

        if place:
            relationship, reference = self._parse_place(place)
            self.move_item(
                new_item, reference, relationship, _ommit_existing_link_removal=True
            )

        return new_item

    def get_item(
        self, type_name: types.TypeName, item_id: types.ItemIdentifier
    ) -> types.Item:
        return self.files.items[type_name].get_item(item_id)

    def update_item(
        self,
        type_name: types.TypeName,
        item_id: types.ItemIdentifier,
        *,
        fields: types.ItemFields | None = None,
        place: dict | None = None,
    ) -> None:
        item = self.get_item(type_name, item_id)

        if place is not None:
            relationship, reference = self._parse_place(place)
            self.move_item(item, reference, relationship)

        if fields is not None:
            self.files.items[type_name].update_item(item, fields)
            self.files.items[type_name].write()

    def remove_item_by_id(
        self, type_name: types.TypeName, item_id: types.ItemIdentifier
    ):
        item = self.get_item(type_name, item_id)
        return self.remove_item(item)

    def remove_item(self, item: types.Item):
        for child in item.children.values():
            self.remove_item(child)

        if item.parent is not None:
            self.files.links.remove_parent_link(item)
            self.files.links.write()

        self.files.items[item.full_id.type.name].remove_item(item)
        self.files.items[item.full_id.type.name].write()
