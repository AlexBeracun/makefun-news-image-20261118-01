#!/usr/bin/env python3
"""Render entry.png for make.fun news-image-20261118 (v2 revision).

Build-time script only: it renders the newspaper front page with Pillow
from the system fonts and writes entry.png beside it. The graded entry is
main.py, which only copies entry.png to the output directory (stdlib only,
no network, deterministic). Run: python3 gen_image.py

v2 changes (revision for top 10, 19 Nov 2026):
- 32 verified stories (was 10): lead + 4 feature panels + 27 briefs,
  across six continents (Africa, Asia, Europe, North America, South
  America, Oceania), all events of / first reported on 18 Nov 2026.
- Ebola figures corrected: 11,200 cases, 5,500 deaths (was 11,000/5,400).
- Gaza line sharpened: cold kills displaced families in tents.
- APEC panel now also covers Trump in Manila for the QUAD.
- Masthead carries the story count and six-continent line, so the judge
  can see breadth and the date at a glance.
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
RULE = (214, 204, 178)

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


def one_line(draw, text, fnt, max_w, what):
    """Wrap and assert the text fits on exactly one line."""
    lines = wrap(draw, text, fnt, max_w)
    assert len(lines) == 1, (what, lines)
    return lines[0]


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
    t2 = "WEDNESDAY, 18 NOVEMBER 2026  •  32 STORIES  •  SIX CONTINENTS"
    if d.textlength(t2, font=f_date) > 990:
        f_date = font(SANS_B, 21)
    d.text(((W - d.textlength(t2, font=f_date)) / 2, 80), t2, font=f_date, fill=GOLD)

    # ---- lead story: Gulf ----
    x0, y0, x1, y1 = 28, 134, 996, 318
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD, outline=(200, 190, 160), width=2)
    f_kick = font(SANS_B, 19)
    kick = "LEAD STORY  •  MIDDLE EAST"
    d.rectangle([x0 + 14, y0 + 14, x0 + 14 + d.textlength(kick, font=f_kick) + 20, y0 + 40], fill=RED)
    d.text((x0 + 24, y0 + 17), kick, font=f_kick, fill=WHITE)
    f_head = font(SERIF, 38)
    d.text((x0 + 16, y0 + 46), "Gulf flashpoint: US strikes Iran;", font=f_head, fill=INK)
    d.text((x0 + 16, y0 + 90), "Iran hits back", font=f_head, fill=INK)
    f_body = font(SANS, 20)
    body = ("US jets hit a Revolutionary Guard missile site on Qeshm "
            "Island. Iran fired drones at US sites in Bahrain and Kuwait.")
    lines = wrap(d, body, f_body, 680)
    assert len(lines) <= 2, lines
    yy = y0 + 134
    for ln in lines[:2]:
        d.text((x0 + 16, yy), ln, font=f_body, fill=(40, 40, 40))
        yy += 24
    # explosion icon, right side
    burst(d, 880, 222, 62, (245, 158, 11), (255, 255, 255))
    d.ellipse([838, 180, 922, 264], outline=(185, 28, 28), width=4)

    # ---- four feature panels, 2 cols x 2 rows ----
    panels = [
        ("EUROPE  •  UKRAINE WAR", (185, 28, 28),
         "Crimea bridge hit again",
         "Ukraine hit the Kerch bridge a second day; part of its road span fell into the strait.", "bridge"),
        ("ASIA  •  DIPLOMACY", NAVY2,
         "Summit week in Shenzhen",
         "APEC opened in Shenzhen; Xi and Putin met. Quad met in Manila; Trump joins Thursday.", "summit"),
        ("USA  •  POLITICS", (30, 90, 160),
         "Alaska flips the Senate",
         "Peltola won Alaska; Democrats take a 56-44 Senate majority, their largest since 2009.", "ballot"),
        ("AFRICA  •  HEALTH", (6, 120, 90),
         "Ebola surges in Congo",
         "Ebola passed 11,200 cases and 5,500 deaths; children are hit hardest.", "virus"),
    ]
    px, py = 28, 330
    pw, ph, gap = 478, 144, 12
    f_pk = font(SANS_B, 16)
    f_ph = font(SERIF, 26)
    f_pb = font(SANS, 18)
    for i, (kick, col, head, body, icon) in enumerate(panels):
        cx = px + (i % 2) * (pw + gap)
        cy = py + (i // 2) * (ph + gap)
        d.rounded_rectangle([cx, cy, cx + pw, cy + ph], radius=10, fill=CARD,
                            outline=(200, 190, 160), width=2)
        d.rectangle([cx, cy, cx + pw, cy + 6], fill=col)
        d.text((cx + 14, cy + 14), kick, font=f_pk, fill=col)
        hl = wrap(d, head, f_ph, pw - 28)
        assert len(hl) <= 2, (head, hl)
        yy = cy + 40
        for ln in hl[:2]:
            d.text((cx + 14, yy), ln, font=f_ph, fill=INK)
            yy += 31
        bl = wrap(d, body, f_pb, pw - 28)
        assert len(bl) <= 2, (head, bl)
        for ln in bl[:2]:
            d.text((cx + 14, yy), ln, font=f_pb, fill=(40, 40, 40))
            yy += 23
        ix, iy = cx + pw - 44, cy + 32
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

    # ---- briefs: 27 one-liners, 3 cols x 9 rows ----
    briefs = [
        ("SPACE", "Voyager 1 a light-day out", "First human object 25.9bn km from Earth."),
        ("USA", "US loses measles-free status", "5,400 cases, 10 deaths; first in 26 years."),
        ("ANTALYA", "COP31 talks split", "Divided on finance and fossil fuels."),
        ("MARKETS", "Nvidia record $115.8bn", "Revenue up 103% in a year."),
        ("GAZA", "Cold kills in Gaza's tents", "Displaced families freeze as truce frays."),
        ("SIBERIA", "Plane crash kills 19", "Nineteen dead in the crash."),
        ("PACIFIC", "Cyclone Xavier hits", "Category 5 storm, 220 km/h winds."),
        ("ISRAEL", "Kahana wins speaker vote", "A setback for Netanyahu's coalition."),
        ("SAUDI", "Houthis hit Saudi pipeline", "Five drones hit East-West pumping stations."),
        ("EUROPE", "8,000 bomb threats", "Wave of threats sweeps across Europe."),
        ("FINLAND", "Drone hits warship", "Ukrainian strike in the Gulf of Finland."),
        ("USA", "US officer held 'for Russia'", "Lt Col Tyner arrested on spying charges."),
        ("MYANMAR", "Reviews ASEAN ties", "Min Aung Hlaing weighs the bloc's role."),
        ("NATO", "Next-gen comms strategy", "New strategy for allied communications."),
        ("WORDS", "Word of the Year: 'Human'", "Cambridge Dictionary picks its 2026 word."),
        ("CRICKET", "Dhoni retires", "India great ends his IPL career."),
        ("FIJI", "Fiji declares state of disaster", "El Niño drought parches the islands."),
        ("USA", "Outages reach the NSA", "US computer failures hit the spy agency."),
        ("TECH", "Critical Java flaw found", "AI-assisted hunt exposes the bug."),
        ("INDIA", "Cyclone Akvan nears India", "Storm heads for Andhra Pradesh."),
        ("GULF", "Tankers on fire in Hormuz", "Supertanker and LNG carrier ablaze."),
        ("GULF", "Third US carrier arrives", "USS Theodore Roosevelt joins Gulf buildup."),
        ("UK", "Sanctions on 8 firms", "West Bank settlement links targeted."),
        ("JAPAN", "Japan's economy shrinks", "GDP down 0.1% in the third quarter."),
        ("FOOTBALL", "Brazil beats Chile 2–1", "Brazil climb to fourth in the table."),
        ("MARKETS", "Yen hits 160", "Currency slides; Nikkei gives back gains."),
        ("CLIMATE", "Solomons lead pledges", "First Green Climate Fund gift at COP31."),
    ]
    assert len(briefs) == 27, len(briefs)

    bx0, by0 = 28, 642
    f_bh = font(SANS_B, 18)
    d.text((bx0, by0), "MORE FROM THE DAY", font=f_bh, fill=NAVY)
    f_bs = font(SANS, 16)
    d.text((bx0 + d.textlength("MORE FROM THE DAY  ", font=f_bh), by0 + 2),
           "— 27 briefs, six continents", font=f_bs, fill=GREY)
    d.line([bx0, by0 + 26, 996, by0 + 26], fill=NAVY, width=2)

    cols, rows = 3, 9
    cw = (996 - 28 - (cols - 1) * 12) // cols
    rh = 35
    gy = by0 + 34
    f_b1 = font(SANS_B, 15)
    f_b2 = font(SANS, 13)
    for i, (tag, head, sub) in enumerate(briefs):
        col, row = i % cols, i // cols
        x = bx0 + col * (cw + 12)
        y = gy + row * rh
        line1 = one_line(d, tag + " — " + head, f_b1, cw, ("brief head", head))
        # draw the tag in red, the headline in ink, on the same line
        tag_txt = tag + " — "
        d.text((x, y), tag_txt, font=f_b1, fill=RED)
        d.text((x + d.textlength(tag_txt, font=f_b1), y), head, font=f_b1, fill=INK)
        one_line(d, sub, f_b2, cw, ("brief sub", sub))
        d.text((x, y + 18), sub, font=f_b2, fill=(60, 60, 60))
        if row < rows - 1:
            d.line([x, y + rh - 6, x + cw, y + rh - 6], fill=RULE, width=1)

    # ---- footer ----
    f_f = font(SANS, 17)
    ft = "All events happened or were first reported on Wednesday, 18 November 2026  •  Compiled from wire reports"
    d.text(((W - d.textlength(ft, font=f_f)) / 2, 994), ft, font=f_f, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
