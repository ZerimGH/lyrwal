import config
from lyricsgenius import Genius
from pathlib import Path
import tomllib
import random

# Class responsible for fetching and storing local information
class Cacher:
    # Make sure the necessary cache files exist
    def ensure_files(self):
        if not self.cache_dir.exists():
            print(f"Making cache directory {self.cache_dir}")
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        if not self.artist_id_cache.exists():
            print(f"Making artist id cache file {self.artist_id_cache}")
            self.artist_id_cache.write_text("[artists]")

    def __init__(self):
        self.cache_dir = Path("~/.cache/lyrwal").expanduser() 
        self.artist_id_cache = self.cache_dir / "artists.toml"
        self.ensure_files()

    # Get all cached Artist Name -> Id's
    def fetch_artist_ids(self):
        try:
            with open(self.artist_id_cache, "rb") as f:
                ids = tomllib.load(f)
                return ids['artists'] 
        except (FileNotFoundError, KeyError): return {}

    # Get a specific artist's id
    def fetch_artist_id(self, artist_name):
        ids = self.fetch_artist_ids()
        if artist_name in ids: return int(ids[artist_name])
        else: return None

    # Get all song id's from an artist id
    def fetch_artist_songs(self, artist_id):
        artist_cache_dir = self.cache_dir / str(artist_id)
        if not artist_cache_dir.exists(): return None
        song_id_cache = artist_cache_dir / "songs.txt"
        if not song_id_cache.exists(): return None
        with open(song_id_cache, "r") as f:
            return f.read().splitlines()

    # Get the lyrics of an artist's song
    def fetch_artist_song_lyrics(self, artist_id, song_id):
        artist_cache_dir = self.cache_dir / str(artist_id)
        if not artist_cache_dir.exists(): return None
        lyrics = artist_cache_dir / f"{song_id}.txt"
        if not lyrics.exists(): return None
        with open(lyrics, "r") as f:
            return f.read()

    # Store an artists id
    def store_artist_id(self, artist_name, artist_id):
        ids = self.fetch_artist_ids()
        ids[artist_name] = artist_id

        with open(self.artist_id_cache, "w") as f:
            f.write("[artists]\n")
            for aid, val in ids.items():
                f.write(f'"{aid}" = "{val}"\n')

    # Store all song id's from an artist
    def store_artist_songs(self, artist_id, song_ids):
        artist_cache_dir = self.cache_dir / str(artist_id)
        artist_cache_dir.mkdir(parents=True, exist_ok=True)
        song_id_cache = artist_cache_dir / "songs.txt"
        with open(song_id_cache, "w") as f:
            for sid in song_ids:
                f.write(f"{sid}\n")

    # Store the lyrics of an artist's song
    def store_artist_song_lyrics(self, artist_id, song_id, lyrics):
        artist_cache_dir = self.cache_dir / str(artist_id)
        artist_cache_dir.mkdir(parents=True, exist_ok=True)
        lyrics_p = artist_cache_dir / f"{song_id}.txt"
        with open(lyrics_p, "w") as f:
            f.write(lyrics)

# Class responsible for fetching information from the API
class Finder:
    def __init__(self):
        if config.options.api_key is not None:
            self.genius = Genius(access_token = config.options.api_key,
                                 timeout = 5,
                                 remove_section_headers = True,
                                 skip_non_songs = True)
        else: self.genius = None

    def fetch_artist_id(self, artist_name):
        if self.genius is None: return None
        try:
            artist = self.genius.search_artist(artist_name, max_songs = 0) 
        except Exception as e:
            print(f"Genius lookup request failed: {e}")
            return None
        if artist is None: 
            print(f"Failed to lookup id for artist {artist_name}.")
            return None
        return artist._body['id'] 

    def fetch_artist_songs(self, artist_id):
        if self.genius is None: return None
        to_load = config.options.max_songs
        all_songs = []
        page = 1
        while len(all_songs) < to_load:
            try:
                local_songs = self.genius.artist_songs(artist_id=artist_id,
                                                       sort='popularity',
                                                       per_page=50,
                                                       page=page)
                if not local_songs: break 
                for song in local_songs['songs']:
                    all_songs.append(song['id'])
                    if len(all_songs) >= to_load: break
                page += 1
            except Exception as e:
                print(f"Genius song search request failed: {e}")
                return None
        return all_songs

    def fetch_artist_song_lyrics(self, artist_id, song_id):
        if self.genius is None: return None
        try:
            return self.genius.lyrics(song_id=song_id, remove_section_headers=True)
        except Exception as e:
            print(f"Genius lyrics request failed: {e}")
            return None

# Main fetcher class
class Fetcher:
    def __init__(self):
        self.cacher = Cacher()
        self.finder = Finder()

    def fetch_artist_id(self, artist_name):
        # Check cached ids
        cache_res = self.cacher.fetch_artist_id(artist_name)
        if cache_res is not None: return cache_res
        # Lookup from genius
        find_res = self.finder.fetch_artist_id(artist_name)
        if find_res is None:
            print(f"Id for artist {artist_name} was not cached, and genius lookup failed.") 
            return None
        # Store lookup result
        self.cacher.store_artist_id(artist_name, find_res)
        return find_res

    def fetch_artist_songs(self, artist_id):
        # Check cached ids
        cache_res = self.cacher.fetch_artist_songs(artist_id)
        if cache_res is not None: return cache_res
        # Lookup from genius
        find_res = self.finder.fetch_artist_songs(artist_id)
        if find_res is None:
            print(f"Songs for artist id {artist_id} was not cached, and genius lookup failed.") 
            return None
        # Store lookup result
        self.cacher.store_artist_songs(artist_id, find_res)
        return find_res

    def fetch_artist_song_lyrics(self, artist_id, song_id):
        # Check cached ids
        cache_res = self.cacher.fetch_artist_song_lyrics(artist_id, song_id)
        if cache_res is not None: return cache_res
        # Lookup from genius
        find_res = self.finder.fetch_artist_song_lyrics(artist_id, song_id)
        if find_res is None:
            print(f"Song lyrics for artist id {artist_id}, song id {song_id} was not cached, and genius lookup failed.") 
            return None
        # Store lookup result
        self.cacher.store_artist_song_lyrics(artist_id, song_id, find_res)
        return find_res

fetcher = Fetcher()

def random_lyrics():
    artist_names = config.options.artists.copy()
    while len(artist_names) > 0:
        artist = random.choice(artist_names)
        artist_names.remove(artist)
        artist_id = fetcher.fetch_artist_id(artist) 
        if artist_id is None: continue
        artist_songs = fetcher.fetch_artist_songs(artist_id)
        if artist_songs is None: continue
        while len(artist_songs) > 0:
            song = random.choice(artist_songs)
            artist_songs.remove(song)
            lyrics = fetcher.fetch_artist_song_lyrics(artist_id, song)
            if lyrics is not None: return lyrics
    return None
