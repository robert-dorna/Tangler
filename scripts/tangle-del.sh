#!/usr/bin/env bash


echo "from task:"
ta read task "$1"

echo "deleting account:"
ta read account "$2"

echo "running ..."
ta unlink task "$1" account "$2"
ta delete account "$2"
echo "done!"
