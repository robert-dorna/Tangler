#!/usr/bin/env bash

nixPackages=""
nixPackages="$nixPackages python39Packages.pandas"
nixPackages="$nixPackages python39Packages.pyyaml"
nixPackages="$nixPackages python39Packages.flask"

command=""
command="$command source $HOME/Projects/tangle/.venv/bin/activate;"

if [ "$1" = "shell" ]; then
    if [ "$2" = "left" ]; then
      command="$command alias qq='x; tangle.py read check; tangle.py read task; tangle.py read note';"
      command="$command tangle.py read check;"
      command="$command tangle.py read task;"
      command="$command tangle.py read note;"
    elif [ "$2" = "right" ]; then
      command="$command alias qq='x; tangle.py read item; tangle.py read contact; tangle.py read journal; tangle.py read +transaction; tangle.py read account';"
      command="$command tangle.py read item;"
      command="$command tangle.py read contact;"
      command="$command tangle.py read journal;"
      command="$command tangle.py read +transaction;"
      command="$command tangle.py read account;"
    fi
    command="$command return"
else
    command="$command python tangle.py $1"
fi

# --pure was used in example on nix forum, dk why
nix-shell -p $nixPackages --command "$command"
