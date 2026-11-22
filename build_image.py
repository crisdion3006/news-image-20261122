#!/usr/bin/env python3
"""Render the 22 November 2026 front page as a single 1024x1024 PNG.

Everything here is drawn fresh for this entry: night sky, skyline,
explosion bursts, four story cards and an also-today strip.
Run: python3 build_image.py  -> writes entry.png next to this file.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

PAPER = (247, 242, 232)
INK = (20, 26, 38)
NAVY = (20, 36, 62)
NAVY2 = (34, 62, 102)
RED = (192, 57, 43)
GOLD = (232, 164, 52)
ORANGE = (240, 122, 32)
CREAM = (250, 246, 236)
GREY = (110, 112, 118)
LINE = (196, 190, 178)
CARD = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, color, max_w, leading):
    """Draw wrapped paragraph; returns y just below last line."""
    for ln in wrap(d, text, f, max_w):
        d.text((x, y), ln, font=f, fill=color)
        y += leading
    return y


def burst(d, cx, cy, r, color):
    """Spiky explosion star."""
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)


def skyline(d, x0, y_base, x1, color):
    """Jagged city silhouette across the hero bottom."""
    import random
    rnd = random.Random(22)
    pts = [(x0, y_base)]
    x = x0
    while x < x1:
        bw = rnd.randint(28, 70)
        bh = rnd.randint(30, 95)
        pts.append((x, y_base - bh))
        pts.append((x + bw, y_base - bh))
        if rnd.random() < 0.35:  # antenna
            pts.append((x + bw / 2 - 2, y_base - bh - 22))
            pts.append((x + bw / 2 + 2, y_base - bh - 22))
            pts.append((x + bw / 2 + 2, y_base - bh))
        pts.append((x + bw, y_base))
        x += bw
    pts.append((x1, y_base))
    d.polygon(pts, fill=color)


def arc_trail(d, x0, y0, x1, y1, color):
    """A missile arc: quadratic bezier sampled as dots + line."""
    mx, my = (x0 + x1) / 2, min(y0, y1) - 70
    prev = None
    for t_i in range(21):
        t = t_i / 20
        px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1
        py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1
        if prev:
            d.line([prev, (px, py)], fill=color, width=3)
        prev = (px, py)
    d.ellipse([x1 - 5, y1 - 5, x1 + 5, y1 + 5], fill=color)


def tag(d, x, y, text, bg, fg=(255, 255, 255)):
    f = font(SANS_B, 17)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + tw + 20, y + 30], radius=4, fill=bg)
    d.text((x + 10, y + 5), text, font=f, fill=fg)
    return tw + 20


def story_card(d, box, accent, kicker, head, body, glyph):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=10, fill=CARD, outline=LINE, width=1)
    d.rounded_rectangle([x0, y0, x1, y0 + 9], radius=4, fill=accent)
    d.rectangle([x0, y0 + 5, x1, y0 + 9], fill=accent)
    kx = x0 + 18
    ky = y0 + 20
    kf = font(SANS_B, 16)
    d.text((kx, ky), kicker, font=kf, fill=accent)
    # small glyph disc top-right
    gx, gy = x1 - 62, y0 + 18
    d.ellipse([gx, gy, gx + 44, gy + 44], fill=accent)
    glyph(d, gx + 22, gy + 22)
    hy = ky + 28
    hf = font(SERIF_B, 25)
    hy = para(d, kx, hy, head, hf, INK, x1 - x0 - 36, 30)
    bf = font(SANS, 17)
    para(d, kx, hy + 6, body, bf, (58, 62, 70), x1 - x0 - 36, 22)


def glyph_star(d, cx, cy):
    pts = []
    for i in range(10):
        ang = math.pi * i / 5 - math.pi / 2
        rr = 13 if i % 2 == 0 else 5.5
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 255, 255))


def glyph_leaf(d, cx, cy):
    d.ellipse([cx - 11, cy - 13, cx + 11, cy + 13], outline=(255, 255, 255), width=3)
    d.line([(cx, cy - 13), (cx, cy + 13)], fill=(255, 255, 255), width=3)
    d.line([(cx, cy), (cx + 9, cy - 6)], fill=(255, 255, 255), width=2)
    d.line([(cx, cy + 3), (cx - 9, cy - 3)], fill=(255, 255, 255), width=2)


def glyph_shield(d, cx, cy):
    d.polygon([(cx, cy - 13), (cx + 11, cy - 8), (cx + 11, cy + 4),
               (cx, cy + 14), (cx - 11, cy + 4), (cx - 11, cy - 8)],
              outline=(255, 255, 255), width=3)
    d.text((cx - 4, cy - 8), "!", font=font(SANS_B, 16), fill=(255, 255, 255))


def glyph_flame(d, cx, cy):
    d.polygon([(cx, cy - 14), (cx + 9, cy - 1), (cx + 6, cy + 11),
               (cx - 6, cy + 11), (cx - 9, cy - 1)], fill=(255, 255, 255))
    d.ellipse([cx - 4, cy + 1, cx + 4, cy + 9], fill=ORANGE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.text((W / 2, 16), "THE WORLD IN ONE DAY", font=font(SERIF_B, 56),
           fill=CREAM, anchor="ma")
    d.text((W / 2, 76), "SUNDAY, 22 NOVEMBER 2026",
           font=font(SANS_B, 21), fill=GOLD, anchor="ma")
    d.rectangle([0, 104, W, 110], fill=RED)

    # ---------- hero: night sky over a city under attack ----------
    hx0, hy0, hx1, hy1 = 36, 126, 988, 448
    for yy in range(hy0, hy1):
        t = (yy - hy0) / (hy1 - hy0)
        r = int(NAVY[0] + (NAVY2[0] - NAVY[0]) * t)
        g = int(NAVY[1] + (NAVY2[1] - NAVY[1]) * t)
        b = int(NAVY[2] + (NAVY2[2] - NAVY[2]) * t)
        d.line([(hx0, yy), (hx1, yy)], fill=(r, g, b))
    import random
    rnd = random.Random(7)
    for _ in range(70):
        sx = rnd.randint(hx0 + 6, hx1 - 6)
        sy = rnd.randint(hy0 + 6, hy1 - 120)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 225, 235))
    arc_trail(d, 120, 440, 420, 400, (255, 214, 130))
    arc_trail(d, 880, 440, 660, 395, (255, 214, 130))
    skyline(d, hx0, hy1, hx1, (12, 20, 36))
    burst(d, 420, 400, 42, ORANGE)
    burst(d, 420, 400, 24, GOLD)
    burst(d, 660, 395, 34, ORANGE)
    burst(d, 660, 395, 19, GOLD)
    burst(d, 820, 415, 22, (240, 90, 40))
    # smoke puffs above skyline
    for cx, cy, rr in [(300, 415, 26), (520, 420, 30), (760, 412, 24)]:
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(58, 66, 84))

    tag(d, hx0 + 22, hy0 + 20, "UKRAINE  •  WAR", RED)
    title_f = font(SERIF_B, 42)
    d.text((hx0 + 22, 195), "RUSSIA'S BIGGEST ATTACK YET",
           font=title_f, fill=(255, 255, 255))
    sub_f = font(SANS, 21)
    para(d, hx0 + 22, 252,
         "110 missiles and 400+ drones strike Ukraine. Zelenskyy calls Putin a "
         "'killer' as Trump calls him a friend — and Poland reports a Russian "
         "missile in its airspace.",
         sub_f, (214, 222, 235), hx1 - hx0 - 44, 26)

    # ---------- 2x2 story cards ----------
    cards = [
        ((36, 466, 502, 640), (146, 90, 32), "MEXICO",
         "EL CHAPO ISIDRO CAPTURED",
         "FBI most-wanted drug lord Fausto Isidro Meza Flores seized in a "
         "shoot-out; 11 killed.",
         glyph_star),
        ((522, 466, 988, 640), (46, 125, 72), "CLIMATE  •  COP31",
         "FOSSIL-FUEL FIGHT STALLS DEAL",
         "Climate talks run into overtime in Antalya as a pared-down draft "
         "drops coal, oil and gas.",
         glyph_leaf),
        ((36, 656, 502, 830), (90, 60, 120), "UNITED STATES",
         "FBI PROBES CRIME DATABASE HACK",
         "The bureau investigates an apparent breach of its National Crime "
         "Information Center database.",
         glyph_shield),
        ((522, 656, 988, 830), (168, 60, 40), "MIDDLE EAST",
         "IRAN STRIKES BAHRAIN, HORMUZ",
         "IRGC claims attacks on US radars; a site is hit and tankers are "
         "struck in the Strait of Hormuz.",
         glyph_flame),
    ]
    for box, accent, kicker, head, body, gl in cards:
        story_card(d, box, accent, kicker, head, body, gl)

    # ---------- also today strip ----------
    sy = 852
    d.text((36, sy), "ALSO TODAY", font=font(SANS_B, 19), fill=RED)
    d.line([(170, sy + 12), (988, sy + 12)], fill=LINE, width=2)
    minis = [
        ("ICE RAIDS SEATTLE JET BRIDGE",
         "Two held on an L.A. flight; governor denounces raid."),
        ("JENSEN HUANG QUITS NVIDIA",
         "Speculation swirls over the chip chief's next move."),
        ("EVEREST HELICOPTER CRASH",
         "Two helicopters collide; 1 dead, 2 injured."),
        ("BOAT SINKS IN NIGERIA",
         "24 mourners drown on their way to a funeral."),
    ]
    col_w = (988 - 36) / 4
    for i, (h, b) in enumerate(minis):
        x = 36 + i * col_w
        if i:
            d.line([(x - 10, sy + 34), (x - 10, sy + 108)], fill=LINE, width=1)
        para(d, x, sy + 34, h, font(SANS_B, 17), INK, col_w - 20, 21)
        para(d, x, sy + 80, b, font(SANS, 14), GREY, col_w - 20, 18)

    # ---------- footer ----------
    d.line([(36, 984), (988, 984)], fill=LINE, width=1)
    d.text((W / 2, 992), "ALL STORIES VERIFIED FROM REPORTS PUBLISHED 22 NOVEMBER 2026",
           font=font(SANS, 14), fill=GREY, anchor="ma")

    img.save(OUT, optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
