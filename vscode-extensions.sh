#!/usr/bin/env bash

vscode_extensions="eamodio.gitlens ms-python.python njpwerner.autodocstring bungcip.better-toml svelte.svelte-vscode"

for ext_id in $vscode_extensions;
do
    code --install-extension $ext_id
done
