from ....utils.algorithms import odict_inserted, odict_reordered, Placement
from collections.abc import Iterator
from .....library import types
from ....utils.file import JsonFile
from pathlib import Path


class LinksFile(JsonFile):
    DEFAULT_FILE_NAME = "_links.json"

    def __init__(self, space_path: str | Path, file_name: str = DEFAULT_FILE_NAME):
        super().__init__(Path(space_path) / file_name, on_init=self.load)

    def load(self, links: list[dict]) -> None:
        # TODO: validate links? make them typed?
        self.links: list[dict] = links

    def write(self, data=None) -> None:
        if data is not None:
            self.load(data)

        super().write(self.links)

    ## ================================================================================ ##
    ## types                                                                            ##
    ## ================================================================================ ##

    def remove_type(self, type_name: types.TypeName, *, cascade=False):
        remaining_links = []
        for link in self.links:
            parent_type_name, child_type_name = link["from"]["what"], link["to"]["what"]
            if parent_type_name == type_name or child_type_name == type_name:
                if not cascade and parent_type_name != child_type_name:
                    raise ValueError(
                        f'cannot delete type "{type_name}": items of other types are linked with "{type_name}" items'
                    )
            else:
                remaining_links.append(link)

        self.links = remaining_links

    def rename_type(self, type_name: types.TypeName, new_type_name: types.TypeName):
        if type_name == new_type_name:
            return

        for link in self.links:
            if link["from"]["what"] == type_name:
                link["from"]["what"] = new_type_name

            if link["to"]["what"] == type_name:
                link["to"]["what"] = new_type_name

    ## ================================================================================ ##
    ## links                                                                            ##
    ## ================================================================================ ##

    def list_links(self) -> Iterator[dict]:
        return (link for link in self.links)

    def index_link(self, parent: types.Item, child: types.Item) -> int:
        link = {
            "from": {
                "what": parent.full_id.type,
                "_id": parent.full_id.identifier,
            },
            "to": {
                "what": child.full_id.type,
                "_id": child.full_id.identifier,
            },
        }
        return self.links.index(link)

    def create_link(
        self, item: types.Item, reference: types.Item, relationship: types.Relationship
    ):
        new_link = {
            "to": {
                "what": item.full_id.type,
                "_id": item.full_id.identifier,
            },
        }

        if relationship == types.Relationship.CHILD:
            new_link["from"] = {
                "what": reference.full_id.type,
                "_id": reference.full_id.identifier,
            }

            self.links.append(new_link)

            item.parent = reference
            item.parent.children[item.full_id] = item

        else:
            if reference.parent is None:
                raise ValueError(
                    "internal Tangler error: cannot create a link with item that is top level"
                )

            new_link["from"] = {
                "what": reference.parent.full_id.type,
                "_id": reference.parent.full_id.identifier,
            }

            new_link_index = self.index_link(reference.parent, reference)
            if relationship == types.Relationship.BELOW:
                new_link_index += 1

            self.links.insert(new_link_index, new_link)

            item.parent = reference.parent
            item.parent.children = odict_inserted(
                item.parent.children,
                item,
                reference_key=reference.full_id,
                placement=Placement.BEFORE
                if relationship == types.Relationship.ABOVE
                else Placement.AFTER,
            )

    def remove_parent_link(self, item: types.Item):
        if item.parent is None:
            raise ValueError(
                "cannot unlink given item from parent as this item has no parent"
            )

        self.links.remove(
            {
                "from": {
                    "what": item.parent.full_id.type,
                    "_id": item.parent.full_id.identifier,
                },
                "to": {
                    "what": item.full_id.type,
                    "_id": item.full_id.identifier,
                },
            }
        )

        del item.parent.children[item.full_id]
        item.parent = None
