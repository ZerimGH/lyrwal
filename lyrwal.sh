#!/usr/bin/env bash

cd "$(dirname "$0")"

set -e

mkdir -p $HOME/Pictures
mkdir -p $HOME/Pictures/lyrwal

# Generate configs if not there
mkdir -p $HOME/.config/lyrwal
set_wallpaper_path="$HOME/.config/lyrwal/set-wallpaper.sh"
config_toml_path="$HOME/.config/config.toml"

if [ ! -e "$set_wallpaper_path" ]; then
    echo "Creating $set_wallpaper_path..."

    cat <<EOL > "$set_wallpaper_path"
#!/usr/bin/env bash

echo 'You have not created a script to set your wallpaper!'
echo 'Please edit $HOME/.config/lyrwal/set-wallpaper.sh to properly set the wallpaper based on the wallpaper_dir from your configuration file.'
EOL
    chmod +x "$set_wallpaper_path"
    echo "$set_wallpaper_path has been created."
fi

if [ ! -e "$config_toml_path" ]; then
    echo "Creating $config_toml_path..."

    cat <<EOL > "$config_toml_path"
[genius]
api_key = "YOUR_API_KEY"

[lyrics]
artists = ["Avenged Sevenfold"]
max_lines = 8
max_songs = 200 

[render]
width = 1920
height = 1080
font = "/usr/share/fonts/liberation/LiberationMono-Regular.ttf"
font_size = 38 
text_color = "#ffffff"
background_color = "#000000"

[wallpaper]
wallpaper_dir = "$HOME/Pictures/lyrwal/wallpaper.png"
command = "$HOME/.config/lyrwal/set-wallpaper.sh"
EOL

    echo "$config_toml_path has been created."
    echo "You may need to get an API key for genius for $config_toml_path, and edit $set_wallpaper_path to correctly set your wallpaper."
fi


# Generate wallpaper
cd $HOME/.lyrwal/py
./.venv/bin/python ./main.py
font=$(./.venv/bin/python -c 'import config; config.get_opt("font")')
background_color=$(./.venv/bin/python -c 'import config; config.get_opt("background_color")')
text_color=$(./.venv/bin/python -c 'import config; config.get_opt("text_color")')
width=$(./.venv/bin/python -c 'import config; config.get_opt("width")')
height=$(./.venv/bin/python -c 'import config; config.get_opt("height")')
font_size=$(./.venv/bin/python -c 'import config; config.get_opt("font_size")')
wall_dir=$(./.venv/bin/python -c 'import config; config.get_opt("wallpaper_dir")')
wall_command=$(./.venv/bin/python -c 'import config; config.get_opt("command")')
wall_dir=$(eval echo $wall_dir)
wall_command=$(eval echo $wall_command)

img_cmd="textwal -f ${font} -b ${background_color} -t ${text_color} -w ${width} -h ${height} -s ${font_size} -o ${wall_dir}"  

$img_cmd < /tmp/lyrwal.txt
$wall_command
rm /tmp/lyrwal.txt
