Lyrwal is a simple program I made to set my wallpaper to an image of random song lyrics from artists.

It's very incomplete right now, and the lyrics requests are very basic so it sometimes includes collaborations / samples of artists, but I will work on it :)

Preview:
![2026_02_05_20_04_33](https://github.com/user-attachments/assets/6ce650af-f6db-47b8-a471-98f5865581fc)



Setup:
  1) Install the package

     Using AUR helper:
     > yay -S lyrwal
     > 
     OR only using git:
     
     If using this method, first ensure that you have these installed: gcc, make, python, freetype2 
     > git clone --recursive https://github.com/ZerimGH/lyrwal.git && cd lyrwal && ./install.sh
     > 
  3) Get an API key for genius lyrics from https://genius.com/api-clients (free)
  4) Run lyrwal, and let it generate default configs
     > lyrwal update
  5) Add your API key to the config file at ~/.config/lyrwal/config.toml
  
     Look for the lines:
     > [genius]
     > 
     > api_key = "****************************************************************" # < PUT YOUR API KEY IN THESE QUOTES
     >
     You can customise colours, font, text styles, background image, resolution, and artists here too.
  6) Fill in the script to set your wallpaper.

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
  7) Run lyrwal update, and your wallpaper should update :) (It will take a while to update the wallpaper until enough lyrics have been cached)
