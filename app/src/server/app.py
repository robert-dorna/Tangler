from flask import Flask
from werkzeug.exceptions import BadRequest
from logging.config import dictConfig

from .routes.data import data_request_handler, data_update_request_handler, data_create_request_handler
from .routes.config import config_read_request_handler, config_patch_request_handler

from .routes.move import move_route_handler
from .routes.unlink import unlink_route_handler

from .utils.logging import config as logger_config
from .utils.exceptions import handler as exception_handler


dictConfig(logger_config)

app = Flask(__name__)


@app.errorhandler(BadRequest)
def handle_exception(e):
    return exception_handler(e)


@app.route("/data")
def update_task():
    return data_request_handler(app)


@app.route("/data", methods=['POST'])
def update():
    return data_update_request_handler()


@app.route("/data", methods=['PUT'])
def create():
    return data_create_request_handler()


@app.route("/move")
def move():
    return move_route_handler(app)


@app.route("/unlink")
def unlink():
    return unlink_route_handler()


@app.route("/config")
def read_config():
    return config_read_request_handler()


@app.route("/config", methods=["POST"])
def patch_display():
    return config_patch_request_handler()


def run():
    app.run(host='0.0.0.0', port=8000)


if __name__ == "__main__":
    run()
