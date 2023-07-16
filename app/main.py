#!/usr/bin/env python
from sys import argv
from tangler import Tangler

# NOTE: this is temporary to allow for `flask --app main.py --debug`
tangler = Tangler(spaces_config="spaces.yml")
server = tangler.get_server()
app = server.app

if __name__ == "__main__":
    # tangler = Tangler(spaces_config="spaces.yml")
    tangler.run(argv)
