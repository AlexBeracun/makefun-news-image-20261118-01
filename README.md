# makefun-news-image-20261118-01

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/AlexBeracun/makefun-news-image-20261118-01/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/AlexBeracun/makefun-news-image-20261118-01/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image summing up Wednesday 18 November 2026's world news, as a
newspaper front page: "THE WORLD IN ONE PAGE".

Lead story: the Gulf flashpoint — US jets strike a Revolutionary Guard
missile site on Qeshm Island, Iran fires drones at US sites in Bahrain
and Kuwait. Then the Kerch bridge hit again, the APEC summit opening in
Shenzhen ahead of Thursday's first Trump–Xi–Putin three-way meeting,
Peltola winning Alaska to give Democrats a 56–44 Senate majority, the
Ebola outbreak in Congo passing 11,000 cases, Voyager 1 reaching one
light-day from Earth, and the US losing its measles-free status — plus
Gaza, the Siberia plane crash and Cyclone Xavier in the "Also today"
strip. Every event happened or was first reported on 18 November 2026.

## How it is built

`gen_image.py` renders `entry.png` (1024×1024, Pillow + system fonts)
from the day's wire reports. `main.py` is the graded entry: Python 3.13,
standard library only, no network — it just copies `entry.png` to the
output directory, so two runs write identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# out/entry.png — 1024x1024 PNG, under 1 MiB
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=ajkq5baq&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
