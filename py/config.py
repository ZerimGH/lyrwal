import tomllib
from pathlib import Path
import os

def err(): 
    print("Something went wrong with loading the configuration.")
    exit(1)

CONFIG_PATH = Path("~/.config/lyrwal/config.toml").expanduser()
SET_PATH = Path("~/.config/lyrwal/set-wallpaper.sh").expanduser()
EXAMPLE_CONFIG = """\
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

[wallpaper]
wallpaper_dir = "$HOME/Pictures/lyrwal/wallpaper.png"
command = "$HOME/.config/lyrwal/set-wallpaper.sh"
"""

EXAMPLE_SET = """\
#!/usr/bin/env bash

echo 'You have not created a script to set your wallpaper!'
echo 'Please edit ~/.config/lyrwal/set-wallpaper.sh to properly set the wallpaper based on the wallpaper_dir from your configuration file.'
"""

def ensure_config():
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not CONFIG_PATH.is_file():
        CONFIG_PATH.write_text(EXAMPLE_CONFIG, encoding="utf-8")

    if not SET_PATH.is_file():
        SET_PATH.write_text(EXAMPLE_SET, encoding="utf-8")
        os.chmod(SET_PATH, 0o755)

def read_config():
    ensure_config()
    with open(CONFIG_PATH, "rb") as f:
        config = tomllib.load(f)
        return config

class Config:
    def __init__(self):
        try:
            config = read_config()
            if not config: raise Exception('Could not read config file') 
            self.api_key = config['genius']['api_key']
            self.artists = config['lyrics']['artists']
            self.max_lines = int(config['lyrics']['max_lines'])
            self.max_songs = int(config['lyrics']['max_songs'])
            self.width = int(config['render']['width'])
            self.height = int(config['render']['height'])
            self.font = config['render']['font']
            self.font_size = int(config['render']['font_size'])
            self.text_color = config['render']['text_color']
            self.background_color = config['render']['background_color']
            self.text_align = config['render']['text_align']
            self.char_align = config['render']['char_align']
            self.wallpaper_dir = config['wallpaper']['wallpaper_dir']
            self.command = config['wallpaper']['command']
            self.valid = True
        except Exception as e:
            print(e)
            err()
            self.valid = False

    def print(self):
        if not self.valid:
            print("Invalid config")
            err()
        else:
            d = self.__dict__
            for v in d:
                print('%s: %s' % (str(v), str(d[v])))

def get_opt(key):
    try:
        cfg = Config()
        print(cfg.__dict__[key])
    except Exception as e:
        print(e)
        err()
