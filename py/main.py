import fetcher
import re
import config as cfg
import random
config = cfg.Config()
if not config.valid:
    print("Invalid config, cannot fetch.")
    exit()

def random_lyrics():
    lyrics = fetcher.random_lyrics()
    if not lyrics:
        return "No lyrics found."

    paragraphs = re.split(r'\n{2,}', lyrics)
    paragraph = random.choice(paragraphs)

    max_lines = config.max_lines
    powers = [2]
    for i in range(2, max_lines):
        n = 2 ** i
        if n >= max_lines: break
        powers.append(n)
    n_lines = random.choice(powers)

    return "\n".join(paragraph.split("\n")[:n_lines])

if __name__ == "__main__":
    print(random_lyrics())

