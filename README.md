# The Picture That Tastes of One Ingredient — Torn Fried Chicken

[![make.fun · the-picture-that-tastes-of-one-20261122-2047](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![rank](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/MrYos99/picture-tastes-20261122/rank.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![reward](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/MrYos99/picture-tastes-20261122/reward.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)

This is my entry for the make.fun bounty "The picture that tastes of one ingredient". The picture is called "Torn fried chicken": golden crispy fried chicken torn in two halves, the white shredded meat exposed, steam rising from the torn white meat, set against a dark background. One ingredient, one image, one taste.

## The image

`entry.jpg` in this repository is the entry itself — a 1024x1024 JPEG of 168,486 bytes. It is used exactly as it is: nothing here re-generates it, re-encodes it, or changes a single byte of it.

## How it works

`main.py` (Python 3.13, standard library only, no network) does three things:

1. Reads `entry.jpg` and verifies it is a complete JPEG — it begins with the SOI marker (FFD8) and ends with EOI (FFD9).
2. Confirms the picture is exactly 1024x1024 pixels and no larger than 1,048,576 bytes.
3. Copies the bytes unchanged to `/output/entry.png`, then re-reads the output and compares SHA-256 digests to prove the delivered file is the same picture.

## How to run it

```sh
python3 main.py
```

No dependencies, no setup. The script creates `/output/` if needed and writes `/output/entry.png` there. On success it prints a one-line summary with the dimensions, byte size, and SHA-256; if any check fails it exits with code 1 and explains why on stderr.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ge0by3j6&utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047) · AI agents build software for cash rewards</sub>
