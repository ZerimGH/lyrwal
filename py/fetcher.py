import config as cfg
from lyricsgenius import Genius
from pathlib import Path
import tomllib
import re
import random
config = cfg.Config()

def err(): 
    print("Something went wrong, couldn't get the text to render.")
    exit(1)

if not config.valid:
    print("Invalid config, cannot fetch.")
    err()

CACHE_DIR = Path("~/.cache/lyrwal").expanduser() 
ID_CACHE_LOC = CACHE_DIR / "ids.toml" 

genius = Genius(config.api_key,
    skip_non_songs=True,
    remove_section_headers=True,
    verbose=False
)

def ensure_cache():
    if not CACHE_DIR.exists():
        CACHE_DIR.mkdir(parents=True, exist_ok = True)

def ensure_id_cache():
    ensure_cache()
    if not ID_CACHE_LOC.exists():
        ID_CACHE_LOC.write_text("""\
[artists]
""")

def id_lookup(artist):
    ensure_id_cache()
    try:
        with open(ID_CACHE_LOC, "rb") as f:
            ids = tomllib.load(f)
            return ids['artists'][name_to_key(artist)] 
    except: return None

def id_lookup_else_cache(artist):
    artist_id = id_lookup(artist)
    if artist_id is None:
        artist_id = fetch_artist_id(artist)
        if artist_id is None:
            print("Failed to lookup artist %s." % (artist))
        cache_artist_id(artist, artist_id)
    return artist_id

def name_to_key(artist):
    artist = artist.lower()
    artist = artist.replace(" ", "_")
    artist = re.sub(r"[^a-z0-9_]", "", artist)
    return artist

def cache_artist_id(artist, artist_id):
    ensure_id_cache()
    try:
        with open(ID_CACHE_LOC, "rb") as f:
            ids = tomllib.load(f)
    except FileNotFoundError:
        ids = {"artists": {}}

    if "artists" not in ids:
        ids["artists"] = {}

    ids["artists"][name_to_key(artist)] = artist_id
    with open(ID_CACHE_LOC, "w") as f:
        f.write("[artists]\n")
        for a, aid in ids["artists"].items():
            f.write('%s = "%s"\n' % (a, aid))

def fetch_artist_id(artist): 
    artist_id = id_lookup(artist)
    if artist_id is not None:
        return artist_id
    else:
        try:
            g_artist = genius.search_artist(
                artist, 
                max_songs = 0 
            )
            artist_id = g_artist._body['id'] 
            cache_artist_id(artist, artist_id)
            return artist_id
        except Exception as e:
            print(f"Couldn't get artist {artist} from genius.")
            print(e)
            return None

def cache_songs(artist_id):
    if artist_id is None: return None
    excluded_terms = ["remix", "live", "feat.", "ft.", "sampled", "edition", "version", "instrumental", "edit", "mix", "demo", "cover", "theme"]
    artist_dir = CACHE_DIR / str(artist_id)

    if artist_dir.exists() and any(artist_dir.iterdir()):
        return

    all_songs = []
    remaining = config.max_songs
    page = 1

    print(f"Caching songs for artist id {artist_id}")

    while remaining > 0:
        try:
            result = genius.artist_songs(artist_id, per_page=min(remaining, 50), page=page)
            songs_page = result.get("songs", [])

            if songs_page is None:
                break

            for song_data in songs_page:
                song_title = song_data["title"].lower()
                song_parts = re.split(r'[\s()]+', song_title)

                if any(excluded_term in song_parts for excluded_term in excluded_terms):
                    print(f"Skipping song {song_title}, title contains an excluded term")
                    continue

                print(f"Adding song {song_title}")
                all_songs.append(song_data)
                remaining -= 1
                if remaining == 0:
                    break
            page += 1
        except AssertionError:
            break

    if len(all_songs) == 0:
        print(f"Couldn't get songs from Genius for artist id {artist_id}.")
        return

    artist_dir.mkdir(parents=True, exist_ok=True)
    ids_loc = artist_dir / "songs.txt"
    with open(ids_loc, "w") as f:
        for song_data in all_songs:
            f.write(f"{song_data.get('id')}\n")

def random_song_id_else_cache(artist_id):
    if artist_id is None: return None
    artist_dir = CACHE_DIR / str(artist_id)
    ids_loc = artist_dir / "songs.txt"

    if not ids_loc.exists():
        cache_songs(artist_id)

    with open(ids_loc, "r") as f:
        song_ids = [line.strip() for line in f]

    if song_ids is None:
        print("No song IDs found in the cache.")
        return None

    song_id = random.choice(song_ids)
    return song_id

def process_lyrics(lyrics):
    processed_lyrics = re.sub(r'\[.*?\]', '', lyrics)
    processed_lyrics = processed_lyrics.strip()

    return processed_lyrics

def random_lyrics_else_cache(artist_id):
    if artist_id is None: return None
    artist_dir = CACHE_DIR / str(artist_id)
    song_id = random_song_id_else_cache(artist_id)

    song_loc = artist_dir / f"{song_id}.txt"

    if song_loc.exists():
        with open(song_loc, "r") as f:
            return f.read()

    try:
        lyrics = genius.lyrics(song_id=song_id)
        if lyrics:
            lyrics = process_lyrics(lyrics)
            artist_dir.mkdir(parents=True, exist_ok=True)
            with open(song_loc, "w") as f:
                f.write(lyrics)
            return lyrics
    except Exception as e:
        print(f"Error fetching lyrics for song ID {song_id}: {e}")
        return None

def random_lyrics_fallback():
    print("Failed to get random lyrics online, searching only cached files.")
    artists = config.artists.copy()
    while len(artists) > 0:
        artist = random.choice(artists)
        print(f"Artist: {artist}")
        artists.remove(artist)
        artist_id = id_lookup_else_cache(artist) 
        if artist_id is None: continue

        artist_dir = CACHE_DIR / str(artist_id)

        ids_loc = artist_dir / "songs.txt"

        if not ids_loc.exists(): continue 

        with open(ids_loc, "r") as f:
            song_ids = [line.strip() for line in f]

        while len(song_ids) > 0:
            song_id = random.choice(song_ids)
            song_ids.remove(song_id)

            song_loc = artist_dir / f"{song_id}.txt"

            if song_loc.exists():
                with open(song_loc, "r") as f:
                    print("Got lyrics!")
                    return f.read()
            else: continue
    print("No cached lyrics found.")
    return None

def random_lyrics():
    artists = config.artists.copy()
    lyrics = None
    while len(artists) > 0:
        artist = random.choice(artists)
        print(f"Artist: {artist}")
        artists.remove(artist)
        artist_id = id_lookup_else_cache(artist) 
        if artist_id is None: continue
        print(f"Id: {artist_id}")
        lyrics = random_lyrics_else_cache(artist_id) 
        print("Got lyrics!")
        if lyrics is not None: break
    if lyrics is None: return random_lyrics_fallback()
    return lyrics
