#!/usr/bin/env python
from sys import argv
from tangler import Tangler


if __name__ == "__main__":
    tangler = Tangler(spaces_config="spaces.yml")
    tangler.run(argv)
