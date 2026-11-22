# news-image-20261121

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/arestafirman/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/arestafirman/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

One broadsheet image summing up the world's news of **Saturday 21 November 2026** — 42 dated stories, drawn entirely in code (Python + PIL, no photos, no downloads).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. To redraw the poster from scratch:

```sh
python3 generate_image.py
```

The render is fully deterministic: two runs produce byte-identical PNGs.

## What's in the picture

- **42 stories, all dated Saturday 21 November 2026**: 3 heroes (COP31 overtime in Antalya, five Houthi missiles shot down over Riyadh and Jizan, the M6.7 Peru quake), 10 medium tiles, and 29 more in the numbered list.
- **Regions**: Europe 5 · Asia 12 · Middle East 5 · Africa 2 · Americas 10 · Oceania 4 · Global 4 (= 42).
- **Six big numbers**: Day 13 of COP31 · 5 missiles down (3 over Riyadh + 2 over Jizan) · 6.7 magnitude in Peru · 146 people safe after the Davao landing · $58,983 bitcoin early Saturday (CoinGecko 02:08 UTC) · 124* for Rahul at tea in Wellington.
- **Timeline "THE DAY IN UTC"**: 7 points from the Davao landing after midnight to Rahul's century at tea, with BepiColombo's Mercury capture framed as due 19:24 CET, not done.
- **A numbered world map** (positions approximate) and a **DATE CHECK** box naming the other days' news left out — including the Kim Keon Hee verdict (19 Nov), Mlambo-Ngcuka's death (20 Nov) and Indonesia's asset-seizure law (19 Nov).
- Every tile carries a status badge — CONFIRMED (2+ outlets), OFFICIAL (on the record), REPORTED (one outlet), CLAIM (one side's account) — explained in the footer legend.
