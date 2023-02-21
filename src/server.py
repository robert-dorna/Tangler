from flask import Flask, jsonify, request, Response
from .api import Api
from .core.files import read_yaml, CONFIG_PATH
from logging.config import dictConfig
from os import path


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


# SOCKETS, WebSockets/Socket.IO,
# RAW, RPC, SOAP, REST, GraphQL
@app.route("/data")
def update_task():

    args = {**request.args}

    if 'index' in args:
        args['index'] = int(args['index'])

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


@app.route("/types")
def get_types():
    response = jsonify([
        {"name": "email", "emoji": "✉️"},
        {"name": "contact", "emoji": "👤"},
        {"name": "task", "emoji": "✅"},
        {"name": "check", "emoji": "🔁"},
        {"name": "note", "emoji": "✍️"},
        {"name": "account", "emoji": "🔑"},
        {"name": "item", "emoji": "🧳"},
        {"name": "transaction", "emoji": "💲"},
        {"name": "journal", "emoji": "📒"}
    ])
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/display")
def get_display():
    display = read_yaml(path.join(CONFIG_PATH, "_display.yaml"))
    response = jsonify(display)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    app.run()
