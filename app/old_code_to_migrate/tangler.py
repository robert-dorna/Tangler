#!/usr/bin/env python
from sys import argv
from src.server import run, app


if __name__ == "__main__":
    if len(argv) > 1 and argv[1] == 'server':
        run()
    else:
        from src.cli import parse_args, run_command
        run_command(**parse_args(argv[1:]))
