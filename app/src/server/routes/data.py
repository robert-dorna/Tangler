from flask import request, jsonify
from ...lib.api import Api


# SOCKETS, WebSockets/Socket.IO,
# RAW, RPC, SOAP, REST, GraphQL
def data_route_handler(app):

    args = {**request.args}

    if 'index' in args:
        args['index'] = int(args['index'])
    if '_id' in args:
        args['_id'] = int(args['_id'])

    app.logger.info('args: %s', args)

    api = Api()
    method = args.pop('method') if 'method' in args else 'read'
    method = getattr(api, method)

    what = args.pop('what')if 'what' in args else 'task'
    if ',' in what:
        what = what.split(',')

    app.logger.info('calling with')
    app.logger.info(' > what: %s', what)
    app.logger.info(' > args: %s', args)

    if isinstance(what, list):
        result = {w: method(what=w, **args) for w in what}
    else:
        result = method(what=what, **args)

    # data.flush()

    success = True  # todo, way to check from Data that it was updated
    response = jsonify(
        {'status': 'ran method, success unknown', 'result': result} if success else
        {'status': 'error'}
    )

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response