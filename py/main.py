import fetcher
import re
import random
import config
import unicodedata

# Get a random song's lyrics, and select the first few lines of a random paragraph
def random_lyrics():
    lyrics = fetcher.random_lyrics()
    if lyrics is None:
        return "No lyrics found."

    paragraphs = re.split(r'\n{2,}', lyrics)
    paragraph = random.choice(paragraphs)

    max_lines = config.options.max_lines
    powers = [2]
    for i in range(2, max_lines):
        n = 2 ** i
        if n > max_lines: break
        powers.append(n)
    n_lines = random.choice(powers)

    return "\n".join(paragraph.split("\n")[:n_lines])

# Replace unrenderable characters from the selected lyrics
def process_lyrics(lyrics):
    return unicodedata.normalize('NFD', lyrics).encode('ascii', 'ignore')

if __name__ == "__main__":
    lyrics = random_lyrics()
    lyrics_ascii = process_lyrics(lyrics)
    final_lyrics = lyrics_ascii.decode('ascii')
    with open("/tmp/lyrwal.txt", "w") as f:
        f.write(final_lyrics)
    exit(0)
