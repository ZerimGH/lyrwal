Lyrwal is a simple program I made to set my wallpaper to an image of random song lyrics from artists.

It's very incomplete right now, but I will work on it :)

Setup (Arch linux only):
  1) Clone the repo
     > git clone --recursive git@github.com:ZerimGH/lyrwal.git
  2) Cd, and run the install script
     > cd lyrwal && ./install.sh
  3) Get an API key for genius lyrics from https://genius.com/api-clients (free)
  4) Run lyrwal, and let it generate default configs
     > lyrwal
  5) Add your API key to the config file at ~/.config/lyrwal/config.toml
  
     Look for the lines:
     > [genius]
     > api_key = "****************************************************************" # < PUT YOUR API KEY IN THESE QUOTES
     >
     You can customise colours, font, resolution, and artists here too.
  6) Fill in the script to set your wallpaper
     There's no generic way to update the wallpaper between wm's, so you'll need a script to do that.
     The script is at ~/.config/lyrwal/set-wallpaper.sh, and is run after the wallpaper is rendered.
     An example script might look like:
     > #!/usr/bin/env bash
     >
     > \# These exports are only needed if the script will be run as root, or by something like cronie
     >
     > export DISPLAY=:0
     >
     > export XAUTHORITY=$(ls /tmp/xauth_* | head -n 1)
     >
     > feh --bg-fill "~/Pictures/lyrwal/wallpaper.png" # You will need to change the directory if you change the wallpaper_dir in the config file. It's also better to use an absolute path here
  7) Run lyrwal, and your wallpaper should update :)
