from flask import Flask
from werkzeug.exceptions import BadRequest
from logging.config import dictConfig

from .utils.logging import config as logger_config
from .utils.exceptions import handler as exception_handler


dictConfig(logger_config)

app = Flask(__name__)


@app.errorhandler(BadRequest)
def handle_exception(e):
    return exception_handler(e)