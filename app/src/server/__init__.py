from .app import app
from .routes.data import *
from .routes.config import *
from .routes.config_fields import *
from .routes.config_types import *


def run():
    app.run(host='0.0.0.0', port=8000)