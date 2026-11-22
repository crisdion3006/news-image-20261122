#!/usr/bin/env python3
"""Poster infographic: world news of Sunday 22 November 2026.

Draws entry.png (1024x1024) with Pillow. The layout is a full-bleed
dark poster: a giant gold hero number, three missile-trail arcs, a
two-line serif headline, four full-width colour bands for the other
stories, and a gold ticker footer.

Everything is fixed coordinates and fixed text, so the output is
deterministic: run it twice and the PNG bytes are identical.
"""

import hashlib
import math
import os

from PIL import Image, ImageDraw, ImageFont

SIZE = (1024, 1024)

# ---- palette -------------------------------------------------------
PAGE = (10, 15, 30)        # near-black navy
GOLD = (245, 180, 20)      # hero number, ticker, date line
CREAM = (246, 242, 230)    # "MISSILES"
EMBER = (238, 108, 28)     # "+400 DRONES"
SLATE = (140, 150, 172)    # "THE WORLD IN ONE DAY"
DECK = (168, 176, 192)     # deck under the headline
RULE = (215, 38, 45)       # thin red rule under the dateline
TRAIL = (228, 196, 88)     # missile-trail arcs
WHITE = (255, 255, 255)
BODY = (246, 246, 246)     # body copy inside the bands

BANDS = [
    ((238, 102, 8), "01 MEXICO", "EL CHAPO ISIDRO CAPTURED",
     "FBI most-wanted drug lord seized in a shoot-out; 11 killed."),
    ((0, 148, 128), "02 CLIMATE \u2022 COP31", "FOSSIL-FUEL FIGHT STALLS DEAL",
     "Talks run into overtime in Antalya as the draft drops coal, oil and gas."),
    ((106, 68, 205), "03 UNITED STATES", "FBI PROBES CRIME DATABASE HACK",
     "The bureau investigates an apparent breach of its crime database."),
    ((204, 32, 56), "04 MIDDLE EAST", "IRAN STRIKES BAHRAIN, HORMUZ",
     "IRGC claims attacks on US radars; tankers struck in the Strait."),
]

FOOTER = ("ALSO: ICE RAIDS SEATTLE \u2022 HUANG QUITS NVIDIA \u2022 "
          "EVEREST CRASH \u2022 NIGERIA BOAT SINKS")

DECK_TEXT = ("Zelenskyy calls Putin a 'killer' as Trump calls him a friend "
             "\u2014 and Poland reports a Russian missile in its airspace.")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    """Load a DejaVu font at the requested size."""
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def split_lines(draw, text, font, max_width):
    """Greedy word wrap: returns lines that each fit max_width."""
    lines = []
    current = ""
    for word in text.split(" "):
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def quad_points(start, ctrl, end, steps=48):
    """Sample points along a quadratic Bezier curve."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * ctrl[0] + t ** 2 * end[0]
        y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * ctrl[1] + t ** 2 * end[1]
        pts.append((x, y))
    return pts


def trail(draw, start, ctrl, end):
    """One thin gold arc with a glowing dot at its far end."""
    pts = quad_points(start, ctrl, end)
    for a, b in zip(pts, pts[1:]):
        draw.line([a, b], fill=TRAIL, width=2)
    ex, ey = end
    draw.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=GOLD)


def band(draw, top, height, colour, kicker, headline, body):
    """One full-width colour band with left headline and right body."""
    draw.rectangle([0, top, SIZE[0], top + height], fill=colour)
    sans_b = lambda s: load("DejaVuSans-Bold.ttf", s)
    draw.text((48, top + 10), kicker, font=sans_b(18), fill=WHITE)
    draw.text((48, top + 32), headline, font=sans_b(26), fill=WHITE)
    body_font = load("DejaVuSans.ttf", 17)
    lines = split_lines(draw, body, body_font, 336)
    y = top + 10
    for line in lines[:2]:
        draw.text((640, y), line, font=body_font, fill=BODY)
        y += 22


def render_poster():
    img = Image.new("RGB", SIZE, PAGE)
    draw = ImageDraw.Draw(img)

    sans_b = lambda s: load("DejaVuSans-Bold.ttf", s)
    serif_b = lambda s: load("DejaVuSerif-Bold.ttf", s)

    # ---- dateline --------------------------------------------------
    draw.text((48, 40), "SUNDAY \u2022 22 NOVEMBER 2026",
              font=sans_b(30), fill=GOLD)
    draw.text((48, 78), "THE WORLD IN ONE DAY",
              font=sans_b(26), fill=SLATE)
    draw.rectangle([48, 118, 976, 123], fill=RULE)

    # ---- hero number ------------------------------------------------
    draw.text((48, 146), "110", font=sans_b(230), fill=GOLD)
    draw.text((560, 182), "MISSILES", font=sans_b(64), fill=CREAM)
    draw.text((560, 258), "+400 DRONES", font=sans_b(46), fill=EMBER)

    # ---- missile trails ---------------------------------------------
    trail(draw, (82, 462), (290, 392), (498, 418))
    trail(draw, (352, 470), (540, 398), (700, 424))
    trail(draw, (642, 466), (800, 396), (948, 414))

    # ---- headline + deck --------------------------------------------
    draw.text((48, 488), "RUSSIA'S BIGGEST", font=serif_b(72), fill=WHITE)
    draw.text((48, 562), "ATTACK YET", font=serif_b(72), fill=WHITE)
    deck_font = load("DejaVuSans.ttf", 23)
    y = 648
    for line in split_lines(draw, DECK_TEXT, deck_font, 928):
        draw.text((48, y), line, font=deck_font, fill=DECK)
        y += 28

    # ---- colour bands ------------------------------------------------
    top = 712
    for colour, kicker, headline, body in BANDS:
        band(draw, top, 70, colour, kicker, headline, body)
        top += 70

    # ---- footer ticker ------------------------------------------------
    draw.text((48, 1000), FOOTER, font=sans_b(17), fill=GOLD)

    return img


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render_poster().save(out, "PNG")
    with open(out, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    print("wrote %s  %d bytes  sha256=%s" % (out, os.path.getsize(out), digest))


if __name__ == "__main__":
    main()
