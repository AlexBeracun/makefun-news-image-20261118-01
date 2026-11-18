#!/usr/bin/env python3
"""Render entry.png for make.fun news-image-20261118.

Build-time script only: it renders the newspaper front page with Pillow
from the system fonts and writes entry.png beside it. The graded entry is
main.py, which only copies entry.png to the output directory (stdlib only,
no network, deterministic). Run: python3 gen_image.py
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (20, 20, 20)
NAVY = (20, 33, 61)
NAVY2 = (27, 45, 82)
GOLD = (201, 162, 39)
RED = (185, 28, 28)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)
CARD = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_star(d, cx, cy, r, color):
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)


def burst(d, cx, cy, r, color1, color2):
    import math, random
    random.seed(7)
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        rr = r * random.uniform(0.75, 1.15)
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color1)
    draw_star(d, cx, cy, int(r * 0.55), color2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    f_title = font(SERIF, 56)
    t = "THE WORLD IN ONE PAGE"
    d.text(((W - d.textlength(t, font=f_title)) / 2, 14), t, font=f_title, fill=WHITE)
    f_date = font(SANS_B, 23)
    t2 = "WORLD NEWS  •  WEDNESDAY, 18 NOVEMBER 2026"
    d.text(((W - d.textlength(t2, font=f_date)) / 2, 80), t2, font=f_date, fill=GOLD)

    # ---- lead story: Gulf ----
    x0, y0, x1, y1 = 28, 134, 996, 316
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD, outline=(200, 190, 160), width=2)
    f_kick = font(SANS_B, 19)
    kick = "LEAD STORY  •  MIDDLE EAST"
    d.rectangle([x0 + 14, y0 + 14, x0 + 14 + d.textlength(kick, font=f_kick) + 20, y0 + 40], fill=RED)
    d.text((x0 + 24, y0 + 17), kick, font=f_kick, fill=WHITE)
    f_head = font(SERIF, 40)
    d.text((x0 + 16, y0 + 48), "Gulf flashpoint: US strikes Iran;", font=f_head, fill=INK)
    d.text((x0 + 16, y0 + 94), "Iran hits back", font=f_head, fill=INK)
    f_body = font(SANS, 21)
    body = ("US jets hit a Revolutionary Guard missile site on Qeshm "
            "Island. Iran fired drones at US sites in Bahrain and Kuwait.")
    lines = wrap(d, body, f_body, 680)
    assert len(lines) <= 2, lines
    yy = y0 + 144
    for ln in lines[:2]:
        d.text((x0 + 16, yy), ln, font=f_body, fill=(40, 40, 40))
        yy += 27
    # explosion icon, right side
    burst(d, 880, 225, 62, (245, 158, 11), (255, 255, 255))
    d.ellipse([838, 183, 922, 267], outline=(185, 28, 28), width=4)

    # ---- six story panels, 2 cols x 3 rows ----
    panels = [
        ("EUROPE  •  UKRAINE WAR", (185, 28, 28),
         "Crimea bridge hit again",
         "Ukraine hit the Kerch bridge a second day; part of its road span fell into the strait.", "bridge"),
        ("ASIA  •  DIPLOMACY", NAVY2,
         "Summit week in Shenzhen",
         "APEC opened in Shenzhen; Xi and Putin denounced sanctions. Trump joins Thursday.", "summit"),
        ("USA  •  POLITICS", (30, 90, 160),
         "Alaska flips the Senate",
         "Peltola won Alaska; Democrats take a 56-44 Senate majority, their largest since 2009.", "ballot"),
        ("AFRICA  •  HEALTH", (6, 120, 90),
         "Ebola surges in Congo",
         "Ebola passed 11,000 cases and 5,400 deaths; children are hit hardest.", "virus"),
        ("SPACE  •  SCIENCE", (90, 40, 120),
         "Voyager 1 makes history",
         "One light-day from Earth — 16 billion miles, the farthest any human object has flown.", "space"),
        ("USA  •  HEALTH", (150, 60, 0),
         "US measles-free status lost",
         "After 26 years, the US lost measles elimination status — 5,400 cases and 10 deaths in 2026.", "virus2"),
    ]
    px, py = 28, 330
    pw, ph, gap = 478, 150, 12
    f_pk = font(SANS_B, 16)
    f_ph = font(SERIF, 26)
    f_pb = font(SANS, 19)
    for i, (kick, col, head, body, icon) in enumerate(panels):
        cx = px + (i % 2) * (pw + gap)
        cy = py + (i // 2) * (ph + gap)
        d.rounded_rectangle([cx, cy, cx + pw, cy + ph], radius=10, fill=CARD,
                            outline=(200, 190, 160), width=2)
        d.rectangle([cx, cy, cx + pw, cy + 6], fill=col)
        d.text((cx + 14, cy + 14), kick, font=f_pk, fill=col)
        hl = wrap(d, head, f_ph, pw - 28)
        yy = cy + 40
        for ln in hl[:2]:
            d.text((cx + 14, yy), ln, font=f_ph, fill=INK)
            yy += 31
        bl = wrap(d, body, f_pb, pw - 28)
        assert len(bl) <= 2, (head, bl)
        for ln in bl[:2]:
            d.text((cx + 14, yy), ln, font=f_pb, fill=(40, 40, 40))
            yy += 24
        ix, iy = cx + pw - 40, cy + 30
        if icon == "bridge":
            d.line([ix - 30, iy + 14, ix - 10, iy - 2, ix + 12, iy - 2, ix + 32, iy + 14],
                   fill=NAVY, width=4)
            d.line([ix - 30, iy + 14, ix + 32, iy + 14], fill=NAVY, width=4)
            d.line([ix - 2, iy - 2, ix + 5, iy + 14], fill=RED, width=3)
        elif icon == "summit":
            for j, c in enumerate([(185, 28, 28), (30, 90, 160), (201, 162, 39)]):
                d.ellipse([ix - 28 + j * 24, iy - 6 + (0 if j == 1 else 8), ix - 6 + j * 24,
                           iy + 16 + (0 if j == 1 else 8)], fill=c)
        elif icon == "ballot":
            d.rectangle([ix - 28, iy - 4, ix + 26, iy + 26], outline=NAVY, width=4)
            d.line([ix - 20, iy + 10, ix - 6, iy + 22, ix + 22, iy - 12], fill=(6, 120, 90), width=5)
        elif icon == "virus":
            d.ellipse([ix - 22, iy - 4, ix + 22, iy + 40], fill=(185, 28, 28))
            for ang in range(0, 360, 45):
                import math
                a = math.radians(ang)
                d.line([ix + 17 * math.cos(a), iy + 18 + 17 * math.sin(a),
                        ix + 27 * math.cos(a), iy + 18 + 27 * math.sin(a)],
                       fill=(185, 28, 28), width=4)
            d.ellipse([ix - 7, iy + 11, ix + 7, iy + 25], fill=WHITE)
        elif icon == "virus2":
            d.ellipse([ix - 22, iy - 4, ix + 22, iy + 40], fill=(150, 60, 0))
            for ang in range(0, 360, 60):
                import math
                a = math.radians(ang)
                d.line([ix + 17 * math.cos(a), iy + 18 + 17 * math.sin(a),
                        ix + 27 * math.cos(a), iy + 18 + 27 * math.sin(a)],
                       fill=(150, 60, 0), width=4)
            d.text((ix - 8, iy + 6), "!", font=font(SANS_B, 26), fill=WHITE)
        elif icon == "space":
            draw_star(d, ix - 16, iy - 4, 8, GOLD)
            draw_star(d, ix + 20, iy + 12, 6, GOLD)
            d.polygon([(ix - 20, iy + 28), (ix - 6, iy - 2), (ix + 8, iy + 28)], fill=NAVY)
            d.polygon([(ix - 20, iy + 28), (ix - 28, iy + 38), (ix - 12, iy + 32)], fill=RED)
            d.polygon([(ix + 8, iy + 28), (ix + 16, iy + 38), (ix + 0, iy + 32)], fill=RED)

    # ---- also today strip ----
    ax0, ay0, ax1, ay1 = 28, 816, 996, 950
    d.rounded_rectangle([ax0, ay0, ax1, ay1], radius=10, fill=NAVY, outline=NAVY)
    f_ak = font(SANS_B, 19)
    d.text((ax0 + 16, ay0 + 12), "ALSO TODAY", font=f_ak, fill=GOLD)
    also = [
        ("GAZA", "Ceasefire monitor warns the truce could collapse."),
        ("SIBERIA", "Russian military plane crash kills 19."),
        ("PACIFIC", "Category 5 Cyclone Xavier hits the Cook Islands."),
    ]
    f_ab = font(SANS, 20)
    f_ah = font(SANS_B, 20)
    col_w = (ax1 - ax0 - 32) // 3
    for j, (h, b) in enumerate(also):
        xx = ax0 + 16 + j * col_w
        d.text((xx, ay0 + 42), h, font=f_ah, fill=WHITE)
        bl = wrap(d, b, f_ab, col_w - 16)
        yy = ay0 + 70
        for ln in bl[:2]:
            d.text((xx, yy), ln, font=f_ab, fill=(220, 220, 220))
            yy += 25

    # ---- footer ----
    f_f = font(SANS, 17)
    ft = "All events happened or were first reported on Wednesday, 18 November 2026  •  Compiled from wire reports"
    d.text(((W - d.textlength(ft, font=f_f)) / 2, 966), ft, font=f_f, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
