import os
from flask import request, jsonify
from ..app import app
from ...lib.api import Api



@app.route("/data/<what>", methods=['GET'])
def new_get_data_what(what):
    response = jsonify(Api().readall(what))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/data/<what>/<int:id>", methods=['GET'])
def new_get_data_what_id(what, id):
    response = jsonify(Api().read(what, id))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/data/<what>", methods=['POST'])
def new_post_data_what(what):
    new_item_id = Api().create(what, {**request.json})
    response = jsonify({'new_item_id': new_item_id})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/data/<what>/<int:id>", methods=['PATCH'])
def new_patch_data_what_id(what, id):
    Api().update(what, id, {**request.json})
    return new_get_data_what_id(what, id)


@app.route("/data/<what>/<int:id>", methods=['DELETE'])
def new_delete_data_what_id(what, id):
    Api().delete(what, id)
    response = jsonify({'response': 'ok (probably)'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response