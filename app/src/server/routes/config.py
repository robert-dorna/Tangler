from flask import request, jsonify
from ..app import app
from ...lib.core.files import read_yaml, write_yaml, CONFIG_PATH


@app.route("/config", methods=['GET'])
def get_config():
    response = jsonify(read_yaml(CONFIG_PATH))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/config/<section>", methods=['GET'])
def get_config_section(section):
    response = jsonify(read_yaml(CONFIG_PATH)[section])
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/config/order", methods=['PUT'])
def set_config_order():
    config = read_yaml(CONFIG_PATH)
    config['order'] = request.json  

    write_yaml(CONFIG_PATH, config)

    response = jsonify({'response': 'ok (probably)'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response