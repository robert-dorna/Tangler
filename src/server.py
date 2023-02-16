from flask import Flask, jsonify, request, Response
from .api import Api
from logging.config import dictConfig


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

    success = True # todo, way to check from Data that it was updated
    response = jsonify(
        {'status': 'ran method, success unknown', 'result': result } if success else 
        {'status': 'error'}
    )
    
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
    

if __name__ == "__main__":
  app.run()
