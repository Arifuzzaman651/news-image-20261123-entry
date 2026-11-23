"""Draw the 23 November 2026 world-news poster (1024x1024) from stories.json.

System python3 + PIL only. Deterministic: fixed layout, fixed fonts, no
timestamps, no randomness — the same input always draws the same bytes.
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (176, 42, 42)
BLUE = (31, 78, 121)
GREEN = (46, 107, 52)
GOLD = (150, 110, 12)
GREY = (110, 110, 105)
LIGHT = (233, 227, 212)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 122, 178),
              outline=(20, 60, 100), width=3)
    d.ellipse([cx - r * 0.55, cy - r * 0.6, cx + r * 0.1, cy - r * 0.05],
              fill=(72, 150, 84))
    d.ellipse([cx - r * 0.1, cy + r * 0.15, cx + r * 0.6, cy + r * 0.65],
              fill=(72, 150, 84))
    d.ellipse([cx + r * 0.35, cy - r * 0.45, cx + r * 0.7, cy - r * 0.15],
              fill=(72, 150, 84))
    # crack: a red zigzag across the globe
    pts = [(cx - r * 0.8, cy - r * 0.5), (cx - r * 0.3, cy - r * 0.1),
           (cx - r * 0.55, cy + r * 0.25), (cx, cy + r * 0.55),
           (cx + r * 0.45, cy + r * 0.8)]
    d.line(pts, fill=RED, width=6, joint="curve")


def draw_building(d, x, y, w, h):
    # two apartment blocks, one broken, smoke above — all scaled to (w, h)
    d.rectangle([x, y + h * 0.45, x + w * 0.45, y + h], fill=(70, 70, 78))
    d.rectangle([x + w * 0.55, y + h * 0.6, x + w, y + h], fill=(96, 96, 104))
    d.polygon([(x + w * 0.55, y + h * 0.6), (x + w * 0.72, y + h * 0.28),
               (x + w * 0.88, y + h * 0.6)], fill=(96, 96, 104))
    for bx in (x + w * 0.06, x + w * 0.22, x + w * 0.62, x + w * 0.78):
        for by in (y + h * 0.55, y + h * 0.72, y + h * 0.88):
            d.rectangle([bx, by, bx + 10, by + 9], fill=(240, 210, 90))
    for sx, sy, sr in ((x + w * 0.7, y + h * 0.12, 8),
                       (x + w * 0.84, y + h * 0.04, 6),
                       (x + w * 0.58, y + h * 0.08, 5)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 150, 148))


def draw_talks(d, x, y, w, h):
    # two speech bubbles facing each other, lightning between
    d.rounded_rectangle([x, y + 4, x + w * 0.38, y + h * 0.52], radius=10,
                        fill=BLUE)
    d.polygon([(x + w * 0.28, y + h * 0.5), (x + w * 0.34, y + h * 0.68),
               (x + w * 0.38, y + h * 0.5)], fill=BLUE)
    d.rounded_rectangle([x + w * 0.62, y + 4, x + w, y + h * 0.52], radius=10,
                        fill=RED)
    d.polygon([(x + w * 0.72, y + h * 0.5), (x + w * 0.66, y + h * 0.68),
               (x + w * 0.62, y + h * 0.5)], fill=RED)
    d.polygon([(x + w * 0.52, y + h * 0.2), (x + w * 0.44, y + h * 0.55),
               (x + w * 0.5, y + h * 0.55), (x + w * 0.46, y + h * 0.92),
               (x + w * 0.58, y + h * 0.5), (x + w * 0.52, y + h * 0.5)],
              fill=(240, 200, 40))


def draw_capitol(d, x, y, w, h):
    d.rectangle([x, y + h * 0.75, x + w, y + h], fill=(90, 90, 96))
    d.pieslice([x + w * 0.28, y + h * 0.1, x + w * 0.72, y + h * 0.85],
               180, 360, fill=(120, 120, 128))
    for i in range(5):
        cx = x + w * (0.18 + i * 0.16)
        d.rectangle([cx - 5, y + h * 0.55, cx + 5, y + h * 0.75],
                    fill=(200, 200, 205))
    d.rectangle([x + w * 0.48, y, x + w * 0.52, y + h * 0.12], fill=INK)
    d.polygon([(x + w * 0.52, y), (x + w * 0.72, y + 8), (x + w * 0.52, y + 16)],
              fill=RED)


def draw_factory(d, x, y, w, h):
    d.rectangle([x, y + 40, x + w * 0.7, y + h], fill=(120, 96, 70))
    d.rectangle([x + w * 0.7, y + 10, x + w * 0.82, y + h], fill=(96, 96, 104))
    for i in range(3):
        d.polygon([(x + i * w * 0.23, y + 40), (x + (i + 0.5) * w * 0.23, y + 18),
                   (x + (i + 1) * w * 0.23, y + 40)], fill=(150, 60, 50))
    d.polygon([(x + w * 0.42, y + 30), (x + w * 0.5, y - 8), (x + w * 0.58, y + 8),
               (x + w * 0.66, y - 14), (x + w * 0.62, y + 30)],
              fill=(240, 140, 30))
    d.ellipse([x + w * 0.86, y - 6, x + w * 0.98, y + 6], fill=(150, 150, 148))


def draw_planet(d, x, y, w, h):
    cx, cy, r = x + w * 0.45, y + h * 0.5, min(w, h) * 0.32
    d.ellipse([cx - r * 2.1, cy - r * 0.7, cx + r * 2.1, cy + r * 0.7],
              outline=(120, 120, 130), width=3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 158, 145),
              outline=(110, 100, 88), width=2)
    for dx, dy, dr in ((-0.4, -0.3, 0.16), (0.35, 0.2, 0.12), (0.1, -0.5, 0.1),
                       (-0.1, 0.45, 0.13)):
        d.ellipse([cx + dx * r - dr * r, cy + dy * r - dr * r,
                   cx + dx * r + dr * r, cy + dy * r + dr * r],
                  fill=(130, 120, 108))
    d.rectangle([cx + r * 1.5, cy - r * 0.55, cx + r * 1.75, cy - r * 0.3],
                fill=BLUE)
    for sx, sy in ((x + 6, y + 8), (x + w - 10, y + 4), (x + w * 0.8, y + h - 8)):
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)


ICONS = {"globe": draw_globe, "building": draw_building, "talks": draw_talks,
         "capitol": draw_capitol, "factory": draw_factory,
         "planet": draw_planet}


def tag_chip(d, x, y, text, color):
    f = font(SANS_B, 17)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + tw + 16, y + 26], radius=5, fill=color)
    d.text((x + 8, y + 4), text, font=f, fill=(255, 255, 255))


def story_block(d, box, story, tag_color, head_size=27, sum_size=20,
                 scene_h=0):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    d.rectangle([x0, y0, x1, y1], fill=None, outline=(200, 192, 172), width=1)
    tag_chip(d, x0 + 14, y0 + 12, story["tag"], tag_color)
    hf = font(SANS_B, head_size)
    lines = wrap(d, story["headline"], hf, x1 - x0 - 28)
    ty = y0 + 46
    for ln in lines[:2]:
        d.text((x0 + 14, ty), ln, font=hf, fill=INK)
        ty += head_size + 6
    sf = font(SANS, sum_size)
    slines = wrap(d, story["summary"], sf, x1 - x0 - 28)
    # only as many summary lines as fit above the scene strip
    max_lines = max(0, (y1 - scene_h - 10 - ty) // (sum_size + 5))
    for ln in slines[:max_lines]:
        d.text((x0 + 14, ty + 2), ln, font=sf, fill=(60, 60, 58))
        ty += sum_size + 5


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    stories = {s["id"]: s for s in data["stories"]}

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28  # margin

    # ---- masthead ----
    title = font(SERIF_B, 62)
    d.text((W / 2, 22), data["masthead"], font=title, fill=INK, anchor="ma")
    d.line([(m, 100), (W - m, 100)], fill=INK, width=3)
    date_f = font(SANS_B, 33)
    d.text((W / 2, 112), data["date"], font=date_f, fill=RED, anchor="ma")
    d.line([(m, 156), (W - m, 156)], fill=RED, width=3)

    # ---- lead story: COP31, full width, scene on the right ----
    s = stories["cop31"]
    y0, y1 = 172, 424
    d.rectangle([m, y0, W - m, y1], outline=INK, width=2)
    tag_chip(d, m + 16, y0 + 14, s["tag"], RED)
    hf = font(SANS_B, 42)
    lines = wrap(d, s["headline"], hf, W - m - 340 - 16)
    ty = y0 + 50
    for ln in lines[:2]:
        d.text((m + 16, ty), ln, font=hf, fill=INK)
        ty += 48
    sf = font(SANS, 23)
    slines = wrap(d, s["summary"], sf, W - m - 340 - 16)
    for ln in slines[:4]:
        d.text((m + 16, ty + 2), ln, font=sf, fill=(60, 60, 58))
        ty += 29
    draw_globe(d, W - m - 150, y0 + 118, 80)
    d.text((W - m - 150, y0 + 208), "NO DEAL", font=font(SANS_B, 24),
           fill=RED, anchor="ma")

    # ---- row 2: two stories ----
    row2 = [(stories["kyiv"], BLUE), (stories["trump-iran"], (120, 60, 120))]
    bw = (W - 2 * m - 16) // 2
    for i, (st, col) in enumerate(row2):
        x0 = m + i * (bw + 16)
        x1 = x0 + bw
        y0b, y1b = 440, 692
        story_block(d, (x0, y0b, x1, y1b), st, col, head_size=26, sum_size=19,
                    scene_h=70)
        # scene strip at the bottom of the block
        ICONS[st["icon"]](d, x0 + 30, y1b - 70, bw - 60, 62)

    # ---- row 3: three stories ----
    row3 = [(stories["us-house"], BLUE), (stories["indonesia"], (150, 60, 50)),
            (stories["mercury"], (60, 60, 80))]
    bw3 = (W - 2 * m - 32) // 3
    for i, (st, col) in enumerate(row3):
        x0 = m + i * (bw3 + 16)
        x1 = x0 + bw3
        y0b, y1b = 708, 996
        story_block(d, (x0, y0b, x1, y1b), st, col, head_size=25, sum_size=19,
                    scene_h=86)
        ICONS[st["icon"]](d, x0 + 24, y1b - 86, bw3 - 48, 74)

    img.save(os.path.join(HERE, "entry.png"), "PNG")


if __name__ == "__main__":
    main()
