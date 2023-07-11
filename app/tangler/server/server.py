from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeAlias

from flask import Flask, Response, jsonify, request
from werkzeug.exceptions import BadRequest

from ..library import types
from ..library.spaces.config import SpacesConfig
from ..library.spaces.filesystem.space import FilesystemSpace
from .logging import configure as configure_logging

configure_logging()


def as_response(
    result: types.Config
    | types.Item.Type.Field
    | types.Item.Type
    | types.Item
    | list
    | dict
    | None,
) -> Response:
    if isinstance(result, types.Config):
        result = types.from_config(result)
    elif isinstance(result, types.Item.Type.Field):
        result = types.from_field(result)
    elif isinstance(result, types.Item.Type):
        result = types.from_type(result)
    elif isinstance(result, types.Item):
        result = types.from_item(result)

    # TODO: enable CORS(app), smth like that
    # TODO: turn it into a decorator
    response = jsonify(
        {
            "result_summary": "request processed",
            "result": result,
        }
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


class Server:
    """Tangler REST Server.

    It simply exposes `library.spaces.FilesystemSpace` api through `flask`,
    and makes some operations idempotent (e.g. normally `FilesystemSpace.remove_type` fails if type does not exist, here it is a no-op).
    """

    RequestHandler: TypeAlias = Callable[..., Response]

    def __init__(self, spaces_config: str | Path | SpacesConfig):
        """Initializes `Server`."""

        if not isinstance(spaces_config, SpacesConfig):
            spaces_config = SpacesConfig(spaces_config)

        self.spaces_config = spaces_config
        self.space = FilesystemSpace(
            self.spaces_config.path.parent
            / self.spaces_config.config["spaces"][0]["directory"]
        )

        self.app = Flask(__name__)
        self.app.register_error_handler(BadRequest, self._jsonify_exception)

        # not sure if POST by some convention should not have <what> (new resource name) in URL but in params instead

        rules: list[tuple[str, str, Server.RequestHandler]] = [
            # spaces
            # >
            # > todo
            # >
            # config
            ("/config", "GET", self.get_config),
            ("/config/<section>", "GET", self.get_config_section),
            ("/config/order", "PUT", self.set_types_order),
            # config -- type
            ("/config/types/<what>", "POST", self.create_type),
            ("/config/types/<what>", "PUT", self.set_type),
            ("/config/types/<what>", "GET", self.get_type),
            ("/config/types/<what>", "PATCH", self.update_type),
            ("/config/types/<what>", "DELETE", self.remove_type),
            # config -- field
            ("/config/fields/<what>", "GET", self.get_fields),
            ("/config/fields/<what>/<field>", "POST", self.create_field),
            ("/config/fields/<what>/<field>", "PUT", self.set_field),
            ("/config/fields/<what>/<field>", "GET", self.get_field),
            ("/config/fields/<what>/<field>", "PATCH", self.update_field),
            ("/config/fields/<what>/<field>", "DELETE", self.remove_field),
            # data
            ("/data/<what>", "GET", self.get_items),
            ("/data/<what>", "POST", self.create_item),
            ("/data/<what>/<int:id>", "GET", self.get_item),
            ("/data/<what>/<int:id>", "PATCH", self.update_item),
            ("/data/<what>/<int:id>", "DELETE", self.remove_item),
        ]

        for path, method, handler in rules:
            self.app.add_url_rule(path, methods=[method], view_func=handler)

        # note about: /data/<what> POST vs /config/types/<what> POST (and /config/fields)
        # this is not consistant with config POST as this one does not have exactly the same
        # path as the resulting (new/being created) resource.
        # idk if it should be made consistent or leaved as that.

        # TODO: also, jsonify() every single response so it does not
        # have to be repeated in handlers.
        # (and if it is a type from types., from from_TYPE() on the result first,
        # then jsonify)

    def run(self):
        self.app.run(host="0.0.0.0", port=8000)

    def _jsonify_exception(self, e: Any) -> Response:
        """Return JSON instead of HTML for HTTP errors."""

        response = e.get_response()
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    ## ================================================================================ ##
    ## config                                                                           ##
    ## ================================================================================ ##

    def get_config(self) -> Response:
        result = self.space.get_config()
        return as_response(result)

    def get_config_section(self, section: str) -> Response:
        result = types.from_config(self.space.get_config())[section]
        return as_response(result)

    ## ================================================================================ ##
    ## config - types order                                                             ##
    ## ================================================================================ ##

    def set_types_order(self) -> Response:
        data = request.json
        if not isinstance(data, list):
            raise ValueError("request should have a json list as body")

        self.space.set_types_order(data)
        result = self.space.get_types_order()
        return as_response(result)

    ## ================================================================================ ##
    ## config - types                                                                   ##
    ## ================================================================================ ##

    def create_type(self, what: str) -> Response:
        data = request.json
        if not isinstance(data, dict):
            raise ValueError("request should have a json dict as body")

        self.space.create_type(types.as_type({**data, "name": what}))
        return self.get_type(what)

    def set_type(self, what: str) -> Response:
        data = request.json
        if not isinstance(data, dict):
            raise ValueError("request should have a json dict as body")

        self.space.set_type(types.as_type({**data, "name": what}))
        return self.get_type(what)

    def get_type(self, what: str) -> Response:
        result = self.space.get_type(types.TypeName(what))
        return as_response(result)

    def update_type(self, what: str) -> Response:
        data = request.json
        if not isinstance(data, dict):
            raise ValueError("request should have a json dict as body")

        self.space.update_type(
            types.TypeName(what),
            new_name=data.pop("name", None),
            new_emoji=data.pop("emoji", None),
            new_fields=data.pop("fields", None),
            new_template=data.pop("template", None),
        )
        return self.get_type(what)

    def remove_type(self, what: str) -> Response:
        if self.space.exists_type(types.TypeName(what)):
            self.space.remove_type(types.TypeName(what))
        return as_response(None)

    ## ================================================================================ ##
    ## config - fields                                                                  ##
    ## ================================================================================ ##

    def get_fields(self, what: str) -> Response:
        result = self.space.list_fields(types.TypeName(what))
        return as_response(result)

    def create_field(self, what: str, field: str) -> Response:
        data = request.json
        if not isinstance(data, dict):
            raise ValueError("request should have a json dict as body")

        self.space.create_field(
            types.TypeName(what), types.as_field({**data, "name": field})
        )
        return self.get_field(what, field)

    def set_field(self, what: str, field: str) -> Response:
        data = request.json
        if not isinstance(data, dict):
            raise ValueError("request should have a json dict as body")

        self.space.set_field(
            types.TypeName(what), types.as_field({**data, "name": field})
        )
        return self.get_field(what, field)

    def get_field(self, what: str, field: str) -> Response:
        result = self.space.get_field(types.TypeName(what), types.FieldName(field))
        return as_response(result)

    def update_field(self, what: str, field: str) -> Response:
        data = request.json
        if not isinstance(data, dict):
            raise ValueError("request should have a json dict as body")

        self.space.update_field(
            types.TypeName(what),
            types.FieldName(field),
            new_name=data.pop("name", None),
            new_required=data.pop("required", None),
            new_values=data.pop("values", None),
            new_width=data.pop("width", None),
        )
        return self.get_field(what, field)

    def remove_field(self, what: str, field: str) -> Response:
        if self.space.exists_field(types.TypeName(what), types.FieldName(field)):
            self.space.remove_field(types.TypeName(what), types.FieldName(field))
        return as_response(None)

    ## ================================================================================ ##
    ## items                                                                            ##
    ## ================================================================================ ##

    def get_items(self, what: str) -> Response:
        result = self.space.list_root_items(types.TypeName(what))
        return as_response(result)

    def create_item(self, what: str) -> Response:
        data = request.json
        if not isinstance(data, dict):
            raise ValueError("request should have a json dict as body")

        place: dict = data.pop("_place", None)

        item_type = self.space.get_type(types.TypeName(what))

        result = self.space.create_item(
            item_type.name, types.as_item(data, item_type), place
        )
        return as_response(result)

    def get_item(self, what: str, id: int) -> Response:
        result = self.space.get_item(types.TypeName(what), types.ItemIdentifier(id))
        return as_response(result)

    def update_item(self, what: str, id: int) -> Response:
        data = request.json
        if not isinstance(data, dict):
            raise ValueError("request should have a json dict as body")

        place: dict = data.pop("_place", None)

        self.space.update_item(
            types.TypeName(what),
            types.ItemIdentifier(id),
            fields=data,  # NOTE: probably wrong
            place=place,
        )
        return self.get_item(what, id)

    def remove_item(self, what: str, id: int) -> Response:
        if self.space.exists_item(types.TypeName(what), types.ItemIdentifier(id)):
            self.space.remove_item_by_id(types.TypeName(what), types.ItemIdentifier(id))
        return as_response(None)
