#!/usr/bin/env bash

set -xe

git submodule update --init --recursive
make all -C textwal

python -m venv venv

venv/bin/pip install --upgrade pip
venv/bin/pip install -r py/requirements.txt

sudo mkdir -p /usr/lib/lyrwal

sudo install -Dm755 lyrwal.sh /usr/bin/lyrwal
sudo install -Dm755 textwal/build/textwal /usr/bin/textwal
sudo install -d /usr/lib/lyrwal
sudo cp -r py /usr/lib/lyrwal/

sudo cp -r venv /usr/lib/lyrwal/venv

sudo install -Dm644 LICENSE /usr/share/licenses/lyrwal/LICENSE
