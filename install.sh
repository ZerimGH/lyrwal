#!/usr/bin/env bash

./uninstall.sh

dir=$(pwd)

set -xe

sudo pacman -S --needed python gcc freetype2

mkdir -p ~/.lyrwal
cp -r ./py ~/.lyrwal

make install -C ./textwal

cd ~/.lyrwal/py
make install
cd $dir

sudo cp ./lyrwal.sh /usr/local/bin/lyrwal 
sudo chmod +x /usr/local/bin/lyrwal 
