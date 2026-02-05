#!/usr/bin/env bash

cd "$(dirname "$0")"

set -e

cmd="$1"
arg="$2"

if [ -z "$cmd" ]; then
    echo "Usage: $0 {update|get <key>}"
    exit 1
fi

python_loc="/usr/lib/lyrwal/venv/bin/python"
mkdir -p $HOME/Pictures
mkdir -p $HOME/Pictures/lyrwal

set_wallpaper_path="$HOME/.config/lyrwal/set-wallpaper.sh"
config_toml_path="$HOME/.config/lyrwal/config.toml"

write_cfg() {
  cat <<EOL > "$config_toml_path"
[genius]
api_key = "YOUR_API_KEY" # API key, get one at https://genius.com/api-clients/new

[lyrics]
artists = ["Avenged Sevenfold"] # A list of artists names to include songs by
max_lines = 8 # The maximum number of lines of a song's paragraph to render
max_songs = 50 # The maximum number of songs to load and store from each artist

[render]
width = 1920 # Width of the output wallpaper image
height = 1080 # Height of the output wallpaper image
font = "/usr/share/fonts/liberation/LiberationMono-Regular.ttf" # The location of the font used to render (has to be .ttf i think)
font_size = 38 # Font size
text_color = "#ffffff"
background_color = "#000000"
# Possible values: centre, left, right, top, bottom, top-left, top-right, bottom-left, bottom-right
text_align = "centre" # Where the text is rendered on the screen
# Possible values: centre, left, right
char_align = "left" # If characters are rendered aligned to the left or to the right
#bg_img = "/path/to/bg.png" # An optional background image to put behind the text
#opacity = 0.5 # An optional opacity value for the text

[wallpaper]
wallpaper_dir = "$HOME/Pictures/lyrwal/wallpaper.png" # Location that the rendered wallpaper will be saved
command = "$HOME/.config/lyrwal/set-wallpaper.sh" # The command that will be run to set the wallpaper
EOL
}

write_set_wallpaper() {
  echo "Creating $set_wallpaper_path..."
  cat <<EOL > "$set_wallpaper_path"
#!/usr/bin/env bash

WALLPAPER_DIR=\$(lyrwal get wallpaper_dir)
echo 'You have not created a script to set your wallpaper!'
echo 'Please edit $HOME/.config/lyrwal/set-wallpaper.sh to properly set the wallpaper based on WALLPAPER_DIR.'
EOL
}

if [ "$cmd" = "update" ]; then
  # Generate configs if not there
  mkdir -p $HOME/.config/lyrwal

  if [ ! -e "$set_wallpaper_path" ]; then
      write_set_wallpaper
      chmod +x "$set_wallpaper_path"
      echo "$set_wallpaper_path has been created."
  fi

  if [ ! -e "$config_toml_path" ]; then
      echo "Creating $config_toml_path..."
      write_cfg
      echo "$config_toml_path has been created."
      echo "You may need to get an API key for genius for $config_toml_path, and edit $set_wallpaper_path to correctly set your wallpaper."
  fi

    echo "Getting lyrics to render..."
    cd /usr/lib/lyrwal/py
    $python_loc ./main.py

    font=$($python_loc -c 'import config; config.get_opt("font")')
    background_color=$($python_loc -c 'import config; config.get_opt("background_color")')
    text_color=$($python_loc -c 'import config; config.get_opt("text_color")')
    width=$($python_loc -c 'import config; config.get_opt("width")')
    height=$($python_loc -c 'import config; config.get_opt("height")')
    font_size=$($python_loc -c 'import config; config.get_opt("font_size")')
    text_align=$($python_loc -c 'import config; config.get_opt("text_align")')
    char_align=$($python_loc -c 'import config; config.get_opt("char_align")')
    opacity=$($python_loc -c 'import config; config.get_opt("opacity")')
    bg_img=$($python_loc -c 'import config; config.get_opt("bg_img")')
    wallpaper_dir=$($python_loc -c 'import config; config.get_opt("wallpaper_dir")')
    wall_command=$($python_loc -c 'import config; config.get_opt("command")')
    bg_img=$(eval echo $bg_img)
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
    [ -n "$opacity" ]         && img_cmd+=( -p "$opacity" )

    # printf 'CMD:'; printf ' %q' "${img_cmd[@]}"; echo
    "${img_cmd[@]}" < /tmp/lyrwal.txt
    echo "Finished rendering wallpaper"
    echo "Using command ${wall_command} to set the wallpaper"
    $wall_command
    rm /tmp/lyrwal.txt

elif [ "$cmd" = "get" ]; then
    if [ -z "$arg" ]; then
        echo "Usage: $0 get <key>"
        exit 1
    fi
    cd /usr/lib/lyrwal/py
    $python_loc -C "import config; config.get_opt('$arg')"
else
    echo "Unknown command: $cmd"
    echo "Usage: $0 {update|get <key>}"
    exit 1
fi

