import tomllib
from pathlib import Path
import os
import requests

CONFIG_PATH = Path("~/.config/lyrwal/config.toml").expanduser()

REQUIRED = {
    "genius.api_key": str,
    "lyrics.artists": list,
    "lyrics.max_lines": int,
    "lyrics.max_songs": int,
    "wallpaper.wallpaper_dir": str,
    "wallpaper.command": str,
}

OPTIONAL = {
    "render.bg_img": str,
    "render.width": int,
    "render.height": int,
    "render.font": str,
    "render.font_size": int,
    "render.text_color": str,
    "render.background_color": str,
    "render.text_align": str,
    "render.char_align": str,
    "render.opacity": float,
}

class _MISSING: pass

def read_config():
    with open(CONFIG_PATH, "rb") as f:
        config = tomllib.load(f)
        return config

def get(config, path, cast=None, default=_MISSING):
    cur = config
    for key in path.split("."):
        if key not in cur:
            if default is _MISSING:
                raise KeyError(path)
            return default
        cur = cur[key]
    return cast(cur) if cast else cur

class Options:
    # Load all options from the toml file
    def load(self):
        try:
            config = read_config()
            if not config:
                raise RuntimeError("Could not read config file")
            for path, typ in REQUIRED.items():
                setattr(self, path.split(".")[-1], get(config, path, typ))
            for path, typ in OPTIONAL.items():
                setattr(self, path.split(".")[-1], get(config, path, typ, default=None))
            self.valid = True
        except Exception as e:
            print(f"Config error: {e}")
            self.valid = False

    def __init__(self):
        self.load()

def get_opt(key):
    try:
        v = getattr(options, key, None) 
        if v is not None: print(v)
    except Exception as e:
        return

options = Options()
if not options.valid:
    print("Invalid config file. Please correct it.")
    exit(1)

