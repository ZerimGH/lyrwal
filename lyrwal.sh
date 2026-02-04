#!/usr/bin/env bash

cd "$(dirname "$0")"

set -xe

# Compile textwal
make all -C ./textwal

# Get text
make install -C ./py
make run -s -C ./py > /tmp/lyrwal.txt 

# Generate wallpaper
cd ./py
font=$(./.venv/bin/python -c 'import config; config.get_opt("font")')
background_color=$(./.venv/bin/python -c 'import config; config.get_opt("background_color")')
text_color=$(./.venv/bin/python -c 'import config; config.get_opt("text_color")')
width=$(./.venv/bin/python -c 'import config; config.get_opt("width")')
height=$(./.venv/bin/python -c 'import config; config.get_opt("height")')
font_size=$(./.venv/bin/python -c 'import config; config.get_opt("font_size")')
wall_dir=$(./.venv/bin/python -c 'import config; config.get_opt("wallpaper_dir")')
wall_command=$(./.venv/bin/python -c 'import config; config.get_opt("command")')
# expand directories
wall_dir=$(eval echo $wall_dir)
wall_command=$(eval echo $wall_command)
cd ..
echo $wall_dir
echo $wall_command

img_cmd="./textwal/build/textwal -f ${font} -b ${background_color} -t ${text_color} -w ${width} -h ${height} -s ${font_size} -o ${wall_dir}"  

$img_cmd < /tmp/lyrwal.txt
$wall_command
