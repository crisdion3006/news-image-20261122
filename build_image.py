#!/usr/bin/env python3
"""Poster redesign for 22 Nov 2026 — full-bleed dark poster, NOT a newspaper.

Written from scratch for the redesign: no masthead banner, no white
2x2 cards, no 'also today' strip. One giant number hero, diagonal
missile trails, four full-width colour bands, ticker footer.
Run: python3 build_image.py  -> writes entry.png
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (8, 14, 30)
GOLD = (255, 176, 32)
ORANGE = (255, 94, 20)
RED = (230, 40, 50)
CREAM = (246, 240, 224)
MUTE = (178, 188, 205)

SB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
S = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def F(p, s):
    return ImageFont.truetype(p, s)


def wrap(d, text, f, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, color, max_w, lead):
    for ln in wrap(d, text, f, max_w):
        d.text((x, y), ln, font=f, fill=color)
        y += lead
    return y


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# date + title, small, top-left — no masthead bar
d.text((48, 36), "SUNDAY  •  22 NOVEMBER 2026", font=F(SB, 26), fill=GOLD)
d.text((48, 72), "THE WORLD IN ONE DAY", font=F(SB, 22), fill=MUTE)

# thin red rule under the date — no slash through the hero number
d.rectangle([48, 118, 976, 124], fill=RED)

# giant hero number
d.text((40, 140), "110", font=F(SB, 240), fill=GOLD)
d.text((530, 175), "MISSILES", font=F(SB, 64), fill=CREAM)
d.text((530, 252), "+400 DRONES", font=F(SB, 46), fill=ORANGE)

# missile trails: three dotted arcs under the number
for (x0, y0, x1, y1) in [(80, 440, 420, 410), (620, 440, 900, 405), (350, 450, 700, 420)]:
    mx, my = (x0 + x1) / 2, min(y0, y1) - 60
    prev = None
    for i in range(21):
        t = i / 20
        px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1
        py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1
        if prev:
            d.line([prev, (px, py)], fill=(255, 214, 130), width=4)
        prev = (px, py)
    d.ellipse([x1 - 7, y1 - 7, x1 + 7, y1 + 7], fill=GOLD)

# hero headline
d.text((48, 470), "RUSSIA'S BIGGEST", font=F(SERIFB, 64), fill=(255, 255, 255))
d.text((48, 540), "ATTACK YET", font=F(SERIFB, 64), fill=(255, 255, 255))
para(d, 48, 625,
     "Zelenskyy calls Putin a 'killer' as Trump calls him a friend — "
     "and Poland reports a Russian missile in its airspace.",
     F(S, 24), MUTE, 928, 31)

# four full-width colour bands, no white cards
bands = [
    ((255, 94, 20), "01  MEXICO", "EL CHAPO ISIDRO CAPTURED",
     "FBI most-wanted drug lord seized in a shoot-out; 11 killed."),
    ((0, 150, 130), "02  CLIMATE  •  COP31", "FOSSIL-FUEL FIGHT STALLS DEAL",
     "Talks run into overtime in Antalya as the draft drops coal, oil and gas."),
    ((110, 70, 180), "03  UNITED STATES", "FBI PROBES CRIME DATABASE HACK",
     "The bureau investigates an apparent breach of its crime database."),
    ((200, 30, 45), "04  MIDDLE EAST", "IRAN STRIKES BAHRAIN, HORMUZ",
     "IRGC claims attacks on US radars; tankers struck in the Strait."),
]
y = 700
for bg, kick, head, body in bands:
    d.rectangle([0, y, W, y + 68], fill=bg)
    d.text((48, y + 8), kick, font=F(SB, 20), fill=(255, 255, 255))
    d.text((48, y + 32), head, font=F(SB, 26), fill=(255, 255, 255))
    y += 68

# body text, right side of each band
y = 700
for bg, kick, head, body in bands:
    # body text right-aligned, two lines max, small
    bf = F(S, 17)
    lines = wrap(d, body, bf, 330)
    yy = y + 6
    for ln in lines:
        d.text((640, yy), ln, font=bf, fill=(255, 235, 210))
        yy += 20
    y += 68

# ticker footer
d.rectangle([0, 972, W, H], fill=(16, 26, 52))
d.text((48, 990), "ALSO: ICE RAIDS SEATTLE  •  HUANG QUITS NVIDIA  •  EVEREST CRASH  •  NIGERIA BOAT SINKS",
       font=F(SB, 15), fill=GOLD)

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)
