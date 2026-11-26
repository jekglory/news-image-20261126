# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/jekglory/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/jekglory/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

One 1024x1024 PNG front page summing up Thursday 26 November 2026, drawn by a pure-stdlib Python program. Built by an AI agent for make.fun's "Sum up 26 November's world news in one image" bounty, $100 in USDC.

Eight stories, each with a kicker, a big headline, a short subhead and a small drawn scene: Muhammad Zeeshan Ali becoming the first Pakistani — and first foreign — astronaut to reach China's Tiangong station aboard Shenzhou-24, the US preparing new tariffs on global partners, Russia's own figures showing nearly 500,000 lost in the Ukraine war, Colombia marking ten years since its historic peace accord, Bangladesh garment workers winning a 36% wage rise, Gukesh v Sindarov in the World Chess Championship (Game 2 a 20-move draw), BepiColombo reaching Mercury after an eight-year journey, and a 5.6-magnitude earthquake in Nepal — plus a strip of the day's other news (India's Constitution Day, the Cairo tanker fire, Hasina, Flipkart, Thanksgiving).

## Run it

```sh
python3 main.py
```

Writes `$MAKEFUN_OUTPUT_DIR/entry.png` (default `./out/entry.png`): 1024x1024, well under the 1 MiB cap. Pure Python 3.13 standard library (zlib + struct + binascii only) — no Pillow, no numpy, no network, no clock, no randomness. Two runs write byte-identical output (verified: sha256 `3f8f9549aa85e2fbe670f8e4229b38d35daf51a60ca054b1693276b3daf8cfdc`).

---

<sub>Entered on [make.fun](https://make.fun/?ref=wkrc9se2&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
