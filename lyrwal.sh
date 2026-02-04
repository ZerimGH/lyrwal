#!/usr/bin/env bash

cd "$(dirname "$0")"

set -e

cmd="$1"
arg="$2"

if [ -z "$cmd" ]; then
    echo "Usage: $0 {update|get <key>}"
    exit 1
fi

mkdir -p $HOME/Pictures
mkdir -p $HOME/Pictures/lyrwal

# Generate configs if not there
mkdir -p $HOME/.config/lyrwal
set_wallpaper_path="$HOME/.config/lyrwal/set-wallpaper.sh"
config_toml_path="$HOME/.config/lyrwal/config.toml"

if [ ! -e "$set_wallpaper_path" ]; then
    echo "Creating $set_wallpaper_path..."
    cat <<EOL > "$set_wallpaper_path"
#!/usr/bin/env bash

WALLPAPER_DIR=\$(lyrwal get wallpaper_dir)
echo 'You have not created a script to set your wallpaper!'
echo 'Please edit $HOME/.config/lyrwal/set-wallpaper.sh to properly set the wallpaper based on WALLPAPER_DIR.'
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
text_align = "centre"
char_align = "left"
#bg_img = "/path/to/bg.png"

[wallpaper]
wallpaper_dir = "$HOME/Pictures/lyrwal/wallpaper.png"
command = "$HOME/.config/lyrwal/set-wallpaper.sh"
EOL
    echo "$config_toml_path has been created."
    echo "You may need to get an API key for genius for $config_toml_path, and edit $set_wallpaper_path to correctly set your wallpaper."
fi

if [ "$cmd" = "update" ]; then
    cd $HOME/.lyrwal/py
    ./.venv/bin/python ./main.py update

    font=$(./.venv/bin/python -c 'import config; config.get_opt("font")')
    background_color=$(./.venv/bin/python -c 'import config; config.get_opt("background_color")')
    text_color=$(./.venv/bin/python -c 'import config; config.get_opt("text_color")')
    width=$(./.venv/bin/python -c 'import config; config.get_opt("width")')
    height=$(./.venv/bin/python -c 'import config; config.get_opt("height")')
    font_size=$(./.venv/bin/python -c 'import config; config.get_opt("font_size")')
    text_align=$(./.venv/bin/python -c 'import config; config.get_opt("text_align")')
    char_align=$(./.venv/bin/python -c 'import config; config.get_opt("char_align")')
    bg_img=$(./.venv/bin/python -c 'import config; config.get_opt("bg_img")')
    wallpaper_dir=$(./.venv/bin/python -c 'import config; config.get_opt("wallpaper_dir")')
    wall_command=$(./.venv/bin/python -c 'import config; config.get_opt("command")')
    wallpaper_dir=$(eval echo $wallpaper_dir)
    wall_command=$(eval echo $wall_command)

    img_cmd=(textwal)
    [ -n "$font" ]            && img_cmd+=( -f "$font" )
    [ -n "$background_color" ]&& img_cmd+=( -b "$background_color" )
    [ -n "$text_color" ]      && img_cmd+=( -t "$text_color" )
    [ -n "$width" ]           && img_cmd+=( -w "$width" )
    [ -n "$height" ]          && img_cmd+=( -h "$height" )
    [ -n "$font_size" ]       && img_cmd+=( -s "$font_size" )
    [ -n "$text_align" ]      && img_cmd+=( -A "$text_align" )
    [ -n "$char_align" ]      && img_cmd+=( -a "$char_align" )
    [ -n "$bg_img" ]          && img_cmd+=( -i "$bg_img" )
    [ -n "$wallpaper_dir" ]   && img_cmd+=( -o "$wallpaper_dir" )

    printf 'CMD:'; printf ' %q' "${img_cmd[@]}"; echo
    "${img_cmd[@]}" < /tmp/lyrwal.txt
    $wall_command
    rm /tmp/lyrwal.txt
elif [ "$cmd" = "get" ]; then
    if [ -z "$arg" ]; then
        echo "Usage: $0 get <key>"
        exit 1
    fi
    cd $HOME/.lyrwal/py
    ./.venv/bin/python -c "import config; config.get_opt('$arg')"
else
    echo "Unknown command: $cmd"
    echo "Usage: $0 {update|get <key>}"
    exit 1
fi

