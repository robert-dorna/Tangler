from flask import Flask
from werkzeug.exceptions import BadRequest
from logging.config import dictConfig

from .routes.data import data_route_handler
from .routes.display import display_route_handler
from .routes.update import update_route_handler
from .routes.create import create_route_handler
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
    return data_route_handler(app)


@app.route('/update')
def update():
    return update_route_handler()


@app.route('/create')
def create():
    return create_route_handler()


@app.route("/move")
def move():
    return move_route_handler(app)


@app.route("/unlink")
def unlink():
    return unlink_route_handler()


@app.route("/display")
def get_display():
    return display_route_handler()


@app.route("/config")
def config():
    return display_route_handler()


def run():
    app.run(host='0.0.0.0', port=8000)


if __name__ == "__main__":
    run()
