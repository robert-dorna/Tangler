from flask import Flask, jsonify, request, Response
from .core.datadir import List
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
    data = List('r+')

    args = {**request.args}
    if 'index' in args:
        args['index'] = int(args['index']) 
        
    if ',' in args['what']:
        args['what'] = args['what'].split(',')
        
    # app.logger.info('args: %s', args)

    method = getattr(data, args.pop('method'))
    result = method(**args)

    data.flush()

    success = True # todo, way to check from Data that it was updated
    response = jsonify(
        {'status': 'ran update, success unknown', 'result': result } if success else 
        {'status': 'error'}
    )
    
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
    

if __name__ == "__main__":
  app.run()
