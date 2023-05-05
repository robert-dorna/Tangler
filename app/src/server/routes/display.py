from flask import jsonify
from ...lib.core.files import read_yaml, CONFIG_PATH
from os import path


def display_route_handler(app):
    display = read_yaml(path.join(CONFIG_PATH, "_gui.yaml"))
    response = jsonify(display)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response