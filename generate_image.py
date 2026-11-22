# generate_image.py — draws the news-image-20261121 entry from scratch.
# One broadsheet poster, 1024x1024, summing up Saturday 21 November 2026.
# Everything here is original vector art drawn in code: no photos, no downloads,
# no network, no clock, no unseeded randomness. Two runs must give byte-identical PNGs.
# Written for the make.fun bounty news-image-20261121 (entry by @ares).

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette: cream paper, brick red, navy ink ------------------------------
PAPER = (247, 240, 224)
PAPER2 = (241, 232, 210)
INK = (24, 30, 46)
NAVY = (31, 58, 95)
BRICK = (178, 58, 38)
BRICK_DK = (140, 44, 28)
GOLD = (198, 148, 52)
TEAL = (42, 122, 110)
SKY = (126, 178, 214)
SKY_DK = (58, 110, 158)
NIGHT = (18, 32, 64)
GREEN = (74, 140, 74)
BROWN = (122, 84, 52)
GREY = (110, 108, 100)
LINE = (180, 168, 140)
WHITE = (252, 250, 244)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# --- text helpers -----------------------------------------------------------
def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, spacing=2):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap_text(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def fit_text(draw, text, fnt, max_w):
    """Shrink the font (same family file) until the text fits one line."""
    size = fnt.size
    path = fnt.path
    while size > 9 and draw.textlength(text, font=fnt) > max_w:
        size -= 1
        fnt = ImageFont.truetype(path, size)
    return fnt


def badge(draw, x, y, label, fill):
    """Small status badge; returns width used."""
    fnt = font(SANS_B, 9)
    tw = draw.textlength(label, font=fnt)
    w = int(tw) + 10
    draw.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=fill)
    draw.text((x + 5, y + 2), label, font=fnt, fill=WHITE)
    return w


BADGE_FILL = {"CONFIRMED": TEAL, "OFFICIAL": NAVY, "REPORTED": (120, 96, 40),
              "CLAIM": BRICK}

# --- the 42 stories ---------------------------------------------------------
# region codes: EU Europe, AS Asia, ME Middle East, AF Africa,
#               AM Americas, OC Oceania, GL Global
# (num, region, place, beat, headline, body, source, status)
HEROES = [
    (1, "GL", "ANTALYA, TÜRKIYE", "CLIMATE",
     "Climate summit runs into Saturday with no deal",
     "COP31 missed its Friday close; a draft with no fossil-fuel mention "
     "split nearly 200 countries.",
     "AP, Al Jazeera", "CONFIRMED"),
    (2, "ME", "RIYADH · JIZAN", "WAR",
     "Five Houthi missiles shot down over Saudi Arabia",
     "Coalition: three destroyed over Riyadh before dawn, two over Jizan, "
     "a day after it bombed Hodeidah port.",
     "AFP, Dawn", "OFFICIAL"),
    (3, "AM", "JUNÍN, PERU", "EARTHQUAKE",
     "Magnitude 6.7 earthquake shakes central Peru",
     "Deep quake near Carhuamayo felt in Lima and on the coast; no deaths, "
     "damage or tsunami risk. 00:09 UTC.",
     "USGS, IGP", "OFFICIAL"),
]

TILES = [
    (4, "EU", "KYIV", "WAR",
     "Zelensky: Crimea bridge \u201cwill not stay\u201d",
     "He warns of more double-tap strikes (NBC interview).",
     "NBC", "REPORTED"),
    (5, "ME", "STRAIT OF HORMUZ", "WAR",
     "Iran says it shot down a US drone",
     "Tehran claims it; no confirmation from Washington.",
     "IRIB", "CLAIM"),
    (6, "ME", "TEHRAN", "DIPLOMACY",
     "Iran: uranium stock stays in the country",
     "Minister still seeks a \u201cfair solution\u201d.",
     "Times of Israel", "REPORTED"),
    (7, "AM", "WASHINGTON", "TECHNOLOGY",
     "Trump vows tax on data centres abroad",
     "\u201cTremendous\u201d penalty, he says; no details yet.",
     "ABC", "REPORTED"),
    (8, "AS", "BEIJING", "DIPLOMACY",
     "China: Japan must \u201ccorrect\u201d Taiwan words",
     "Tokyo says its stance is unchanged.",
     "Ministry, AFP", "OFFICIAL"),
    (9, "AS", "DAVAO", "AVIATION",
     "Jet lands safely after engine-fire alert",
     "Air Niugini 767 diverts after midnight; all 146 safe.",
     "Airline, AP", "OFFICIAL"),
    (10, "OC", "CANBERRA", "DIPLOMACY",
     "Australia and China agree to AI talks",
     "Albanese ends an 11-day trip to Beijing.",
     "ABC", "OFFICIAL"),
    (11, "GL", "WORLD", "MARKETS",
     "Bitcoin trades below $59,000 on Saturday",
     "$58,983 early Saturday, down 3.9%; ether $1,625.",
     "CoinGecko 02:08 UTC", "CONFIRMED"),
    (12, "AM", "LAS VEGAS", "FORMULA ONE",
     "Russell fastest in final Las Vegas practice",
     "1:34.041 in a damp session; Verstappen to stewards.",
     "Formula 1, Autosport", "OFFICIAL"),
    (13, "OC", "WELLINGTON", "CRICKET",
     "Rahul hits a century against New Zealand",
     "India 344 for 2 at tea, replying to 368; Rahul 124*.",
     "AFP", "OFFICIAL"),
]

# (num, region, one-line entry incl. source in brackets)
LIST_ITEMS = [
    (14, "EU", "Kryvyi Rih \u2014 Double strike kills 2, injures 42 (Kyiv Independent)"),
    (15, "EU", "Copenhagen \u2014 Russian attach\u00e9 expelled over a plot (Al Jazeera)"),
    (16, "GL", "Antalya \u2014 EU warns COP31 risks a \u201cfossil summit\u201d (AFP)"),
    (17, "AM", "Antalya \u2014 Panama threatens to block the climate deal (Al Jazeera)"),
    (18, "AS", "Antalya \u2014 Indonesia\u2019s PLN signs clean-power deals (Antara)"),
    (19, "ME", "Yemen \u2014 Houthis threaten Jeddah and Red Sea ports (Al Jazeera)"),
    (20, "AM", "Washington \u2014 Vance: Iran strikes were Trump\u2019s call (Reuters)"),
    (21, "AM", "Washington \u2014 Lawmaker threatens SpaceX\u2019s funding (CNN)"),
    (22, "AM", "Texas \u2014 Execution of a man of 70 takes 63 minutes (ABC)"),
    (23, "AM", "Los Angeles \u2014 Jury convicts man over Palisades fire (ABC)"),
    (24, "AM", "Missouri \u2014 Judge approves $7.25bn Roundup deal (AFP)"),
    (25, "AM", "Vancouver \u2014 Canada rests defence in climate trial (AFP)"),
    (26, "AS", "Pyongyang \u2014 Kim tours factories after no Trump meeting (AFP)"),
    (27, "AS", "Sejong \u2014 Freight train derails; no one hurt (Korea Herald)"),
    (28, "AS", "Taipei \u2014 Budget and a cash payout are passed (Taipei Times)"),
    (29, "AS", "Bangkok \u2014 Six-point plan on arsenic in two rivers (The Nation)"),
    (30, "AS", "New Delhi \u2014 Pakistani minister joins SCO forum (Dawn)"),
    (31, "AS", "Eastern India \u2014 Rain alerts as Akvan remnants move inland (ETV)"),
    (32, "AS", "Myanmar \u2014 Rights groups urge sanctions after ruling (AP)"),
    (33, "AF", "Port Louis \u2014 Ratings agency talks to 15 states (Al Jazeera)"),
    (34, "OC", "Melbourne \u2014 Cummins keeps the Australian captaincy (ABC)"),
    (35, "EU", "Warsaw \u2014 Rutte flies in for NATO talks (AP)"),
    (36, "AF", "Bayelsa \u2014 Barge capsizes; 4 dead, 24 saved, 100+ missing (Reuters)"),
    (37, "GL", "Mercury \u2014 BepiColombo capture due 19:24 CET (ESA)"),
    (38, "ME", "Hodeidah \u2014 Strikes hit port; Houthis warn airlines (UN, AP)"),
    (39, "AS", "New Delhi \u2014 Air stays poor; AQI 279 at 7 am (CPCB, ANI)"),
    (40, "EU", "Geneva \u2014 States aim for \u201ckiller robot\u201d rules by 2028 (Reuters)"),
    (41, "OC", "Sydney \u2014 Board backs Cummins as captain (ABC)"),
    (42, "AS", "Visayas \u2014 Grid on yellow alert, 5\u20138 pm (NGCP)"),
]

REGION_NAMES = [("EUROPE", "EU"), ("ASIA", "AS"), ("MIDDLE EAST", "ME"),
                ("AFRICA", "AF"), ("AMERICAS", "AM"), ("OCEANIA", "OC"),
                ("GLOBAL", "GL")]

# (big number, label line 1, label line 2)
BIG_NUMBERS = [
    ("13", "DAY OF COP31", "planned to close day 12"),
    ("5", "MISSILES SHOT DOWN", "3 over Riyadh + 2 over Jizan"),
    ("6.7", "PERU QUAKE", "00:09 UTC, 108 km deep"),
    ("146", "PEOPLE SAFE", "after jet\u2019s Davao landing"),
    ("$58,983", "BITCOIN, EARLY SAT.", "CoinGecko 02:08 UTC"),
    ("124*", "RAHUL AT TEA", "India 344 for 2, Wellington"),
]

# (time label, place, what happened)
TIMELINE = [
    ("AFTER MIDNIGHT", "Davao", "767 lands safely; 146 safe"),
    ("00:09 UTC", "Jun\u00edn, Peru", "M6.7 quake strikes"),
    ("~02:00 UTC", "Riyadh", "3 down; 2 over Jizan"),
    ("MORNING UTC", "Antalya", "COP31 misses close"),
    ("19:24 CET", "Mercury", "Capture due"),
    ("EVENING UTC", "Las Vegas", "Russell fastest"),
    ("TEA", "Wellington", "Rahul 124*"),
]

DATE_CHECK = (
    "DATE CHECK \u2014 Every story here happened, or was first reported, on Saturday "
    "21 November 2026. LEFT OUT as other days\u2019 news: Kim Keon Hee\u2019s 4-year term "
    "(19 Nov) \u00b7 Mlambo-Ngcuka\u2019s death (20 Nov) \u00b7 Indonesia\u2019s asset-seizure "
    "law passed (19 Nov) \u00b7 Wall Street\u2019s fall into a correction (20 Nov) \u00b7 the "
    "Russian barrage on Kyiv\u2019s bridges (20 Nov) \u00b7 the missile that landed in "
    "Poland (20 Nov) \u00b7 the UK\u2013EU deal (20 Nov) \u00b7 Cyclone Akvan\u2019s landfall "
    "(20 Nov) \u00b7 Gaza strikes that killed six (20 Nov) \u00b7 Voyager 1\u2019s light-day "
    "(18 Nov) \u00b7 Shenzhen summit (19 Nov) \u00b7 GTA VI launch (19 Nov) \u00b7 "
    "Anthropic debut, shares up 17% (19 Nov) \u00b7 ICJ Myanmar genocide ruling "
    "(19\u201320 Nov). Not confirmed when drawn, so not shown as done: BepiColombo in "
    "Mercury orbit (due 19:24 CET) \u00b7 a final COP31 text."
)


# --- hero illustrations (original vector art, drawn in code) -----------------
def draw_hero_cop31(d, x, y, w, h):
    """Antalya climate summit: sky, sun, green hills, thermometer, DAY 13."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + w - 44, y + 5, x + w - 16, y + 33], fill=(250, 214, 110))
    d.ellipse([x + w - 37, y + 12, x + w - 23, y + 26], fill=(255, 232, 150))
    # distant hills, then green foreground hill
    d.polygon([(x, y + h), (x, y + h - 20), (x + w * 0.35, y + h - 28),
               (x + w * 0.62, y + h - 18), (x + w, y + h - 24), (x + w, y + h)],
              fill=(96, 150, 110))
    d.polygon([(x, y + h), (x, y + h - 8), (x + w * 0.4, y + h - 14),
               (x + w * 0.7, y + h - 6), (x + w, y + h - 10), (x + w, y + h)],
              fill=GREEN)
    # little wind turbines on the hill
    for tx in (x + int(w * 0.18), x + int(w * 0.82)):
        ty = y + h - 24
        d.line([tx, ty, tx, ty - 14], fill=WHITE, width=2)
        for ang in (90, 210, 330):
            import math as _m
            ex = tx + int(7 * _m.cos(_m.radians(ang)))
            ey = ty - 14 + int(7 * _m.sin(_m.radians(ang)))
            d.line([tx, ty - 14, ex, ey], fill=WHITE, width=2)
    # thermometer, left side
    tx, ty, tw, th = x + 10, y + 5, 13, h - 12
    d.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=6, fill=WHITE,
                        outline=NAVY, width=2)
    d.ellipse([tx - 4, ty + th - 6, tx + tw + 4, ty + th + 8], fill=WHITE,
              outline=NAVY, width=2)
    d.rectangle([tx + 4, ty + 8, tx + tw - 4, ty + th - 2], fill=(220, 120, 100))
    d.ellipse([tx, ty + th - 5, tx + tw, ty + th + 7], fill=BRICK)
    # DAY 13 roundel, right side
    cx, cy, r = x + w - 34, y + h - 18, 18
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BRICK, outline=WHITE, width=2)
    d.text((cx, cy - 10), "DAY", font=font(SANS_B, 8), fill=WHITE, anchor="mt")
    d.text((cx, cy - 2), "13", font=font(SANS_B, 14), fill=WHITE, anchor="mt")


def draw_hero_riyadh(d, x, y, w, h):
    """Riyadh at night: navy sky, stars, crescent, skyline, 5 intercepts."""
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    # stars
    for sx, sy, sr in [(0.12, 0.14, 2), (0.30, 0.08, 1), (0.52, 0.18, 2),
                       (0.68, 0.08, 1), (0.85, 0.22, 2), (0.42, 0.30, 1),
                       (0.08, 0.38, 1), (0.94, 0.42, 1)]:
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr,
                   y + h * sy + sr], fill=(255, 240, 180))
    # crescent moon
    d.ellipse([x + w - 58, y + 8, x + w - 26, y + 40], fill=(250, 240, 200))
    d.ellipse([x + w - 50, y + 4, x + w - 20, y + 38], fill=NIGHT)
    # skyline silhouettes
    base = y + h
    for bx, bw, bh in [(0.00, 0.16, 22), (0.14, 0.12, 30), (0.26, 0.14, 24),
                       (0.40, 0.10, 36), (0.50, 0.16, 22), (0.66, 0.12, 28),
                       (0.78, 0.12, 20), (0.90, 0.10, 26)]:
        d.rectangle([x + w * bx, base - bh, x + w * (bx + bw), base],
                    fill=(10, 20, 44))
    # tower spire on the tallest block
    d.line([x + w * 0.45, base - 36, x + w * 0.45, base - 44], fill=(10, 20, 44),
           width=3)
    d.ellipse([x + w * 0.45 - 3, base - 48, x + w * 0.45 + 3, base - 42],
              fill=GOLD)
    # lit windows
    for wx, wy in [(0.05, 0.78), (0.18, 0.66), (0.30, 0.74), (0.44, 0.60),
                   (0.55, 0.76), (0.70, 0.64), (0.82, 0.78), (0.93, 0.68)]:
        d.rectangle([x + w * wx, y + h * wy, x + w * wx + 5, y + h * wy + 5],
                    fill=GOLD)
    # five intercept bursts with streaks
    bursts = [(0.16, 0.30), (0.36, 0.20), (0.55, 0.34), (0.74, 0.22),
              (0.88, 0.38)]
    for bx, by in bursts:
        cx, cy = x + w * bx, y + h * by
        d.line([cx - 26, cy + 18, cx, cy], fill=(255, 200, 90), width=2)
        for dx, dy in [(0, -9), (0, 9), (-9, 0), (9, 0), (-6, -6), (6, -6),
                       (-6, 6), (6, 6)]:
            d.line([cx, cy, cx + dx, cy + dy], fill=(255, 220, 120), width=2)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 240, 190))


def draw_hero_peru(d, x, y, w, h):
    """Peru quake: brown mountains, seismograph strip, small house, M6.7."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 178))
    # mountains
    d.polygon([(x, y + h), (x, y + h - 24), (x + w * 0.28, y + h - 40),
               (x + w * 0.5, y + h - 22), (x + w * 0.72, y + h - 36),
               (x + w, y + h - 18), (x + w, y + h)], fill=BROWN)
    d.polygon([(x + w * 0.28 - 10, y + h - 34), (x + w * 0.28, y + h - 40),
               (x + w * 0.28 + 10, y + h - 34)], fill=(250, 246, 236))
    d.polygon([(x + w * 0.72 - 9, y + h - 31), (x + w * 0.72, y + h - 36),
               (x + w * 0.72 + 9, y + h - 31)], fill=(250, 246, 236))
    # seismograph paper strip across the middle (stops before M6.7 roundel)
    sy = y + 6
    d.rectangle([x + 8, sy, x + w - 58, sy + 24], fill=WHITE, outline=INK, width=1)
    pts = []
    import math as _m
    for i in range(0, int(w) - 66):
        t = i / max(1, int(w) - 66)
        amp = 1 + 8 * _m.exp(-((t - 0.45) ** 2) / 0.012)
        yy = sy + 12 + amp * _m.sin(i * 0.9) * (1 if i % 2 else -1)
        pts.append((x + 8 + i, yy))
    d.line(pts, fill=BRICK, width=2)
    # small house, lower left, with a crack
    hx, hy = x + 16, y + h - 26
    d.rectangle([hx, hy, hx + 36, hy + 18], fill=(214, 178, 130),
                outline=INK, width=1)
    d.polygon([(hx - 3, hy), (hx + 18, hy - 11), (hx + 39, hy)],
              fill=BRICK_DK)
    d.rectangle([hx + 14, hy + 8, hx + 22, hy + 18], fill=NAVY)
    d.line([hx + 25, hy + 1, hx + 28, hy + 7, hx + 25, hy + 13], fill=INK,
           width=2)
    # M6.7 roundel, lower right
    cx, cy, r = x + w - 32, y + h - 16, 18
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY, outline=WHITE,
              width=2)
    d.text((cx, cy - 8), "M6.7", font=font(SANS_B, 11), fill=WHITE,
           anchor="mt")


HERO_ART = [draw_hero_cop31, draw_hero_riyadh, draw_hero_peru]

# --- world map (schematic continents, drawn in code) ------------------------
# Coarse lon/lat outlines; equirectangular projection into the map box.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-85, 66), (-75, 62),
     (-65, 60), (-55, 52), (-60, 47), (-70, 44), (-75, 39), (-80, 32),
     (-81, 26), (-90, 21), (-97, 16), (-94, 17), (-105, 20), (-110, 23),
     (-117, 33), (-125, 40), (-125, 49), (-130, 55), (-150, 60), (-165, 60)],
    # South America
    [(-80, 9), (-72, 12), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-40, -20), (-48, -28), (-57, -38), (-65, -45), (-68, -52),
     (-70, -54), (-73, -44), (-73, -30), (-70, -18), (-77, -12), (-81, -5),
     (-80, 2)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (40, 15), (43, 11), (48, 11), (51, 10), (44, 0), (40, -10), (35, -18),
     (32, -26), (26, -34), (20, -35), (15, -27), (12, -18), (13, -10),
     (9, 4), (-8, 4), (-13, 8), (-17, 12)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 70), (40, 68), (55, 68),
     (70, 72), (90, 75), (110, 76), (130, 72), (150, 70), (170, 66),
     (178, 65), (170, 60), (162, 56), (158, 52), (142, 50), (140, 40),
     (135, 35), (130, 33), (122, 30), (120, 22), (110, 20), (108, 12),
     (105, 9), (100, 8), (98, 12), (94, 17), (90, 22), (86, 20), (80, 13),
     (77, 8), (73, 16), (70, 22), (66, 25), (61, 25), (57, 26), (54, 26),
     (50, 29), (48, 30), (44, 29), (40, 32), (36, 36), (33, 36), (30, 36),
     (27, 37), (23, 36), (19, 40), (15, 44), (12, 44), (8, 44), (3, 43),
     (-1, 44), (-2, 47), (-5, 48)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (136, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -23), (146, -19), (142, -11), (137, -12), (135, -15), (132, -12),
     (130, -13), (126, -14), (122, -17), (118, -20)],
]

ISLANDS = [(-2, 54), (139, 37), (118, -2), (172, -41), (103, 1), (127, 37)]

# lon/lat of every numbered story that has a place on Earth
# (11 Bitcoin is global; 37 BepiColombo is at Mercury — no Earth dot)
MAP_POINTS = {
    1: (30.7, 36.9), 2: (46.7, 24.6), 3: (-75.9, -11.2), 4: (30.5, 50.4),
    5: (56.5, 26.5), 6: (51.4, 35.7), 7: (-77.0, 38.9), 8: (116.4, 39.9),
    9: (125.6, 7.1), 10: (149.1, -35.3), 12: (-115.1, 36.2),
    13: (174.8, -41.3),
    14: (33.4, 47.9), 15: (12.6, 55.7), 16: (30.7, 36.9), 17: (30.7, 36.9),
    18: (30.7, 36.9), 19: (44.0, 15.0), 20: (-77.0, 38.9), 21: (-77.0, 38.9),
    22: (-99.0, 31.0), 23: (-118.2, 34.0), 24: (-92.0, 38.0),
    25: (-123.1, 49.3), 26: (125.8, 39.0), 27: (127.3, 36.5),
    28: (121.6, 25.0), 29: (100.5, 13.8), 30: (77.2, 28.6), 31: (88.0, 22.0),
    32: (96.0, 21.0), 33: (57.5, -20.2), 34: (145.0, -37.8), 35: (21.0, 52.2),
    36: (6.3, 4.8), 38: (42.8, 14.8), 39: (77.2, 28.6), 40: (6.1, 46.2),
    41: (151.2, -33.9), 42: (124.0, 11.0),
}


# --- layout -----------------------------------------------------------------
def region_counts():
    counts = {code: 0 for _, code in REGION_NAMES}
    for _, region, *_ in HEROES + TILES + LIST_ITEMS:
        counts[region] += 1
    return counts


def draw_region_strip(d, y):
    counts = region_counts()
    total = sum(counts.values())
    assert total == 42, "region counts must sum to 42, got %d" % total
    parts = []
    for name, code in REGION_NAMES:
        parts.append((name + " ", INK, font(SANS_B, 12)))
        parts.append((str(counts[code]) + "   ", BRICK, font(SANS_B, 13)))
    parts.append(("= 42 STORIES", INK, font(SANS_B, 12)))
    total_w = sum(d.textlength(t, font=f) for t, _, f in parts)
    x = (W - total_w) / 2
    for text, fill, fnt in parts:
        d.text((x, y), text, font=fnt, fill=fill)
        x += d.textlength(text, font=fnt)


def draw_big_numbers(d, y):
    x0, gap = 14, 6
    bw = (W - 2 * x0 - gap * 5) // 6
    bh = 52
    for i, (num, lab1, lab2) in enumerate(BIG_NUMBERS):
        x = x0 + i * (bw + gap)
        d.rectangle([x, y, x + bw, y + bh], outline=LINE, width=1,
                    fill=PAPER2)
        nf = font(SANS_B, 27)
        nf = fit_text(d, num, nf, bw - 12)
        d.text((x + bw / 2, y + 4), num, font=nf, fill=NAVY, anchor="mt")
        d.text((x + bw / 2, y + 33), lab1, font=font(SANS_B, 9), fill=BRICK,
               anchor="mt")
        d.text((x + bw / 2, y + 43), lab2, font=font(SANS, 9), fill=GREY,
               anchor="mt")


def draw_timeline(d, y):
    d.text((14, y), "THE DAY IN UTC", font=font(SANS_B, 12), fill=BRICK)
    d.line([14, y + 20, W - 14, y + 20], fill=NAVY, width=2)
    slot = (W - 28) / len(TIMELINE)
    for i, (when, place, what) in enumerate(TIMELINE):
        cx = 14 + slot * i + slot / 2
        d.ellipse([cx - 5, y + 15, cx + 5, y + 25], fill=BRICK,
                  outline=WHITE, width=1)
        d.text((cx, y + 28), when, font=font(SANS_B, 10), fill=NAVY,
               anchor="mt")
        d.text((cx, y + 41), place, font=font(SANS_B, 10), fill=INK,
               anchor="mt")
        wf = fit_text(d, what, font(SANS, 9), slot - 12)
        d.text((cx, y + 54), what, font=wf, fill=GREY, anchor="mt")


def draw_hero(d, idx, story, x, y, w, h):
    num, _reg, place, beat, head, body, src, status = story
    art_h = 46
    HERO_ART[idx](d, x, y, w, art_h)
    d.rectangle([x, y, x + w, y + art_h], outline=INK, width=1)
    yy = y + art_h + 6
    d.text((x, yy), "%d \u00b7 %s \u00b7 %s" % (num, place, beat),
           font=font(SANS_B, 10), fill=BRICK)
    yy += 15
    yy = draw_wrapped(d, x, yy, head, font(SERIF_B, 21), w, INK, spacing=1)
    yy += 3
    yy = draw_wrapped(d, x, yy, body, font(SANS, 11), w, (52, 52, 52),
                      spacing=1)
    yy += 4
    d.text((x, yy), src, font=font(SANS, 9), fill=GREY)
    bw = badge(d, x + w - 74, yy - 2, status, BADGE_FILL[status])
    d.rectangle([x, y + art_h, x + w, y + h], outline=LINE, width=1)


def draw_tile(d, story, x, y, w, h):
    num, _reg, place, beat, head, body, src, status = story
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=1, fill=WHITE)
    d.rectangle([x, y, x + w, y + 3], fill=BRICK)
    yy = y + 7
    d.text((x + 8, yy), "%d \u00b7 %s \u00b7 %s" % (num, place, beat),
           font=font(SANS_B, 9), fill=BRICK)
    yy += 13
    yy = draw_wrapped(d, x + 8, yy, head, font(SERIF_B, 14), w - 16, INK,
                      spacing=0)
    yy += 2
    yy = draw_wrapped(d, x + 8, yy, body, font(SANS, 10), w - 16,
                      (52, 52, 52), spacing=0)
    d.text((x + 8, y + h - 15), src, font=font(SANS, 8), fill=GREY)
    badge(d, x + w - 66, y + h - 17, status, BADGE_FILL[status])


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=1, fill=(232, 238, 242))
    lon0, lon1, lat0, lat1 = -168, 190, 78, -58

    def proj(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat0 - lat) / (lat0 - lat1) * h
        return px, py

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly],
                  fill=(190, 196, 178), outline=(120, 126, 110))
    for lon, lat in ISLANDS:
        px, py = proj(lon, lat)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(190, 196, 178))
    # grey dots for list stories 14-42 (skip 37 Mercury, no Earth place)
    for num in range(14, 43):
        if num not in MAP_POINTS:
            continue
        lon, lat = MAP_POINTS[num]
        px, py = proj(lon, lat)
        jx = ((num * 7) % 5 - 2)
        jy = ((num * 11) % 5 - 2)
        d.ellipse([px + jx - 2, py + jy - 2, px + jx + 2, py + jy + 2],
                  fill=GREY)
    # numbered red dots for hero + tile stories 1-10, 12, 13
    for num in range(1, 14):
        if num not in MAP_POINTS:
            continue
        lon, lat = MAP_POINTS[num]
        px, py = proj(lon, lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=BRICK,
                  outline=WHITE, width=1)
        d.text((px, py - 6), str(num), font=font(SANS_B, 9), fill=WHITE,
               anchor="mt")
    d.text((x + 6, y + h - 16), "Positions approximate \u00b7 11 = worldwide \u00b7 "
           "37 = Mercury", font=font(SANS, 8), fill=GREY)


def draw_list(d, x, y, w, h):
    d.text((x, y), "ALSO ON SATURDAY 21 NOVEMBER", font=font(SANS_B, 12),
           fill=BRICK)
    d.line([x, y + 17, x + w, y + 17], fill=NAVY, width=1)
    col_w = (w - 12) // 2
    rows = (len(LIST_ITEMS) + 1) // 2
    row_h = (h - 24) / rows
    for i, (num, _reg, text) in enumerate(LIST_ITEMS):
        col = i // rows
        row = i % rows
        lx = x + col * (col_w + 12)
        ly = y + 24 + row * row_h
        d.text((lx, ly), "%d" % num, font=font(SANS_B, 11), fill=BRICK)
        fnt = fit_text(d, text, font(SANS, 11), col_w - 24)
        d.text((lx + 22, ly), text, font=fnt, fill=INK)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # kicker
    d.text((W / 2, 8),
           "THE WORLD IN ONE DAY  \u00b7  42 STORIES  \u00b7  7 REGIONS  \u00b7  "
           "EVERY ONE DATED SATURDAY 21 NOVEMBER 2026",
           font=font(SANS_B, 12), fill=BRICK, anchor="mt")
    # masthead
    d.text((W / 2, 24), "Saturday 21 November 2026",
           font=font(SERIF_B, 40), fill=INK, anchor="mt")
    d.line([14, 70, W - 14, 70], fill=INK, width=2)
    d.line([14, 73, W - 14, 73], fill=INK, width=1)
    # sub-headline
    d.text((W / 2, 78),
           "COP31 runs into overtime  \u00b7  Five missiles shot down over Saudi "
           "Arabia  \u00b7  Strong quake shakes Peru",
           font=font(SERIF, 13), fill=NAVY, anchor="mt")
    # region strip
    draw_region_strip(d, 96)
    # big numbers
    draw_big_numbers(d, 116)
    # timeline
    draw_timeline(d, 172)
    # heroes
    hy, hh = 250, 154
    for i, story in enumerate(HEROES):
        draw_hero(d, i, story, 14 + i * 338, hy, 320, hh)
    # tiles 4-13: two rows of five
    tw, th, tg = 192, 88, 8
    for i, story in enumerate(TILES):
        row, col = divmod(i, 5)
        tx = 14 + col * (tw + tg)
        ty = 412 + row * (th + tg)
        draw_tile(d, story, tx, ty, tw, th)
    # map + list
    my = 604
    d.text((14, my), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=BRICK)
    d.line([14, my + 17, 300, my + 17], fill=NAVY, width=1)
    draw_map(d, 14, my + 24, 286, 220)
    draw_list(d, 316, my, W - 14 - 316, 244)
    # date check box
    dy = 856
    d.rectangle([14, dy, W - 14, dy + 92], outline=BRICK, width=2,
                fill=(252, 238, 232))
    draw_wrapped(d, 24, dy + 7, DATE_CHECK, font(SANS, 10), W - 48,
                 (90, 30, 24), spacing=2)
    # footer
    d.text((W / 2, 956),
           "HOW WE CHECKED:  CONFIRMED = 2+ outlets  \u00b7  OFFICIAL = on the "
           "record  \u00b7  REPORTED = one outlet  \u00b7  CLAIM = one side\u2019s account",
           font=font(SANS_B, 10), fill=NAVY, anchor="mt")
    d.text((W / 2, 972),
           "Claims are attributed, not stated as fact  \u00b7  Pictures and map: "
           "original, drawn in code",
           font=font(SANS, 10), fill=GREY, anchor="mt")
    d.text((W / 2, 987),
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera, CNN, USGS, IGP, "
           "CoinGecko, ESA  \u00b7  21 November 2026",
           font=font(SANS, 10), fill=GREY, anchor="mt")
    return img


def main():
    total = len(HEROES) + len(TILES) + len(LIST_ITEMS)
    assert total == 42, "expected 42 stories, got %d" % total
    nums = [s[0] for s in HEROES + TILES] + [s[0] for s in LIST_ITEMS]
    assert nums == list(range(1, 43)), "story numbers must run 1-42"
    img = build()
    assert img.size == (1024, 1024)
    img.save(OUT, format="PNG")
    print("wrote %s %d bytes" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
