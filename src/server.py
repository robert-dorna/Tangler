from flask import abort, Flask, jsonify, request, Response
from .api import Api
from .core.files import read_yaml, CONFIG_PATH
from logging.config import dictConfig
from os import path, listdir
from werkzeug.exceptions import BadRequest
import json


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)


@app.errorhandler(BadRequest)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


# SOCKETS, WebSockets/Socket.IO,
# RAW, RPC, SOAP, REST, GraphQL
@app.route("/data")
def update_task():

    args = {**request.args}

    if 'index' in args:
        args['index'] = int(args['index'])
    if '_id' in args:
        args['_id'] = int(args['_id'])

    app.logger.info('args: %s', args)

    api = Api()
    method = args.pop('method') if 'method' in args else 'read'
    method = getattr(api, method)

    what = args.pop('what') if 'what' in args else 'task'
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


@app.route('/update')
def update():
    args = {**request.args}

    what = args.pop('what')
    _id = int(args.pop('_id'))

    api = Api()
    api.update(what, _id, values=args)

    response = jsonify({'status': 'ran update, success unknown'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/create')
def create():
    args = {**request.args}

    args.pop('_children')

    what = args.pop('_what')
    above = {
        '_id': int(args.pop('_aboveId')),
        'what': args.pop('_aboveWhat'),
    }

    api = Api()
    api.read_links()

    try:
        i, link = next((i, v)
                       for i, v in enumerate(api.links) if v['to'] == above)
        newId = api.create(what, values=args)
        new_link = {'from': link['from'], 'to': {'_id': newId, 'what': what}}
        api.links.insert(i, new_link)
        api.write_links()
    except StopIteration:
        i, _ = api.read(above['what'], above['_id'])
        api.create(what, index=i, values=args)

    response = jsonify({'status': 'ran craete, success unknown'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/move")
def move():
    args = {**request.args}

    location = args.pop('location')
    what = args.pop('what')
    id = int(args.pop('id'))
    to_what = args.pop('to_what')
    to_id = int(args.pop('to_id'))

    api = Api()

    if api.parent(to_what, to_id) is None and what != to_what and location != "child":
        abort(400)

    parent_data = api.parent(what, id)
    if parent_data:
        app.logger.info('unlinking source')
        _, parent = parent_data
        api.unlink(parent['_what'], parent['_id'], what, id)

    app.logger.info('location is %s', location)
    if location == "child":
        app.logger.info('location is child')
        api.link(to_what, to_id, what, id)
    else:
        app.logger.info('location is not child')
        parent_data = api.parent(to_what, to_id)
        if parent_data is None:
            app.logger.info('"to" parent is None')
            index, _ = api.read(to_what, to_id)
            api.move(what, id, index)
        else:
            link_index, parent = parent_data
            new_link = {
                'from': {'what': parent['_what'], '_id': parent['_id']},
                'to': {'what': what, '_id': id}
            }
            app.logger.info('new link is %s', new_link)
            if location == "below":
                link_index += 1
            api.links.insert(link_index, new_link)
            api.write_links()

    response = jsonify({'status': 'ran move, success unknown'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/display")
def get_display():
    display = read_yaml(path.join(CONFIG_PATH, "_gui.yaml"))
    response = jsonify(display)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    app.run()
