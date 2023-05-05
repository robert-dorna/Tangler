from flask import request, jsonify
from ...lib.api import Api


def unlink_route_handler():
    args = {**request.args}

    what = args.pop('what')
    id = int(args.pop('_id'))

    api = Api()

    parent_data = api.parent(what, id)
    if parent_data:
        _, parent = parent_data
        api.unlink(parent['_what'], parent['_id'], what, id)

    response = jsonify({'status': 'ran unlink, success unknown'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response