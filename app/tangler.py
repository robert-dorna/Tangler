#!/usr/bin/env python
from sys import argv
from src.cli import parse_args, run_command
from src.server.app import run, app


if __name__ == "__main__":
    if len(argv) > 1 and argv[1] == 'server':
        run()
    else:
        run_command(**parse_args(argv[1:]))
