#!/usr/bin/env bash

set -xe

git submodule update --init --recursive
make all -C textwal

python -m venv venv

venv/bin/pip install --upgrade pip
venv/bin/pip install -r py/requirements.txt

install -Dm755 lyrwal.sh /usr/bin/lyrwal
install -Dm755 textwal/build/textwal /usr/bin/textwal
install -d /usr/lib/lyrwal
cp -r py /usr/lib/lyrwal/

cp -r venv usr/lib/lyrwal/venv

install -Dm644 LICENSE /usr/share/licenses/lyrwal/LICENSE
