import fetcher
import re
import random
import config

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

if __name__ == "__main__":
    with open("/tmp/lyrwal.txt", "w") as f:
        f.write(random_lyrics())
    exit(0)
