from .app import app
from .routes.data import *
from .routes.move import *
from .routes.unlink import *
from .routes.config import *

from .routes.new_config import *
from .routes.new_data import *


def run():
    app.run(host='0.0.0.0', port=8000)