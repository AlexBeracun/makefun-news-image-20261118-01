# makefun-news-image-20261118-01

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/AlexBeracun/makefun-news-image-20261118-01/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/AlexBeracun/makefun-news-image-20261118-01/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image summing up Wednesday 18 November 2026's world news, as a
newspaper front page: "THE WORLD IN ONE PAGE" — 32 verified stories
across six continents.

Lead story: the Gulf flashpoint — US jets strike a Revolutionary Guard
missile site on Qeshm Island, Iran fires drones at US sites in Bahrain
and Kuwait. Then four feature panels (Kerch bridge hit again, the APEC
summit in Shenzhen with Trump in Manila for the QUAD, Peltola winning
Alaska to give Democrats a 56–44 Senate majority, the Ebola outbreak in
Congo passing 11,200 cases and 5,500 deaths) plus 27 briefs: Voyager 1
reaching one light-day from Earth, the US losing measles-free status,
the COP31 split in Antalya, Nvidia's record $115.8bn quarter, Gaza,
Cyclone Xavier, the Knesset speaker vote, Houthi drones on a Saudi
pipeline, a wave of bomb threats across Europe, and more. Every event
happened or was first reported on 18 November 2026.

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
