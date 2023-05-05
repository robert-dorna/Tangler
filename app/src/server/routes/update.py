from flask import request, jsonify
from ...lib.api import Api


def update_route_handler():
    args = {**request.args}

    what = args.pop('what')
    _id = int(args.pop('_id'))

    api = Api()
    api.update(what, _id, values=args)

    response = jsonify({'status': 'ran update, success unknown'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response