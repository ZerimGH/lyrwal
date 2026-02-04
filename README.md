Lyrwal is a simple program I made to set my wallpaper to an image of random song lyrics from artists.

It's very incomplete right now, and the lyrics requests are very basic so it sometimes includes collaborations / samples of artists, but I will work on it :)

Setup (AUR):
  1) Install the package
     > yay -S lyrwal
  2) Get an API key for genius lyrics from https://genius.com/api-clients (free)
  3) Run lyrwal, and let it generate default configs
     > lyrwal update
  4) Add your API key to the config file at ~/.config/lyrwal/config.toml
  
     Look for the lines:
     > [genius]
     > 
     > api_key = "****************************************************************" # < PUT YOUR API KEY IN THESE QUOTES
     >
     You can customise colours, font, text styles, background image, resolution, and artists here too.
  5) Fill in the script to set your wallpaper.

     There's no generic way to update the wallpaper between wm's, so you'll need a script to do that.
     The script is at ~/.config/lyrwal/set-wallpaper.sh, and is run after the wallpaper is rendered.
     An example script for X11 might look like:
     > #!/usr/bin/env bash
     >
     > \# These exports are only needed if the script will be run indirectly, by something like cronie or your wm
     >
     > export DISPLAY=:0
     >
     > export XAUTHORITY=$(ls /tmp/xauth_* | head -n 1)
     >
     > WALLPAPER_DIR=$(lyrwal get wallpaper_dir)
     >
     > feh --bg-fill $WALLPAPER_DIR
     > 
  6) Run lyrwal update, and your wallpaper should update :) (It will take a while to update the wallpaper until enough lyrics have been cached)
