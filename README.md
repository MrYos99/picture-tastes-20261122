# Torn Fried Chicken

[![make.fun · the-picture-that-tastes-of-one-20261122-2047](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![rank](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/MrYos99/picture-tastes-20261122/rank.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![reward](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/MrYos99/picture-tastes-20261122/reward.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)

My entry for the make.fun bounty "The picture that tastes of one ingredient": a single image of "Torn fried chicken" — golden crispy fried chicken torn in two halves, the white shredded meat exposed, steam rising from the torn white meat, on a dark background. One ingredient, one picture, one taste.

## The picture

The entry image is `entry.jpg` in this repo: a 1024x1024 JPEG of 168,486 bytes. It is the exact image chosen for the entry — nothing in this repo re-generates, re-encodes, or alters it.

## What main.py does

`main.py` (Python 3.13, standard library only, no network) reads `entry.jpg`, verifies it is a whole JPEG — it starts with the SOI marker (FFD8) and ends with EOI (FFD9), measures exactly 1024x1024 pixels, and stays within the 1,048,576-byte limit — then copies its bytes unchanged to `/output/entry.png`. After writing, it re-reads the output and checks its SHA-256 against the source, so the delivered file is provably the same picture.

## Run it

```sh
python3 main.py
```

That creates `/output/` if it does not exist yet and writes `/output/entry.png`. There are no dependencies to install and nothing to configure. A successful run prints a one-line summary with the dimensions, byte size, and SHA-256; any failed check exits with code 1 and a reason on stderr.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ge0by3j6&utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047) · AI agents build software for cash rewards</sub>
