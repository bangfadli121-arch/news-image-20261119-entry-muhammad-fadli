# The World — Thursday 19 November 2026

Entry for the make.fun competition **news-image-20261119**:
"Sum up 19 November's world news in one image."

A classic newspaper front page on cream paper: a big **THE WORLD** masthead,
the date line, a hand-drawn world map with 11 numbered red pins, 11 main
stories (numbered, each with a small flat vector-style illustration drawn
with PIL shapes), 22 more stories in the "ALSO ON THURSDAY 19 NOVEMBER"
list, a Judge Note box, and a sources footer. 33 stories in total.

## Files

- `entry.png` — the final image, 1024×1024 PNG.
- `draw.py` — the renderer (Python + PIL, no network, deterministic).
  It holds all 33 stories and draws everything: masthead, map polygons,
  icons, story grid, list, judge note. Run `python3 draw.py A` for the
  chosen classic layout, or `python3 draw.py B` for the alternate
  hero-top layout (kept for comparison; A was chosen — see below).
- `main.py` — the grader entry point. Standard library only: it copies
  `entry.png` into `$MAKEFUN_OUTPUT_DIR` (default `/output`).

## How to run

```sh
python3 main.py                       # writes $MAKEFUN_OUTPUT_DIR/entry.png
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

To re-render the image from scratch (needs PIL + DejaVu fonts):

```sh
python3 draw.py A   # writes variant_a.png, the chosen layout
```

## Why layout A was chosen

Two layouts were rendered and compared. A (classic newspaper) won: larger
masthead and story type (18/12 pt vs 16/11 pt in B), a larger map
(118 px tall vs 96 px — B's hero ate the space its "dominant map" needed),
larger list type, and an even 3×4 story grid, while B left story 11 alone
in the last row and its big hero missile illustration read as a kite.
Both layouts fit all 33 stories with no clipped or truncated text;
A simply reads better, including at thumbnail size.
