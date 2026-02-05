#!/usr/bin/env bash

read -p "This script requires that you install the packages: gcc, make, python, freetype2. Do you want to continue? (y/n)" choice

if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
    echo "Continuing..."
else
    echo "Exiting..."
    exit 0
fi

./uninstall.sh

dir=$(pwd)

set -xe

mkdir -p ~/.lyrwal
cp -r ./py ~/.lyrwal

make install -C ./textwal

cd ~/.lyrwal/py
make install
cd $dir

sudo cp ./lyrwal.sh /usr/local/bin/lyrwal 
sudo chmod +x /usr/local/bin/lyrwal 
