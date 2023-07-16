#!/usr/bin/env bash

# TODO: add code formatting check
# TODO: turn it into hooks

msg() {
    echo -en "\033[35m"
    echo -n "check_code: "
    echo -en "\033[00m"
    echo $1
}

msg "running tests ..."
pytest

msg "running mypy on tangler/ ..."
mypy tangler/

msg "running mypy on tests/ ..."
mypy tests/