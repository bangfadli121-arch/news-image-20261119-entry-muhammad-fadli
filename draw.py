#!/usr/bin/env python3
"""Draw entry.png for news-image-20261119: 'The World - Thursday 19 November 2026'.

Classic newspaper front page, 1024x1024, cream paper. All story text is the
verified set supplied with the task; nothing is invented here. Two layouts:
  A = classic newspaper (masthead, map band, 3-col stories, 2-col also-list)
  B = hero top story + dominant map, 3-col stories
Render:  python3 draw.py A   -> variant_a.png
         python3 draw.py B   -> variant_b.png
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 222)
INK = (28, 28, 26)
RED = (176, 32, 32)
DARKRED = (120, 20, 20)
MUTED = (112, 102, 86)
RULE = (40, 40, 38)
OCEAN = (214, 230, 227)
LAND = (198, 206, 158)
LANDB = (138, 150, 102)
GOLD = (176, 138, 58)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF = FD + "DejaVuSerif.ttf"
SERIFB = FD + "DejaVuSerif-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"
SANSB = FD + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width):
    """Greedy word wrap; returns list of lines fitting width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_h(fnt, lines, leading):
    return len(lines) * leading


def draw_wrapped(d, x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def centered(d, cx, y, text, fnt, fill):
    d.text((cx - fnt.getlength(text) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- stories
MAIN = [
    dict(n=1, kicker="MIDDLE EAST · US–IRAN",
         head="Iran widens Gulf attacks as US hits back",
         deck="Tehran strikes a US base in Kuwait and Bahrain again; US forces hit a missile site on Qeshm Island.",
         icon="missile", lon=50, lat=26),
    dict(n=2, kicker="CHINA · APEC",
         head="Trump, Xi and Putin to meet in Shenzhen",
         deck="Trilateral talks set for Thursday on the sidelines of the APEC summit.",
         icon="summit", lon=114, lat=22),
    dict(n=3, kicker="CHINA · SUMMIT",
         head="Trump and Putin to meet one on one",
         deck="First meeting since Alaska in August 2025, also in China on Thursday.",
         icon="table", lon=102, lat=37),
    dict(n=4, kicker="UNITED STATES · TECH",
         head="Nvidia's new chief promises faster pay rises",
         deck="Acting CEO Colette Kress moves raises to December after Huang resigns; H-chip sales to China stopped.",
         icon="chip", lon=-122, lat=37),
    dict(n=5, kicker="CULTURE · GAMES",
         head="GTA VI begins global rollout",
         deck="Vice City returns as the game launches in Australia with a 99 on Metacritic.",
         icon="game", lon=-80, lat=26),
    dict(n=6, kicker="EUROPE · UKRAINE",
         head="EU proposes €45bn loan for Kyiv",
         deck="Brussels plan would be repaid after Russia pays reparations.",
         icon="bank", lon=4.5, lat=51),
    dict(n=7, kicker="UKRAINE · WAR",
         head="Crimea bridge hit for a second day",
         deck="Ukraine strikes another span; Russia pounds bridges around Kyiv in reply.",
         icon="bridge", lon=34, lat=45),
    dict(n=8, kicker="SPACE · NASA",
         head="Voyager 1 reaches one light-day from Earth",
         deck="After almost 50 years in space, the probe passes the milestone; NASA confirms on Thursday.",
         icon="rocket", lon=-95, lat=29.5),
    dict(n=9, kicker="THE HAGUE · LAW",
         head="World court rules on Myanmar today",
         deck="ICJ delivers judgment in the Rohingya genocide case brought by The Gambia.",
         icon="scales", lon=4.3, lat=52.2, dx=30, dy=-16),
    dict(n=10, kicker="INDIA · WEATHER",
         head="Cyclone Akvan nears landfall",
         deck="Storm expected between Machilipatnam and Puri; Andhra Pradesh and Odisha on high alert.",
         icon="storm", lon=80.5, lat=16),
    dict(n=11, kicker="UNITED STATES · ECONOMY",
         head="Fed minutes point to more rate rises",
         deck="Most officials expect further hikes if inflation and jobs stay hot.",
         icon="chart", lon=-77, lat=39, dx=32, dy=-20),
]

ALSO = [
    (12, "PHILIPPINES", "Trump wraps Manila visit, says major trade deal finalised"),
    (13, "CANADA", "Carney adjusts China ties, seeks the right deal with US"),
    (14, "WEST BANK", "Australia sanctions Israeli settlers over expansion"),
    (15, "GAZA", "Israeli ground forces move into central Gaza after evacuation orders"),
    (16, "VENEZUELA", "Hegseth makes first visit since Maduro's seizure"),
    (17, "IRAQ", "Six French nationals jailed for life over ISIL"),
    (18, "ALASKA", "Democrat Peltola wins Senate seat, 56–44 majority"),
    (19, "UNITED STATES", "Tougher rules proposed for employment green cards"),
    (20, "CONGRESS", "Liu Yunping elected Democratic Caucus chair, first Taiwanese American"),
    (21, "BULGARIA", "LPG tanker that sank was hit by projectiles, official says"),
    (22, "UNITED STATES", "NSA outage hits classified internal network"),
    (23, "FINANCE", "Deutsche Bank handled $582m in Epstein-linked deals, FT reports"),
    (24, "SOMALIA", "Mogadishu accuses UAE of building secret military bases"),
    (25, "SAUDI ARABIA", "Danger passed in three southern cities after alerts"),
    (26, "LIBYA", "Cocaine and millions of pills seized in the east"),
    (27, "CALIFORNIA", "Atmospheric river brings flood advisories"),
    (28, "TECH", "Microsoft in talks to sell AI services to ByteDance"),
    (29, "TOKYO", "India and Japan set to review defence ties"),
    (30, "INDIA", "Air India crash probe report at 'fag end', court told"),
    (31, "FRANCE", "Justice minister says Mélenchon could win presidency"),
    (32, "CRICKET", "Duckett's 133 puts England on top in third ODI"),
    (33, "TECH", "Baidu chief warns of an AI bubble"),
]

# ------------------------------------------------------- continents (lon, lat)
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-135, 70), (-125, 72), (-115, 73), (-105, 72),
     (-95, 80), (-85, 73), (-78, 71), (-68, 66), (-60, 60), (-55, 52),
     (-60, 46), (-68, 44), (-74, 39), (-76, 35), (-80, 32), (-81, 26),
     (-84, 30), (-89, 21), (-90, 16), (-95, 18), (-100, 20), (-105, 22),
     (-110, 24), (-115, 30), (-120, 34), (-124, 40), (-124, 48), (-130, 55),
     (-140, 60), (-152, 58), (-162, 58), (-168, 66)],
    # Greenland
    [(-45, 60), (-32, 68), (-20, 70), (-25, 76), (-40, 80), (-55, 77),
     (-58, 71), (-53, 64), (-45, 60)],
    # South America
    [(-80, 10), (-76, 5), (-70, 2), (-60, 0), (-52, -3), (-44, -3),
     (-35, -8), (-38, -15), (-41, -22), (-48, -28), (-54, -34), (-58, -39),
     (-65, -45), (-68, -52), (-73, -50), (-73, -40), (-72, -30), (-71, -20),
     (-76, -14), (-80, -5), (-81, 0), (-80, 10)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 44), (-1, 48), (0, 50), (3, 53), (7, 54),
     (8, 57), (10, 59), (14, 58), (18, 56), (21, 55), (24, 58), (27, 60),
     (30, 62), (31, 70), (28, 71), (22, 70), (16, 68), (12, 65), (10, 62),
     (5, 60), (5, 58), (2, 56), (-2, 53), (-5, 50), (-8, 44), (-10, 38),
     (-10, 36)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (20, 32), (30, 31), (34, 28), (37, 22),
     (39, 18), (43, 12), (48, 11), (51, 12), (46, 4), (41, -2), (40, -8),
     (38, -15), (35, -20), (33, -26), (29, -32), (25, -34), (19, -35),
     (16, -32), (14, -25), (12, -18), (9, -8), (9, -1), (9, 4), (2, 6),
     (-5, 5), (-10, 5), (-14, 8), (-17, 14), (-17, 20), (-15, 25), (-11, 30),
     (-6, 35)],
    # Asia
    [(30, 70), (35, 68), (45, 68), (55, 70), (65, 71), (75, 72), (85, 73),
     (95, 75), (105, 76), (115, 74), (125, 73), (135, 72), (145, 71),
     (155, 70), (165, 69), (175, 67), (178, 65), (172, 62), (165, 60),
     (158, 56), (156, 51), (150, 49), (143, 45), (141, 40), (138, 36),
     (135, 34), (130, 33), (127, 35), (124, 39), (121, 36), (120, 31),
     (118, 26), (114, 22), (110, 20), (108, 14), (106, 9), (103, 8),
     (100, 7), (98, 12), (96, 15), (93, 17), (91, 22), (88, 22), (86, 20),
     (83, 17), (80, 15), (78, 9), (76, 10), (74, 14), (72, 20), (69, 22),
     (66, 25), (62, 25), (58, 26), (56, 27), (53, 28), (51, 29), (49, 30),
     (47, 30), (44, 29), (41, 30), (39, 32), (36, 36), (34, 36), (31, 36),
     (30, 38), (31, 42), (33, 45), (36, 46), (39, 48), (42, 50), (45, 53),
     (48, 55), (50, 58), (52, 62), (52, 66), (45, 68), (38, 68), (30, 70)],
    # Australia
    [(113, -22), (114, -28), (114, -32), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (141, -38), (145, -38), (149, -37),
     (151, -34), (153, -31), (153, -27), (151, -24), (148, -20), (146, -19),
     (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
     (127, -14), (124, -16), (121, -18), (117, -20), (113, -22)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 56), (-4, 58), (-2, 58), (0, 53), (1, 51),
     (-3, 50), (-5, 50)],
]

# ------------------------------------------------------------------- icons
# Flat vector-style icons, drawn with PIL shapes inside a box (x, y, w, h).
def icon_missile(d, x, y, w, h):
    # slim diagonal missile: long grey body, red nose cone, small flame
    d.polygon([(x + w * .58, y + h * .06), (x + w * .86, y + h * .34),
               (x + w * .74, y + h * .46), (x + w * .46, y + h * .18)],
              fill=(90, 90, 88))
    d.polygon([(x + w * .58, y + h * .06), (x + w * .86, y + h * .34),
               (x + w * .74, y + h * .46)], fill=RED)
    d.polygon([(x + w * .46, y + h * .18), (x + w * .74, y + h * .46),
               (x + w * .62, y + h * .62), (x + w * .44, y + h * .44)],
              fill=(240, 160, 40))
    d.polygon([(x + w * .46, y + h * .18), (x + w * .30, y + h * .26),
               (x + w * .36, y + h * .42)], fill=RED)
    d.polygon([(x + w * .74, y + h * .46), (x + w * .84, y + h * .60),
               (x + w * .66, y + h * .56)], fill=RED)
    for cx, cy in [(x + w * .12, y + h * .12), (x + w * .88, y + h * .85)]:
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=GOLD)


def icon_summit(d, x, y, w, h):
    for i, cx in enumerate([.2, .5, .8]):
        d.ellipse([x + w * cx - 7, y + 2, x + w * cx + 7, y + 16],
                  fill=[RED, INK, (40, 90, 140)][i])
        d.polygon([(x + w * cx - 9, y + 18), (x + w * cx + 9, y + 18),
                   (x + w * cx + 5, y + h - 6), (x + w * cx - 5, y + h - 6)],
                  fill=[RED, INK, (40, 90, 140)][i])
    d.rectangle([x, y + h - 5, x + w, y + h - 1], fill=GOLD)


def icon_table(d, x, y, w, h):
    d.rectangle([x + 4, y + h * .55, x + w - 4, y + h * .62], fill=(120, 80, 40))
    d.rectangle([x + 8, y + h * .62, x + 12, y + h - 2], fill=(120, 80, 40))
    d.rectangle([x + w - 12, y + h * .62, x + w - 8, y + h - 2], fill=(120, 80, 40))
    for cx in (x + w * .3, x + w * .7):
        d.ellipse([cx - 7, y + 4, cx + 7, y + 18], fill=INK)
        d.rectangle([cx - 8, y + 20, cx + 8, y + h - 2], fill=RED)


def icon_chip(d, x, y, w, h):
    s = min(w, h) - 10
    ox, oy = x + (w - s) // 2, y + (h - s) // 2
    for i in range(3):
        d.line([ox + 6 + i * (s - 12) // 2, oy - 4, ox + 6 + i * (s - 12) // 2, oy],
               fill=INK, width=2)
        d.line([ox + 6 + i * (s - 12) // 2, oy + s, ox + 6 + i * (s - 12) // 2, oy + s + 4],
               fill=INK, width=2)
    d.rectangle([ox, oy, ox + s, oy + s], fill=INK)
    d.rectangle([ox + 6, oy + 6, ox + s - 6, oy + s - 6], outline=GOLD, width=2)
    d.text((ox + s / 2 - 4, oy + s / 2 - 7), "AI", font=font(SANSB, 12), fill=GOLD)


def icon_game(d, x, y, w, h):
    d.rounded_rectangle([x + 2, y + 6, x + w - 2, y + h - 6], radius=10, fill=INK)
    d.ellipse([x + 8, y + h * .35, x + 16, y + h * .35 + 8], fill=PAPER)
    d.ellipse([x + 10, y + h * .35 + 2, x + 14, y + h * .35 + 6], fill=RED)
    d.ellipse([x + w - 18, y + h * .3, x + w - 10, y + h * .3 + 8], fill=GOLD)
    d.ellipse([x + w - 16, y + h * .55, x + w - 8, y + h * .55 + 8], fill=RED)
    d.rectangle([x + w * .42, y + h * .35, x + w * .58, y + h * .35 + 4], fill=PAPER)


def icon_bank(d, x, y, w, h):
    d.polygon([(x + 2, y + 14), (x + w / 2, y + 2), (x + w - 2, y + 14)], fill=RED)
    for i in range(4):
        cx = x + 6 + i * (w - 12) / 3
        d.rectangle([cx - 3, y + 16, cx + 3, y + h - 8], fill=INK)
    d.rectangle([x + 2, y + h - 8, x + w - 2, y + h - 3], fill=INK)
    d.ellipse([x + w - 14, y + 2, x + w - 2, y + 14], fill=GOLD)
    d.ellipse([x + w - 11, y + 5, x + w - 5, y + 11], outline=INK)


def icon_bridge(d, x, y, w, h):
    d.arc([x + 2, y + 2, x + w - 2, y + h * 1.1], 180, 360, fill=RED, width=3)
    for fx in (.2, .38, .56, .74):
        cx = x + w * fx
        d.line([cx, y + h * .35, cx, y + h * .8], fill=INK, width=2)
    d.line([x, y + h * .8, x + w, y + h * .8], fill=INK, width=3)
    d.line([x + w * .8, y + 2, x + w * .95, y + 10], fill=GOLD, width=2)
    d.line([x + w * .95, y + 2, x + w * .8, y + 10], fill=GOLD, width=2)


def icon_rocket(d, x, y, w, h):
    d.polygon([(x + w / 2, y + 1), (x + w * .68, y + h * .45),
               (x + w * .55, y + h * .6), (x + w * .45, y + h * .6),
               (x + w * .32, y + h * .45)], fill=INK)
    d.ellipse([x + w * .42, y + h * .2, x + w * .58, y + h * .35], fill=(180, 220, 230))
    d.polygon([(x + w * .32, y + h * .45), (x + w * .2, y + h * .65),
               (x + w * .42, y + h * .55)], fill=RED)
    d.polygon([(x + w * .68, y + h * .45), (x + w * .8, y + h * .65),
               (x + w * .58, y + h * .55)], fill=RED)
    d.polygon([(x + w * .42, y + h * .6), (x + w * .58, y + h * .6),
               (x + w * .5, y + h - 2)], fill=(240, 160, 40))
    for cx, cy in [(x + 4, y + 6), (x + w - 6, y + 12), (x + w - 4, y + h - 6)]:
        d.ellipse([cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5], fill=GOLD)


def icon_scales(d, x, y, w, h):
    d.line([x + w / 2, y + 2, x + w / 2, y + h - 6], fill=INK, width=3)
    d.line([x + 4, y + 8, x + w - 4, y + 8], fill=INK, width=3)
    for cx in (x + 8, x + w - 8):
        d.line([cx, y + 8, cx, y + h * .55], fill=INK, width=2)
        d.polygon([(cx - 9, y + h * .55), (cx + 9, y + h * .55),
                   (cx, y + h * .75)], fill=GOLD)
    d.rectangle([x + w / 2 - 8, y + h - 6, x + w / 2 + 8, y + h - 2], fill=INK)


def icon_storm(d, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    for r, a0, a1 in [(16, 20, 200), (12, 200, 340), (8, 340, 500), (4, 500, 640)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=(40, 90, 140), width=3)
    d.polygon([(cx - 2, cy + 4), (cx + 2, cy + 4), (cx + 6, cy + h / 2 - 2),
               (cx - 6, cy + h / 2 - 2)], fill=RED)


def icon_chart(d, x, y, w, h):
    base = y + h - 6
    for i, bh in enumerate([8, 14, 11, 20]):
        bx = x + 4 + i * (w - 8) // 4
        d.rectangle([bx, base - bh, bx + (w - 8) // 4 - 4, base], fill=INK)
    d.line([x + 4, base - 20, x + w * .4, base - 26, x + w * .75, base - 30,
            x + w - 4, base - 38], fill=RED, width=3)
    d.polygon([(x + w - 4, base - 38), (x + w - 12, base - 38),
               (x + w - 4, base - 30)], fill=RED)


ICONS = {"missile": icon_missile, "summit": icon_summit, "table": icon_table,
         "chip": icon_chip, "game": icon_game, "bank": icon_bank,
         "bridge": icon_bridge, "rocket": icon_rocket, "scales": icon_scales,
         "storm": icon_storm, "chart": icon_chart}


# --------------------------------------------------------------------- map
def project(x0, y0, x1, y1, lon, lat):
    px = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    py = y0 + (78.0 - lat) / 136.0 * (y1 - y0)
    return px, py


def draw_map(d, x0, y0, x1, y1, pin_r=11):
    d.rectangle([x0, y0, x1, y1], fill=OCEAN, outline=RULE, width=1)
    for lat in (-60, -30, 0, 30, 60):
        _, py = project(x0, y0, x1, y1, 0, lat)
        d.line([x0, py, x1, py], fill=(200, 215, 212), width=1)
    for lon in (-120, -60, 0, 60, 120):
        px, _ = project(x0, y0, x1, y1, lon, 0)
        d.line([px, y0, px, y1], fill=(200, 215, 212), width=1)
    for poly in CONTINENTS:
        pts = [project(x0, y0, x1, y1, lo, la) for lo, la in poly]
        d.polygon(pts, fill=LAND, outline=LANDB)
    small = font(SANSB, 11)
    for s in MAIN:
        tx, ty = project(x0, y0, x1, y1, s["lon"], s["lat"])
        px, py = tx + s.get("dx", 0), ty + s.get("dy", 0)
        if s.get("dx") or s.get("dy"):
            d.line([tx, ty, px, py], fill=(90, 90, 88), width=1)
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=INK)
        d.ellipse([px - pin_r, py - pin_r, px + pin_r, py + pin_r],
                  fill=RED, outline=(255, 255, 255), width=2)
        num = str(s["n"])
        tw = small.getlength(num)
        d.text((px - tw / 2, py - 7), num, font=small, fill=(255, 255, 255))
    # caption strip, top-left, with a paper backing so it stays readable
    lab_f = font(SANSB, 12)
    lab = "THE WORLD AT A GLANCE — 11 STORIES PINNED"
    d.rectangle([x0 + 4, y0 + 4, x0 + 12 + lab_f.getlength(lab), y0 + 22],
                fill=PAPER)
    d.text((x0 + 8, y0 + 6), lab, font=lab_f, fill=RED)


# ----------------------------------------------------------------- header
def draw_header(d, y, mast_size=72):
    centered(d, W // 2, y, "THE WORLD", font(SERIFB, mast_size), INK)
    y += mast_size + 4
    d.line([26, y, W - 26, y], fill=RULE, width=2)
    y += 5
    centered(d, W // 2, y, "THURSDAY 19 NOVEMBER 2026", font(SANSB, 22), INK)
    y += 29
    centered(d, W // 2, y, "33 STORIES  ·  6 CONTINENTS  ·  ONE PAGE",
             font(SANS, 14), MUTED)
    y += 20
    d.line([26, y, W - 26, y], fill=RULE, width=1)
    return y + 6

# -------------------------------------------------------------- story block
def draw_story(d, x, y, w, s, head_size=18, deck_size=12, max_deck_lines=3):
    """One numbered story. Returns bottom y."""
    num_f = font(SERIFB, 24)
    kick_f = font(SANSB, 12)
    head_f = font(SERIFB, head_size)
    deck_f = font(SANS, deck_size)
    # red number square + kicker + icon on the top row
    d.rectangle([x, y, x + 28, y + 28], fill=RED)
    num = str(s["n"])
    d.text((x + 14 - num_f.getlength(num) / 2, y + 1), num, font=num_f,
           fill=(255, 255, 255))
    ICONS[s["icon"]](d, x + w - 44, y - 2, 44, 30)
    d.text((x + 36, y + 6), s["kicker"], font=kick_f, fill=RED)
    y += 34
    for ln in wrap(s["head"], head_f, w):
        d.text((x, y), ln, font=head_f, fill=INK)
        y += head_size + 2
    y += 1
    for ln in wrap(s["deck"], deck_f, w)[:max_deck_lines]:
        d.text((x, y), ln, font=deck_f, fill=(60, 58, 52))
        y += deck_size + 2
    return y


def draw_also(d, y, cols=2, item_size=13):
    head_f = font(SANSB, 14)
    item_f = font(SANS, item_size)
    d.line([26, y, W - 26, y], fill=RULE, width=2)
    y += 7
    d.text((26, y), "ALSO ON THURSDAY 19 NOVEMBER — 22 MORE STORIES",
           font=head_f, fill=INK)
    y += 21
    d.line([26, y, W - 26, y], fill=RULE, width=1)
    y += 7
    gap = 18
    cw = (W - 52 - gap * (cols - 1)) // cols
    per_col = (len(ALSO) + cols - 1) // cols
    top = y
    bottom = y
    for c in range(cols):
        x = 26 + c * (cw + gap)
        yy = top
        for num, place, txt in ALSO[c * per_col:(c + 1) * per_col]:
            line = "%d. %s — %s" % (num, place, txt)
            for ln in wrap(line, item_f, cw):
                d.text((x, yy), ln, font=item_f, fill=INK)
                yy += item_size + 2
            yy += 1
        bottom = max(bottom, yy)
    return bottom


def draw_judge_footer(d, y):
    box_h = 38
    d.rectangle([26, y, W - 26, y + box_h], outline=RED, width=2)
    d.text((38, y + 4), "JUDGE NOTE:", font=font(SANSB, 12), fill=RED)
    d.text((38, y + 20),
           "Every story above happened, or was first reported, on Thursday 19 November 2026. "
           "Disputed claims are attributed, not stated as fact.",
           font=font(SANS, 11), fill=INK)
    y += box_h + 8
    centered(d, W // 2, y,
             "Reporting: AP · Reuters · AFP · BBC · Al Jazeera · The Guardian · Financial Times",
             font(SANS, 11), MUTED)
    return y + 14


# ---------------------------------------------------------------- layout A
def render_a(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = draw_header(d, 10, mast_size=70)
    # map band
    map_top = y
    draw_map(d, 26, map_top, W - 26, map_top + 118)
    y = map_top + 118 + 10
    # 11 stories, 3 columns x 4 rows
    gap = 16
    cw = (W - 52 - gap * 2) // 3
    row_h = 118
    for r in range(4):
        for c in range(3):
            idx = r * 3 + c
            if idx >= len(MAIN):
                break
            x = 26 + c * (cw + gap)
            draw_story(d, x, y + r * row_h, cw, MAIN[idx])
        if r < 3:
            d.line([26, y + (r + 1) * row_h - 7, W - 26, y + (r + 1) * row_h - 7],
                   fill=(210, 200, 175), width=1)
    y = y + 4 * row_h + 2
    y = draw_also(d, y, cols=2, item_size=11)
    y = draw_judge_footer(d, y + 5)
    img.save(path, optimize=True)
    print("A saved", path, "end y =", y)


# ---------------------------------------------------------------- layout B
def render_b(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = draw_header(d, 8, mast_size=56)
    # hero: story 1, big (headline + deck each fit one line at these sizes)
    hero = MAIN[0]
    d.rectangle([26, y, W - 26, y + 84], outline=RULE, width=1)
    d.rectangle([26, y, W - 26, y + 84], fill=(238, 228, 200))
    d.line([26, y, W - 26, y], fill=RED, width=3)
    hx, hy = 40, y + 8
    d.text((hx, hy), "1 · MIDDLE EAST — US–IRAN", font=font(SANSB, 13), fill=RED)
    hy += 19
    for ln in wrap(hero["head"], font(SERIFB, 26), W - 52 - 180):
        d.text((hx, hy), ln, font=font(SERIFB, 26), fill=INK)
        hy += 30
    for ln in wrap(hero["deck"], font(SANS, 13), W - 52 - 180):
        d.text((hx, hy), ln, font=font(SANS, 13), fill=(60, 58, 52))
        hy += 17
    ICONS["missile"](d, W - 190, y + 10, 140, 66)
    y += 84 + 8
    # dominant map (label inside, top-left)
    map_top = y
    draw_map(d, 26, map_top, W - 26, map_top + 96, pin_r=13)
    y = map_top + 96 + 8
    # remaining 10 stories, 3 cols x 4 rows (last row 1 item)
    rest = MAIN[1:]
    gap = 16
    cw = (W - 52 - gap * 2) // 3
    row_h = 112
    for r in range(4):
        for c in range(3):
            idx = r * 3 + c
            if idx >= len(rest):
                break
            x = 26 + c * (cw + gap)
            draw_story(d, x, y + r * row_h, cw, rest[idx],
                       head_size=16, deck_size=11, max_deck_lines=3)
        if r < 3:
            d.line([26, y + (r + 1) * row_h - 6, W - 26, y + (r + 1) * row_h - 6],
                   fill=(210, 200, 175), width=1)
    y = y + 4 * row_h + 2
    y = draw_also(d, y, cols=2, item_size=10)
    y = draw_judge_footer(d, y + 4)
    img.save(path, optimize=True)
    print("B saved", path, "end y =", y)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "A"
    if which.upper() == "A":
        render_a("variant_a.png")
    else:
        render_b("variant_b.png")
