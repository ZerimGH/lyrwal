import tomllib
from pathlib import Path
import os

def err(): 
    print("Something went wrong with loading the configuration.")
    exit(1)

CONFIG_PATH = Path("~/.config/lyrwal/config.toml").expanduser()
SET_PATH = Path("~/.config/lyrwal/set-wallpaper.sh").expanduser()

def read_config():
    with open(CONFIG_PATH, "rb") as f:
        config = tomllib.load(f)
        return config

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
}

class _MISSING: pass

def get(config, path, cast=None, default=_MISSING):
    cur = config
    for key in path.split("."):
        if key not in cur:
            if default is _MISSING:
                raise KeyError(path)
            return default
        cur = cur[key]
    return cast(cur) if cast else cur

class Config:
    def __init__(self):
        try:
            config = read_config()
            if not config:
                raise RuntimeError("Could not read config file")

            for path, typ in REQUIRED.items():
                setattr(self, path.split(".")[-1], get(config, path, typ))

            for path, typ in OPTIONAL.items():
                setattr(
                    self,
                    path.split(".")[-1],
                    get(config, path, typ, default=None)
                )

            self.valid = True

        except Exception as e:
            print(f"Config error: {e}")
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
        v = cfg.__dict__[key]
        if v: print(v)
    except Exception as e:
        return
