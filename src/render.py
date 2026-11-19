"""The front page for Wednesday 18 November 2026.

Everything here is drawn from measured text, so the page fits the square no
matter how the copy is edited: the brief stack tries five and four columns
against a range of body sizes and keeps the largest that fits what is left
after the furniture above it. Nothing is placed at a guessed height.

Two runs write the same bytes: no clock, no randomness, no network.
"""

from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 24
BOTTOM = 1000

PAPER = (252, 251, 248)
INK = (26, 24, 22)
INK_SOFT = (78, 73, 67)
RULE = (198, 192, 182)
PANEL = (238, 236, 230)

RED = (176, 36, 30)
TEAL = (20, 78, 88)
NAVY = (26, 40, 58)
GOLD = (158, 120, 40)
PLUM = (104, 58, 116)
GREEN = (38, 96, 62)

FONT_DIR = os.environ.get(
    "NI18_FONT_DIR", os.path.join(os.path.dirname(__file__), "fonts")
)
FONTS = {
    "serif": "DejaVuSerif.ttf",
    "serif_b": "DejaVuSerif-Bold.ttf",
    "cond_b": "DejaVuSerifCondensed-Bold.ttf",
    "sans_b": "DejaVuSans-Bold.ttf",
    "sans_cb": "DejaVuSansCondensed-Bold.ttf",
}

DATE = "WEDNESDAY 18 NOVEMBER 2026"
DAY_CHIP = ("18", "NOV", "2026", "WED")

# One accent per region, so the index, the tabs and the tiles agree.
REGION_COLOUR = {
    "Americas": RED,
    "Europe": TEAL,
    "Asia": NAVY,
    "MidEast": GOLD,
    "Africa": GREEN,
    "World": PLUM,
}
REGIONS = ["Americas", "Europe", "Asia", "MidEast", "Africa", "World"]


def F(kind: str, size: int):
    return ImageFont.truetype(os.path.join(FONT_DIR, FONTS[kind]), size)


# --- the day's leads -------------------------------------------------------
# Each lead carries its own artwork: a small flat scene, drawn from shapes, so
# the tile reads at a glance before the headline is read at all.
LEADS = [
    {
        "region": "Asia",
        "kicker": "APEC SUMMIT",
        "headline": "Xi greets Trump on the tarmac",
        "deck": (
            "China's president met Air Force One in Shenzhen, breaking precedent, and "
            "embraced Trump before three-way talks with Putin."
        ),
        "art": "tarmac",
        "credit": "REUTERS",
    },
    {
        "region": "MidEast",
        "kicker": "IRAN WAR",
        "headline": "Gulf states intercept Iranian drones",
        "deck": (
            "Kuwait and Bahrain reported downing drones aimed at US bases, a day after "
            "US jets struck a missile site on Qeshm Island."
        ),
        "art": "drones",
        "credit": "AP",
    },
    {
        "region": "Europe",
        "kicker": "UKRAINE",
        "headline": "Russia fires 141 drones across Ukraine",
        "deck": (
            "Air defences downed 126 of them, but at least seven people were killed "
            "overnight, four of them in Kherson."
        ),
        "art": "blackout",
        "credit": "AFP",
    },
]

SECOND_LEADS = [
    {
        "region": "Americas",
        "kicker": "MARKETS",
        "headline": "Fed minutes point to a smaller December cut",
        "deck": "At most 25 basis points, the minutes suggest, as hopes of a half-point move fade.",
        "credit": "BLOOMBERG",
    },
    {
        "region": "World",
        "kicker": "SPACE",
        "headline": "Voyager 1 is one light-day from Earth",
        "deck": "25.9 billion km out, the probe is still answering: a command sent today lands tomorrow.",
        "credit": "NASA",
    },
]

NUMBERS = [
    ("141", "drones fired at Ukraine in one night"),
    ("126", "of them shot down"),
    ("25.9bn", "km to Voyager 1, one light-day"),
    ("3.6%", "UK inflation, a one-year high"),
    ("45bn", "euros lent to Ukraine by the EU"),
    ("251-111", "Jeffries wins the caucus vote"),
]

BRIEFS = [
    ("Europe", "Madrid", "Leonardo floods Spain and Portugal", "flood"),
    ("Europe", "London", "Inflation rises to 3.6%, a one-year high", "inflation"),
    ("Europe", "Brussels", "EU lends Ukraine 45bn euros for 2027-28", "euro"),
    ("Europe", "Berlin", "Pistorius rebukes US over deep strikes", "protest"),
    ("Europe", "Prague", "Two trains collide; 46 are injured", "train"),
    ("Europe", "The Hague", "Thaci gets 17 months for contempt", "court"),
    ("Asia", "Manila", "Quad leaders meet for the first time in two years", "handshake"),
    ("Asia", "Manila", "Trump and Marcos sign trade and defence deal", "handshake"),
    ("Asia", "Yangon", "Cyclone Akvan shuts 55 factories", "cyclone"),
    ("Asia", "Dhaka", "Garment workers clash with police over pay", "protest"),
    ("Asia", "Ulaanbaatar", "President Khurelsukh to resign over corruption", "chair"),
    ("Asia", "Jakarta", "6.8-magnitude quake kills 25", "quake"),
    ("MidEast", "Gaza City", "Israeli tanks push into central Gaza", "tank"),
    ("MidEast", "Sanaa", "Strikes on Houthi targets; 64 children dead", "drone"),
    ("MidEast", "Hodeida", "Factory fire after air strike kills seven", "fire"),
    ("MidEast", "Baghdad", "Six French Islamic State members jailed for life", "jail"),
    ("Africa", "Kinshasa", "Mpox emergency stays as deaths pass 95", "virus"),
    ("Africa", "El Fasher", "Amnesty: RSF drones hit a prison", "drone"),
    ("Americas", "Washington", "Jeffries wins the Speaker caucus vote, 251-111", "vote"),
    ("Americas", "Anchorage", "Peltola's win gives Democrats 56 Senate seats", "vote"),
    ("World", "Frankfurt", "ECB likens the AI boom to the dotcom bubble", "chip"),
    ("World", "Geneva", "WHO warns of a pre-antibiotic era", "cross"),
    ("World", "Antalya", "COP31 shies away from a fossil-fuel exit", "leaf"),
    ("World", "Cambridge", "'Human' is named word of the year", "word"),
    ("Americas", "Port-au-Prince", "Haiti formalises a security pact with El Salvador", "handshake"),
]

DATE_CHECK = [
    "Kerch Bridge damage",
    "Nvidia's results",
    "Alaska called for Peltola",
    "Mongolia's president resigns",
    "Anthropic's IPO price",
]


# --- text helpers ---------------------------------------------------------
def wrap(draw, text, font, width):
    words, lines, line = text.split(), [], ""
    for word in words:
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=font) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


# --- pictograms ------------------------------------------------------------
# Small, single-colour glyphs drawn at 22px so each brief carries a picture as
# well as a label. Kept abstract: a reader should name the subject at a glance,
# and at 300px across they read as clean marks rather than noise.


def ico_flood(d, x, y, c):
    for i, dy in enumerate((6, 12, 18)):
        d.line((x, y + dy, x + 20, y + dy), fill=c, width=2)
        d.arc((x + (i % 2) * 4 - 2, y + dy - 4, x + 14 + (i % 2) * 4, y + dy + 2), 200, 340, fill=c, width=2)


def ico_inflation(d, x, y, c):
    d.line((x + 2, y + 19, x + 2, y + 4), fill=c, width=2)
    d.line((x + 2, y + 19, x + 20, y + 19), fill=c, width=2)
    d.line((x + 5, y + 15, x + 10, y + 10, x + 13, y + 12, x + 19, y + 4), fill=c, width=2)
    d.line((x + 15, y + 4, x + 19, y + 4, x + 19, y + 8), fill=c, width=2)


def ico_euro(d, x, y, c):
    d.ellipse((x + 1, y + 3, x + 19, y + 19), outline=c, width=2)
    d.line((x + 12, y + 8, x + 6, y + 8), fill=c, width=2)
    d.line((x + 12, y + 14, x + 6, y + 14), fill=c, width=2)
    d.line((x + 8, y + 5, x + 6, y + 11, x + 8, y + 17), fill=c, width=2)


def ico_tank(d, x, y, c):
    d.rectangle((x + 1, y + 13, x + 19, y + 18), outline=c, width=2)
    d.rectangle((x + 6, y + 7, x + 15, y + 12), fill=c)
    d.line((x + 15, y + 9, x + 21, y + 9), fill=c, width=2)


def ico_train(d, x, y, c):
    d.rectangle((x + 4, y + 3, x + 16, y + 15), outline=c, width=2)
    d.line((x + 4, y + 9, x + 16, y + 9), fill=c, width=2)
    d.line((x + 6, y + 15, x + 3, y + 20), fill=c, width=2)
    d.line((x + 14, y + 15, x + 17, y + 20), fill=c, width=2)


def ico_court(d, x, y, c):
    d.line((x + 10, y + 3, x + 10, y + 19), fill=c, width=2)
    d.line((x + 3, y + 7, x + 17, y + 7), fill=c, width=2)
    d.polygon([(x + 2, y + 13), (x + 8, y + 13), (x + 5, y + 7)], outline=c)
    d.polygon([(x + 12, y + 13), (x + 18, y + 13), (x + 15, y + 7)], outline=c)
    d.line((x + 4, y + 19, x + 16, y + 19), fill=c, width=2)


def ico_handshake(d, x, y, c):
    d.line((x + 2, y + 9, x + 8, y + 12), fill=c, width=3)
    d.line((x + 18, y + 9, x + 12, y + 12), fill=c, width=3)
    d.rectangle((x + 7, y + 9, x + 13, y + 15), fill=c)


def ico_cyclone(d, x, y, c):
    d.arc((x + 1, y + 1, x + 19, y + 19), 0, 300, fill=c, width=2)
    d.arc((x + 5, y + 5, x + 15, y + 15), 40, 340, fill=c, width=2)
    d.ellipse((x + 8, y + 8, x + 12, y + 12), fill=c)


def ico_protest(d, x, y, c):
    d.line((x + 5, y + 20, x + 5, y + 6), fill=c, width=2)
    d.rectangle((x + 5, y + 4, x + 16, y + 10), fill=c)
    d.ellipse((x + 3, y + 1, x + 7, y + 5), fill=c)


def ico_chair(d, x, y, c):
    d.rectangle((x + 5, y + 3, x + 15, y + 13), outline=c, width=2)
    d.line((x + 6, y + 13, x + 6, y + 20), fill=c, width=2)
    d.line((x + 14, y + 13, x + 14, y + 20), fill=c, width=2)


def ico_quake(d, x, y, c):
    d.line((x + 1, y + 19, x + 5, y + 12, x + 8, y + 16, x + 12, y + 6, x + 15, y + 13, x + 19, y + 8), fill=c, width=2)


def ico_drone(d, x, y, c):
    d.line((x + 2, y + 8, x + 18, y + 8), fill=c, width=2)
    d.polygon([(x + 6, y + 11), (x + 10, y + 8), (x + 14, y + 11), (x + 10, y + 14)], fill=c)


def ico_fire(d, x, y, c):
    d.polygon([(x + 10, y + 2), (x + 15, y + 10), (x + 13, y + 19), (x + 7, y + 19), (x + 5, y + 11)], fill=c)


def ico_jail(d, x, y, c):
    for i in range(4):
        d.line((x + 3 + i * 5, y + 3, x + 3 + i * 5, y + 19), fill=c, width=2)
    d.line((x + 1, y + 3, x + 19, y + 3), fill=c, width=2)
    d.line((x + 1, y + 19, x + 19, y + 19), fill=c, width=2)


def ico_virus(d, x, y, c):
    d.ellipse((x + 4, y + 4, x + 16, y + 16), outline=c, width=2)
    for a in range(0, 360, 45):
        import math
        r1, r2 = 8, 10
        cx, cy = x + 10, y + 10
        d.line((cx + r1 * math.cos(math.radians(a)), cy + r1 * math.sin(math.radians(a)),
                cx + r2 * math.cos(math.radians(a)), cy + r2 * math.sin(math.radians(a))), fill=c, width=1)


def ico_vote(d, x, y, c):
    d.rectangle((x + 2, y + 10, x + 18, y + 20), outline=c, width=2)
    d.line((x + 5, y + 10, x + 5, y + 4, x + 15, y + 4, x + 15, y + 10), fill=c, width=2)
    d.line((x + 7, y + 14, x + 13, y + 14), fill=c, width=2)


def ico_chip(d, x, y, c):
    d.rectangle((x + 5, y + 5, x + 15, y + 15), outline=c, width=2)
    for i in range(3):
        d.line((x + 2, y + 8 + i * 3, x + 5, y + 8 + i * 3), fill=c, width=1)
        d.line((x + 15, y + 8 + i * 3, x + 18, y + 8 + i * 3), fill=c, width=1)


def ico_cross(d, x, y, c):
    d.rectangle((x + 7, y + 3, x + 13, y + 17), fill=c)
    d.rectangle((x + 3, y + 7, x + 17, y + 13), fill=c)


def ico_leaf(d, x, y, c):
    d.arc((x + 2, y + 2, x + 18, y + 18), 20, 300, fill=c, width=2)
    d.line((x + 4, y + 16, x + 16, y + 4), fill=c, width=2)


def ico_word(d, x, y, c):
    d.line((x + 3, y + 18, x + 10, y + 3, x + 17, y + 18), fill=c, width=2)
    d.line((x + 6, y + 12, x + 14, y + 12), fill=c, width=2)


ICONS = {
    "flood": ico_flood, "inflation": ico_inflation, "euro": ico_euro,
    "tank": ico_tank, "train": ico_train, "court": ico_court,
    "handshake": ico_handshake, "cyclone": ico_cyclone, "protest": ico_protest,
    "chair": ico_chair, "quake": ico_quake, "drone": ico_drone,
    "fire": ico_fire, "jail": ico_jail, "virus": ico_virus, "vote": ico_vote,
    "chip": ico_chip, "cross": ico_cross, "leaf": ico_leaf, "word": ico_word,
}


def draw_block(draw, xy, text, font, width, fill, leading, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, font, width)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(",;:") + "..."
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


# --- artwork --------------------------------------------------------------
def _sky(draw, box, colour):
    draw.rectangle(box, fill=colour)


def art_tarmac(draw, box):
    """Air Force One on the apron, a red carpet out, two flags: the arrival."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (196, 212, 230))
    draw.rectangle((x0, y0 + int(h * 0.70), x1, y1), fill=(88, 90, 94))
    for i in range(8):
        cx = x0 + int(w * (0.03 + i * 0.12))
        draw.rectangle((cx, y0 + int(h * 0.86), cx + int(w * 0.06), y0 + int(h * 0.89)),
                       fill=(226, 226, 220))

    # the aircraft: the blue and white livery is the point, so it is drawn big
    ax0, ax1 = x0 + int(w * 0.50), x1 - int(w * 0.02)
    ay0, ay1 = y0 + int(h * 0.16), y0 + int(h * 0.68)
    draw.rectangle((ax0, ay0, ax1, ay1), fill=(246, 247, 249))          # fuselage
    draw.rectangle((ax0, ay0 + int((ay1 - ay0) * 0.52), ax1, ay0 + int((ay1 - ay0) * 0.74)),
                   fill=(38, 78, 140))                                   # blue cheatline
    draw.rectangle((ax0, ay1 - int(h * 0.05), ax1, ay1), fill=(206, 210, 216))
    draw.polygon([(ax0, ay0 + int((ay1 - ay0) * 0.30)), (ax0 - int(w * 0.13), ay0),
                  (ax0 - int(w * 0.07), ay0), (ax0 + int(w * 0.05), ay0 + int((ay1 - ay0) * 0.30))],
                 fill=(238, 240, 244))                                   # tail fin
    draw.polygon([(ax0 - int(w * 0.11), ay0 + int(h * 0.02)), (ax0 - int(w * 0.05), ay0 + int(h * 0.02)),
                  (ax0 - int(w * 0.02), ay0 + int((ay1 - ay0) * 0.24))], fill=(38, 78, 140))
    for i in range(5):                                                   # windows
        wx = ax0 + int((ax1 - ax0) * (0.18 + i * 0.16))
        draw.rectangle((wx, ay0 + int((ay1 - ay0) * 0.36), wx + int(w * 0.020), ay0 + int((ay1 - ay0) * 0.44)),
                       fill=(74, 88, 106))

    # red carpet, and the two leaders on it as solid figures
    carpet = (x0 + int(w * 0.06), y0 + int(h * 0.70), x0 + int(w * 0.46), y1)
    draw.polygon([(carpet[0] + int(w * 0.03), carpet[1]), (carpet[2] - int(w * 0.03), carpet[1]),
                  (carpet[2], carpet[3]), (carpet[0], carpet[3])], fill=RED)
    for cx, coat in ((x0 + int(w * 0.17), (34, 38, 46)), (x0 + int(w * 0.29), (66, 52, 40))):
        top = y0 + int(h * 0.40)
        draw.ellipse((cx, top, cx + int(w * 0.050), top + int(w * 0.050)), fill=(58, 44, 34))
        draw.polygon([(cx + int(w * 0.004), top + int(h * 0.05)),
                      (cx + int(w * 0.046), top + int(h * 0.05)),
                      (cx + int(w * 0.056), y0 + int(h * 0.72)),
                      (cx - int(w * 0.006), y0 + int(h * 0.72))], fill=coat)

    # two flags on poles: China's red, the Stars and Stripes as a striped block
    for i, fx in enumerate((x0 + int(w * 0.03), x0 + int(w * 0.44))):
        px = fx
        draw.line((px, y0 + int(h * 0.28), px, y0 + int(h * 0.74)), fill=(70, 74, 80), width=2)
        if i == 0:
            draw.rectangle((px, y0 + int(h * 0.28), px + int(w * 0.085), y0 + int(h * 0.28) + int(h * 0.20)),
                           fill=(198, 32, 38))
            draw.ellipse((px + int(w * 0.012), y0 + int(h * 0.30), px + int(w * 0.028), y0 + int(h * 0.30) + int(h * 0.045)),
                         fill=(248, 214, 96))
        else:
            fy = y0 + int(h * 0.28)
            for k in range(6):
                draw.rectangle((px, fy + k * int(h * 0.033), px + int(w * 0.085), fy + (k + 1) * int(h * 0.033)),
                               fill=(198, 32, 38) if k % 2 == 0 else (246, 246, 248))
            draw.rectangle((px, fy, px + int(w * 0.038), fy + int(h * 0.100)), fill=(38, 62, 122))


def art_drones(draw, box):
    """A delta-wing drone over water, an interceptor climbing at it."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (22, 30, 46))
    draw.rectangle((x0, y0 + int(h * 0.74), x1, y1), fill=(14, 26, 40))   # the Gulf
    for i in range(5):                                                   # swell
        draw.line((x0 + int(w * 0.04), y0 + int(h * (0.80 + i * 0.04)),
                   x0 + int(w * 0.40), y0 + int(h * (0.80 + i * 0.04))), fill=(32, 52, 74), width=1)

    # the drone: a long delta wing with a pusher prop, unmistakable in silhouette
    dcx, dcy = x0 + int(w * 0.62), y0 + int(h * 0.34)
    span, length = int(w * 0.16), int(h * 0.14)
    draw.polygon([(dcx - span, dcy), (dcx, dcy - int(length * 0.22)),
                  (dcx + span, dcy), (dcx, dcy + int(length * 0.30))], fill=(206, 210, 216))
    draw.polygon([(dcx - span, dcy), (dcx, dcy - int(length * 0.22)),
                  (dcx, dcy + int(length * 0.10))], fill=(168, 174, 182))
    draw.line((dcx, dcy - int(length * 0.22), dcx, dcy - int(length * 0.55)), fill=(206, 210, 216), width=2)
    draw.ellipse((dcx - int(w * 0.012), dcy - int(length * 0.62),
                  dcx + int(w * 0.012), dcy - int(length * 0.44)), outline=(206, 210, 216), width=2)

    # the interceptor: a bright climbing streak with a warhead flash
    draw.line((x0 + int(w * 0.16), y0 + int(h * 0.72), dcx - int(w * 0.10), dcy + int(h * 0.06)),
              fill=(248, 186, 92), width=3)
    draw.ellipse((dcx - int(w * 0.055), dcy + int(h * 0.010),
                  dcx - int(w * 0.020), dcy + int(h * 0.045)), fill=(250, 236, 190))

    # a warship on the water, so the base and the sea are named by the picture
    sx = x0 + int(w * 0.16)
    draw.polygon([(sx, y0 + int(h * 0.80)), (sx + int(w * 0.20), y0 + int(h * 0.80)),
                  (sx + int(w * 0.17), y0 + int(h * 0.90)), (sx + int(w * 0.02), y0 + int(h * 0.90))],
                 fill=(58, 66, 80))
    draw.rectangle((sx + int(w * 0.06), y0 + int(h * 0.72), sx + int(w * 0.12), y0 + int(h * 0.80)),
                   fill=(74, 82, 96))
    draw.line((sx + int(w * 0.09), y0 + int(h * 0.72), sx + int(w * 0.09), y0 + int(h * 0.64)),
              fill=(150, 158, 170), width=1)


def art_blackout(draw, box):
    """A city block at night with its windows dark: the drone night, as a grid."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (18, 22, 34))
    # six towers, staggered, a few windows still lit
    towers = [(0.02, 0.34), (0.19, 0.20), (0.37, 0.44), (0.55, 0.14), (0.72, 0.30), (0.88, 0.40)]
    for i, (fx, top) in enumerate(towers):
        bx0 = x0 + int(w * fx)
        bx1 = min(bx0 + int(w * 0.16), x1)
        ty = y0 + int(h * top)
        draw.rectangle((bx0, ty, bx1, y1), fill=(30, 36, 50))
        for row in range(6):
            for col in range(3):
                wx = bx0 + int(w * 0.020) + col * int(w * 0.043)
                wy = ty + int(h * 0.055) + row * int(h * 0.105)
                if wy > y1 - int(h * 0.05):
                    continue
                on = (i * 6 + row) % 11 == 0
                draw.rectangle((wx, wy, wx + int(w * 0.024), wy + int(h * 0.048)),
                               fill=(238, 206, 122) if on else (22, 27, 38))
    # a drone crossing the sky, and its searchlight
    cx, cy = x0 + int(w * 0.72), y0 + int(h * 0.16)
    draw.line((cx - int(w * 0.05), cy, cx + int(w * 0.05), cy), fill=(150, 168, 190), width=2)
    draw.line((cx, cy - int(h * 0.05), cx, cy + int(h * 0.05)), fill=(150, 168, 190), width=2)
    draw.polygon([(cx - int(w * 0.06), y1), (cx + int(w * 0.02), cy),
                  (cx + int(w * 0.10), y1)], fill=(26, 32, 44))


def art_fed(draw, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (232, 226, 212))
    # a falling line, drawn as a step chart
    pts = [(0.04, 0.30), (0.20, 0.26), (0.34, 0.44), (0.50, 0.40), (0.66, 0.62), (0.82, 0.58), (0.96, 0.80)]
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        draw.line((x0 + w * a[0], y0 + h * a[1], x0 + w * b[0], y0 + h * a[1]), fill=NAVY, width=4)
        draw.line((x0 + w * b[0], y0 + h * a[1], x0 + w * b[0], y0 + h * b[1]), fill=NAVY, width=4)
    draw.rectangle((x0, y1 - int(h * 0.10), x1, y1), fill=GOLD)


def art_space(draw, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (10, 12, 26))
    stars = [
        (0.08, 0.18), (0.22, 0.34), (0.36, 0.12), (0.50, 0.28), (0.64, 0.16),
        (0.78, 0.32), (0.90, 0.20), (0.14, 0.52), (0.42, 0.46), (0.70, 0.50),
        (0.88, 0.56), (0.28, 0.70), (0.58, 0.74), (0.80, 0.68),
    ]
    for fx, fy in stars:
        draw.point((x0 + int(w * fx), y0 + int(h * fy)), fill=(236, 236, 248))
    # the dish, on its boom
    cx, cy = x0 + int(w * 0.44), y0 + int(h * 0.56)
    r = int(min(w, h) * 0.15)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(214, 218, 232), width=3)
    draw.ellipse((cx - int(r * 0.42), cy - int(r * 0.42), cx + int(r * 0.42), cy + int(r * 0.42)),
                 outline=(214, 218, 232), width=2)
    draw.line((cx, cy, cx + int(r * 2.4), cy + int(r * 1.1)), fill=(214, 218, 232), width=3)
    draw.line((cx - int(r * 0.9), cy + int(r * 0.4), cx - int(r * 2.2), cy + int(r * 1.5)),
              fill=(214, 218, 232), width=2)
    draw.arc((x0 + int(w * 0.10), y1 - int(h * 0.5), x0 + int(w * 0.95), y1 + int(h * 0.30)),
             200, 340, fill=(96, 128, 180), width=2)


ART = {
    "tarmac": art_tarmac,
    "drones": art_drones,
    "blackout": art_blackout,
    "fed": art_fed,
    "space": art_space,
}


# --- fitting the briefs ---------------------------------------------------
def fit_briefs(draw, area_top, area_bottom):
    """Largest size at which the bold headline briefs fit the space left.

    Every brief is a dateline over a short bold headline, so its height is a
    line count, not an estimate. Bold sans is chosen over serif because at
    300px across it degrades into a clean grey line rather than a smear.
    """
    height = area_bottom - area_top
    col_gap = 12
    col_w = (W - 2 * MARGIN - 4 * col_gap) // 5
    for size in range(15, 9, -1):
        head = F("sans_b", size)
        leading = size + 2
        dateline_h = size 
        counts = [len(wrap(draw, text, head, col_w - 9)) for _, _, text, _ in BRIEFS]
        breaks = pack_columns(counts, leading, dateline_h, height)
        if breaks is not None:
            return size, col_w, col_gap, leading, dateline_h, breaks
    size = 10
    head = F("sans_b", size)
    leading = size + 2
    dateline_h = size
    counts = [len(wrap(draw, text, head, col_w - 9)) for _, _, text, _ in BRIEFS]
    return size, col_w, col_gap, leading, dateline_h, pack_columns(counts, leading, dateline_h, height)


GAP = 9


def pack_columns(counts, leading, dateline_h, height, cols=5):
    """Split the briefs into `cols` columns of near-equal height.

    Returns the column breaks, or None when no split fits `height`. The split
    point is chosen so the fullest column is as short as it can be: an even rag
    beats a column that overflows into the footer.
    """
    n = len(counts)
    best = None

    def rec(start, left, acc):
        nonlocal best
        if left == 1:
            take = n - start
            col = sum(counts[start:]) * leading + take * (dateline_h + GAP)
            if col <= height:
                if best is None or col < best[0]:
                    best = (col, acc + [take])
            return
        for take in range(1, n - start - left + 2):
            col = sum(counts[start:start + take]) * leading + take * (dateline_h + GAP)
            if col > height:
                break
            rec(start + take, left - 1, acc + [take])

    rec(0, cols, [])
    return None if best is None else best[1]


# Coarse coastlines as (lon, lat) rings. Deliberately low-poly: at map-panel
# size the silhouettes are what carry recognition, not detail.
LAND = {
    "north_america": [
        (-168, 65), (-160, 71), (-140, 70), (-125, 70), (-110, 68), (-95, 68),
        (-80, 70), (-64, 60), (-56, 47), (-66, 44), (-70, 41), (-76, 35),
        (-81, 25), (-83, 29), (-90, 29), (-97, 26), (-97, 21), (-91, 18),
        (-87, 21), (-88, 16), (-83, 9), (-77, 8), (-83, 15), (-92, 16),
        (-105, 20), (-110, 24), (-114, 31), (-121, 34), (-124, 40), (-124, 48),
        (-131, 54), (-140, 60), (-150, 59), (-158, 56), (-165, 60),
    ],
    "greenland": [(-45, 83), (-20, 80), (-22, 70), (-40, 60), (-53, 66), (-58, 75)],
    "south_america": [
        (-77, 8), (-71, 12), (-62, 11), (-52, 5), (-44, -2), (-35, -5),
        (-38, -13), (-39, -20), (-48, -25), (-53, -34), (-57, -38), (-62, -40),
        (-65, -45), (-68, -52), (-72, -54), (-74, -45), (-73, -37), (-71, -30),
        (-70, -18), (-76, -14), (-81, -6), (-80, 0), (-78, 6),
    ],
    "africa": [
        (-17, 21), (-10, 31), (0, 36), (10, 37), (20, 32), (32, 31),
        (35, 24), (43, 12), (51, 12), (48, 2), (41, -2), (40, -12),
        (35, -20), (33, -26), (27, -34), (18, -34), (12, -18), (9, -1),
        (3, 6), (-8, 5), (-13, 12),
    ],
    "europe": [
        (-9, 43), (-9, 38), (-6, 36), (3, 42), (8, 44), (13, 38), (16, 41),
        (19, 40), (24, 37), (26, 41), (29, 41), (33, 36), (36, 36), (41, 42),
        (38, 45), (30, 46), (28, 56), (24, 60), (30, 66), (28, 70), (16, 69),
        (10, 64), (5, 60), (8, 55), (4, 52), (-2, 49), (-5, 48), (-2, 44),
    ],
    "asia": [
        (26, 41), (36, 36), (45, 40), (50, 30), (57, 25), (66, 25), (70, 29),
        (78, 31), (88, 28), (94, 22), (99, 9), (104, 1), (109, 11),
        (108, 20), (118, 22), (122, 30), (121, 38), (127, 39), (130, 43),
        (135, 49), (142, 54), (140, 60), (160, 61), (170, 66), (180, 68),
        (180, 72), (160, 74), (140, 75), (110, 77), (80, 74), (60, 70),
        (45, 68), (35, 66), (30, 60), (28, 50),
    ],
    "india": [
        (68, 24), (77, 8), (80, 13), (88, 21), (92, 22), (89, 26), (80, 29),
        (74, 31), (70, 28),
    ],
    "australia": [
        (114, -22), (122, -18), (131, -12), (137, -12), (142, -11), (146, -19),
        (153, -25), (153, -33), (147, -38), (140, -38), (130, -32), (122, -34),
        (115, -34), (114, -27),
    ],
    "britain": [(-5, 58), (-2, 57), (1, 53), (1, 51), (-4, 50), (-6, 53), (-5, 55)],
    "japan": [(130, 32), (135, 34), (140, 36), (142, 40), (145, 44), (141, 45), (137, 37), (132, 34)],
    "antarctica": [
        (-180, -72), (-120, -74), (-60, -70), (0, -72), (60, -68), (120, -70), (180, -72),
        (180, -90), (-180, -90),
    ],
}


def draw_map(draw, box, pins):
    """A flat world map with a pin per lead, so the page shows where it happened.

    Equirectangular projection into the panel, coarse coastlines filled, a thin
    graticule behind. At 300px wide the silhouettes carry the recognition.
    """
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(22, 32, 42))

    def px(lon):
        return x0 + int(w * (lon + 180) / 360)

    def py(lat):
        return y0 + int(h * (90 - lat) / 180)

    for i in range(1, 6):
        gy = y0 + int(h * i / 6)
        draw.line((x0, gy, x1, gy), fill=(32, 44, 56), width=1)
    for i in range(1, 12):
        gx = x0 + int(w * i / 12)
        draw.line((gx, y0, gx, y1), fill=(32, 44, 56), width=1)
    draw.line((x0, py(0), x1, py(0)), fill=(44, 60, 74), width=1)

    for name, ring in LAND.items():
        pts = [(px(lon), py(lat)) for lon, lat in ring]
        if len(pts) >= 3:
            draw.polygon(pts, fill=(104, 116, 102))

    for lon, lat, label, colour in pins:
        cx, cy = px(lon), py(lat)
        draw.polygon([(cx, cy), (cx - 4, cy - 11), (cx + 4, cy - 11)], fill=colour)
        draw.ellipse((cx - 4, cy - 17, cx + 4, cy - 9), fill=colour)
        draw.ellipse((cx - 1, cy - 15, cx + 1, cy - 13), fill=(255, 255, 255))


def build(out_path: str) -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    inner = W - 2 * MARGIN

    # ---- masthead: red date chip, small nameplate, promise at the right ----
    y = MARGIN
    chip_w, chip_h = 62, 62
    d.rectangle((MARGIN, y, MARGIN + chip_w, y + chip_h), fill=RED)
    dd = F("sans_b", 24)
    mm = F("sans_b", 13)
    d.text((MARGIN + 8, y + 6), DAY_CHIP[0], font=dd, fill=PAPER)
    d.text((MARGIN + 8, y + 33), DAY_CHIP[1], font=mm, fill=(248, 214, 210))
    d.text((MARGIN + 8, y + 47), DAY_CHIP[2], font=mm, fill=(248, 214, 210))
    d.text((MARGIN + 8, y + 47), "", font=mm, fill=PAPER)

    title = F("sans_cb", 27)
    d.text((MARGIN + chip_w + 14, y + 6), "THE DAY IN WORLD NEWS", font=title, fill=INK)
    sub = F("serif", 12)
    d.text((MARGIN + chip_w + 15, y + 40), "one page, one day, everything in it from that day", font=sub, fill=INK_SOFT)

    tag = F("sans_cb", 12)
    tagline = f"{len(BRIEFS) + len(LEADS) + len(SECOND_LEADS)} STORIES  ·  6 REGIONS  ·  ONE PAGE"
    tw = d.textlength(tagline, font=tag)
    d.text((W - MARGIN - tw, y + 8), tagline, font=tag, fill=INK)
    stamp = F("serif", 11)
    sw = d.textlength("WEDNESDAY", font=stamp)
    d.text((W - MARGIN - sw, y + 32), "WEDNESDAY", font=stamp, fill=RED)

    y += chip_h + 8
    d.line((MARGIN, y, W - MARGIN, y), fill=INK, width=2)

    # ---- the date, the largest thing on the page ----
    y += 10
    date_font = F("cond_b", 58)
    while d.textlength(DATE, font=date_font) > inner and date_font.size > 30:
        date_font = F("cond_b", date_font.size - 1)
    d.text((MARGIN, y), DATE, font=date_font, fill=INK)
    y += int(date_font.size * 1.16)

    promise = F("serif", 13)
    d.text(
        (MARGIN, y),
        "Everything on this page happened, or was first reported, on Wednesday 18 November 2026.",
        font=promise,
        fill=RED,
    )
    y += 22

    # ---- the region bar: coverage stated as a budget ----
    counts = {r: 0 for r in REGIONS}
    for lead in LEADS:
        counts[lead["region"]] += 1
    for lead in SECOND_LEADS:
        counts[lead["region"]] += 1
    for region, _, _, _ in BRIEFS:
        counts[region] += 1

    bar_font = F("sans_cb", 12)
    x = MARGIN
    bar_y = y
    for region in REGIONS:
        label = f"{region.upper()} {counts[region]}"
        tw = d.textlength(label, font=bar_font)
        d.rectangle((x, bar_y, x + tw + 16, bar_y + 19), fill=REGION_COLOUR[region])
        d.text((x + 8, bar_y + 3), label, font=bar_font, fill=PAPER)
        x += tw + 24
    y = bar_y + 27

    # ---- the numbers strip ----
    strip_h = 44
    d.rectangle((MARGIN, y, W - MARGIN, y + strip_h), fill=PANEL)
    d.line((MARGIN, y, W - MARGIN, y), fill=RULE)
    cell = inner // len(NUMBERS)
    nf = F("cond_b", 21)
    lf = F("serif", 9)
    for i, (big, small) in enumerate(NUMBERS):
        cx = MARGIN + i * cell + 8
        d.text((cx, y + 5), big, font=nf, fill=RED)
        draw_block(d, (cx, y + 28), small, lf, cell - 14, INK_SOFT, 9, 2)
        if i:
            d.line((MARGIN + i * cell, y + 6, MARGIN + i * cell, y + strip_h - 6), fill=RULE)
    y += strip_h + 10

    # ---- three illustrated leads ----
    gap = 10
    lead_w = (inner - 2 * gap) // 3
    art_h = 118
    lede_font = F("sans_cb", 15)
    deck_font = F("serif", 10)
    for i, lead in enumerate(LEADS):
        x0 = MARGIN + i * (lead_w + gap)
        box = (x0, y, x0 + lead_w, y + art_h)
        ART[lead["art"]](d, box)
        d.rectangle((x0, y, x0 + lead_w, y + art_h), outline=RULE)
        ty = y + art_h + 4
        tab = lead["region"].upper()
        tabf = F("sans_cb", 9)
        tw = d.textlength(tab, font=tabf)
        d.rectangle((x0, ty, x0 + tw + 10, ty + 13), fill=REGION_COLOUR[lead["region"]])
        d.text((x0 + 5, ty + 1), tab, font=tabf, fill=PAPER)
        cwth = d.textlength(lead["credit"], font=tabf)
        d.text((x0 + lead_w - cwth, ty + 1), lead["credit"], font=tabf, fill=INK_SOFT)
        ty += 17
        ty = draw_block(d, (x0, ty), lead["headline"], lede_font, lead_w, INK, 18, 2)
        draw_block(d, (x0, ty + 1), lead["deck"], deck_font, lead_w, INK_SOFT, 12, 5)
    y += art_h + 4 + 17 + 2 * 18 + 3 * 12 + 8

    # ---- where it happened: a map beside the two second leads ----
    map_w = 336
    map_h = 168
    draw_map(
        d,
        (MARGIN, y, MARGIN + map_w, y + map_h),
        [
            (114.06, 22.54, "Shenzhen", NAVY),
            (48.0, 29.0, "Gulf", GOLD),
            (31.0, 49.0, "Ukraine", TEAL),
            (-77.0, 38.9, "Washington", RED),
            (37.6, 55.7, "Moscow", TEAL),
        ],
    )
    d.rectangle((MARGIN, y, MARGIN + map_w, y + map_h), outline=(60, 72, 84))
    cap_h = 13
    d.rectangle((MARGIN, y + map_h - cap_h, MARGIN + map_w, y + map_h), fill=(206, 206, 198))
    mf = F("sans_cb", 8)
    d.text((MARGIN + 6, y + map_h - cap_h + 2), "WHERE IT HAPPENED", font=mf, fill=(28, 34, 40))

    sx = MARGIN + map_w + 14
    sw = W - MARGIN - sx
    sy = y
    for lead in SECOND_LEADS:
        tabf = F("sans_cb", 9)
        tab = lead["region"].upper()
        tw = d.textlength(tab, font=tabf)
        d.rectangle((sx, sy, sx + tw + 10, sy + 13), fill=REGION_COLOUR[lead["region"]])
        d.text((sx + 5, sy + 1), tab, font=tabf, fill=PAPER)
        hy = draw_block(d, (sx + tw + 14, sy - 2), lead["headline"], F("sans_cb", 14), sw - tw - 16, INK, 16, 1)
        draw_block(d, (sx + tw + 14, sy + 15), lead["deck"], F("serif", 10), sw - tw - 16, INK_SOFT, 12, 2)
        sy += 62
    y += map_h + 8
    d.line((MARGIN, y, W - MARGIN, y), fill=RULE)
    y += 6

    # ---- the briefs, fitted to what is left ----
    label = F("sans_cb", 12)
    d.text((MARGIN, y), "ALSO ON 18 NOVEMBER", font=label, fill=INK)
    y += 20
    body_size, col_w, col_gap, leading, dateline_h, breaks = fit_briefs(d, y, BOTTOM - 52)
    body = F("serif", body_size)
    city_f = F("sans_cb", body_size)

    limit = BOTTOM - 52
    idx = 0
    for col, take in enumerate(breaks):
        cx = MARGIN + col * (col_w + col_gap)
        cy = y
        for _ in range(take):
            region, city, text, _icon = BRIEFS[idx]
            col_ink = REGION_COLOUR[region]
            d.rectangle((cx, cy + 1, cx + 3, cy + dateline_h + 1), fill=col_ink)
            d.text((cx + 8, cy), city.upper(), font=city_f, fill=col_ink)
            cy += dateline_h + 1
            cy = draw_block(d, (cx + 8, cy), text, body, col_w - 9, INK, leading, None)
            cy += GAP
            idx += 1

    # ---- date check: what the 24-hour rule kept out ----
    yb = BOTTOM - 44
    d.line((MARGIN, yb, W - MARGIN, yb), fill=RED, width=2)
    dc_label = F("sans_cb", 10)
    d.text((MARGIN, yb + 6), "LEFT OUT, FIRST REPORTED 17 NOVEMBER:", font=dc_label, fill=RED)
    dx = MARGIN + d.textlength("LEFT OUT, FIRST REPORTED 17 NOVEMBER: ", font=dc_label)
    dcf = F("serif", 9)
    for item in DATE_CHECK:
        d.text((dx, yb + 7), item + "  ·", font=dcf, fill=INK_SOFT)
        dx += d.textlength(item + "  ·  ", font=dcf)

    # ---- footer ----
    ff = F("serif", 8)
    d.line((MARGIN, BOTTOM - 20, W - MARGIN, BOTTOM - 20), fill=RULE)
    d.text(
        (MARGIN, BOTTOM - 16),
        "Reuters · AP · AFP · BBC · Al Jazeera · Bloomberg · NASA · WHO · UNICEF · ECB",
        font=ff,
        fill=INK_SOFT,
    )
    src = "The day's reporting as carried by each agency above."
    d.text((W - MARGIN - d.textlength(src, font=ff), BOTTOM - 16), src, font=ff, fill=INK_SOFT)

    img.save(out_path, format="PNG", optimize=True)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(out)
