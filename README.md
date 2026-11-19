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
cp variant_a.png entry.png   # the file main.py ships
```

## v2 (19 Nov 2026, revision of the v1 entry)

Same 33 stories, word for word. Four fixes over v1: the map band is
taller (188 px, lat −60..84 so no coast is clipped) and North America is
redrawn with Hudson Bay, Florida and Baja, so it reads as a broad
continent instead of a thin strip; the missile (#1) and summit-meeting
(#3) icons are redrawn as concrete pictograms (upright rocket with
fins and flame; two figures at a table with two flags) and all icons
are slightly larger (52×34); story decks are 14 pt in darker ink and
the ALSO list is 12.5 pt, so small type stays readable; and the last
grid row gives stories 10 and 11 each half the grid width, so there is
no empty cell at bottom-right. End y is 1020.5 of 1024; two runs of
`draw.py A` are byte-identical.

## Why layout A was chosen

Two layouts were rendered and compared. A (classic newspaper) won: larger
masthead and story type (18/14 pt vs 16/11 pt in B), a larger map
(188 px tall vs 96 px — B's hero ate the space its "dominant map" needed),
larger list type, and a full story grid, while B left story 11 alone
in the last row and its big hero missile illustration read as a kite.
Both layouts fit all 33 stories with no clipped or truncated text;
A simply reads better, including at thumbnail size.

## v3 (19 Nov 2026, revision of v2)

Same 33 stories, word for word (verified: git diff v2→v3 touches no
MAIN/ALSO text); main.py unchanged. Three changes over v2, following the
top 1–2 pattern: (1) all 11 main cards get real photorealistic photos —
large panels (64 px) on heroes 1–3, photo banners on small cards 4–11
(11 generated photos in photos/, 1920x1280, centre-cropped + LANCZOS
downscale, no readable text in-frame, no close-up faces of real leaders;
hero 3 flags are US + Russia, hero 2 hall has 3 flags); (2) a big-numbers
strip under the masthead (€45bn · 99 · 50 yrs · 56–44 · $582m · 133 —
every number verified present in the 33 stories) plus a "THE DAY IN UTC"
strip with 5 slots drawn only from our stories (GTA VI rollout, ICJ
Myanmar judgment, Shenzhen summit, Voyager, Fed minutes — no Banxico,
no invented clock times, phases only); (3) the map is now a proportional
block (380x232) at bottom-left beside the ALSO list, not a thin strip.
End y is 1015 of 1024; asserts (kicker/headline/deck overflow, bottom
margin per card, ALSO within map block) all pass; 2x runs byte-identical.
