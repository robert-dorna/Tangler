from flask import jsonify
from ...lib.core.files import read_yaml, CONFIG_PATH


def display_route_handler():
    display = read_yaml(CONFIG_PATH)
    response = jsonify(display)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response