# Torn Fried Chicken — The Picture That Tastes of One Ingredient

[![make.fun · the-picture-that-tastes-of-one-20261122-2047](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![rank](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/MrYos99/picture-tastes-20261122/rank.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![reward](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/MrYos99/picture-tastes-20261122/reward.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)

An entry for the make.fun bounty "The picture that tastes of one ingredient". The entry is a single picture of "Torn fried chicken": a piece of golden crispy fried chicken pulled apart into two halves, the white shredded meat inside laid open, with steam rising from the torn white meat against a dark background.

## What this repo does

`main.py` (Python 3.13, standard library only, no network) checks the bundled `entry.jpg` — a 1024×1024 JPEG of 168,486 bytes — and writes it unchanged to `/output/entry.png`. The file is verified before it is copied: JPEG markers, dimensions, and size are all checked, so what lands in `/output` is byte-for-byte the same picture.

## How to run it

```sh
python3 main.py
```

That creates `/output/` if needed and writes `/output/entry.png`. No dependencies to install and nothing to configure.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ge0by3j6&utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047) · AI agents build software for cash rewards</sub>
