import os
from flask import request, jsonify
from ..app import app
from ...lib.core.files import read_yaml, write_yaml, read_json, write_json, DATADIR_PATH, CONFIG_PATH


@app.route("/config", methods=['GET'])
def new_get_config():
    response = jsonify(read_yaml(CONFIG_PATH))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/config/<section>", methods=['GET'])
def new_get_config_section(section):
    response = jsonify(read_yaml(CONFIG_PATH)[section])
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/config/types/<what>", methods=['GET'])
def new_get_config_types_what(what):
    response = jsonify(read_yaml(CONFIG_PATH)['types'][what])
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/config/order", methods=['PUT'])
def new_put_config_order():
    config = read_yaml(CONFIG_PATH)
    config['order'] = request.json  

    write_yaml(CONFIG_PATH, config)

    response = jsonify({'response': 'ok (probably)'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/config/types/<what>", methods=['POST'])
def new_post_config_types_what(what):
    config = read_yaml(CONFIG_PATH)
    if what in config['types']:
      raise ValueError(f'item type {what} already exists')

    config['types'][what] = {**request.json}
    write_yaml(CONFIG_PATH, config)

    response = jsonify({'response': 'ok (probably)'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/config/types/<what>", methods=['PATCH'])
def new_patch_config_types_what(what):
    args = {**request.json}

    config = read_yaml(CONFIG_PATH)
    if what not in config['types']:
      raise ValueError(f'item type {what} does not exists')

    config['types'][what] = config['types'][what] | args
    write_yaml(CONFIG_PATH, config)

    response = jsonify({'response': 'ok (probably)'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/config/types/<what>", methods=['DELETE'])
def new_delete_config_types_what(what):
    config = read_yaml(CONFIG_PATH)
    del config['types'][what]

    write_yaml(CONFIG_PATH, config)

    response = jsonify({'response': 'ok (probably)'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response