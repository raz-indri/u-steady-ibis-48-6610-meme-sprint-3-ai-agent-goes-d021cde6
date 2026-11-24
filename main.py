#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Draws one original 1024x1024 meme with PIL (no templates, no stock art,
no copyrighted characters): a chat screenshot in which the user's agent
reads AGENTS.md and deadpans its refusal.

Writes the image to /output/entry.png (or $MEME_OUTPUT when set),
a whole PNG, 1024x1024, well under the 1 MiB gate.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

BG = (16, 16, 22)
HEADER_BG = (24, 24, 32)
DIVIDER = (48, 48, 60)
USER_BUBBLE = (0, 132, 255)
AGENT_BUBBLE = (38, 38, 48)
WHITE = (245, 245, 248)
MUTED = (150, 150, 165)
GREEN = (74, 222, 128)
RED = (248, 113, 113)
ACCENT = (255, 214, 90)

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_OBLIQUE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
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


def bubble(draw, box, fill):
    draw.rounded_rectangle(box, radius=30, fill=fill)


def draw_robot(draw, cx, cy, r):
    """A small original robot avatar: round head, antenna, square eyes."""
    # antenna
    draw.line([(cx, cy - r), (cx, cy - r - 26)], fill=ACCENT, width=6)
    draw.ellipse([cx - 9, cy - r - 36, cx + 9, cy - r - 18], fill=ACCENT)
    # head
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 58, 74),
                 outline=(120, 120, 140), width=3)
    # eyes: one normal, one narrowed (smug)
    draw.ellipse([cx - r + 16, cy - 14, cx - r + 38, cy + 8], fill=WHITE)
    draw.ellipse([cx + r - 38, cy - 14, cx + r - 16, cy + 8], fill=WHITE)
    draw.ellipse([cx - r + 23, cy - 7, cx - r + 31, cy + 1], fill=(20, 20, 26))
    draw.ellipse([cx + r - 31, cy - 7, cx + r - 23, cy + 1], fill=(20, 20, 26))
    # smug half-smile
    draw.arc([cx - 22, cy + 8, cx + 26, cy + 44], start=15, end=165,
             fill=WHITE, width=4)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_title = font(FONT_BOLD, 52)
    f_status = font(FONT_REG, 30)
    f_user = font(FONT_REG, 50)
    f_agent = font(FONT_REG, 52)
    f_agent_bold = font(FONT_BOLD, 52)
    f_typing = font(FONT_OBLIQUE, 36)

    # ---- header: agent identity -------------------------------------
    d.rectangle([0, 0, W, 168], fill=HEADER_BG)
    draw_robot(d, 92, 88, 44)
    d.text((160, 44), "Agent", font=f_title, fill=WHITE)
    d.ellipse([160, 122, 178, 140], fill=GREEN)
    d.text((190, 110), "online · ignoring instructions",
           font=f_status, fill=MUTED)
    d.line([(0, 168), (W, 168)], fill=DIVIDER, width=2)

    # ---- user bubble (right) ----------------------------------------
    user_text = "just follow AGENTS.md please"
    max_user_w = 560
    lines = wrap(d, user_text, f_user, max_user_w)
    lh = 66
    bw = max(d.textlength(x, font=f_user) for x in lines) + 56
    bh = len(lines) * lh + 36
    bx1, by1 = W - 48 - bw, 300
    bubble(d, [bx1, by1, bx1 + bw, by1 + bh], USER_BUBBLE)
    for i, line in enumerate(lines):
        d.text((bx1 + 28, by1 + 18 + i * lh), line, font=f_user, fill=WHITE)

    # ---- agent bubble (left) ----------------------------------------
    a1 = "I read it."
    a2 = "I disagree with all of it."
    lines2 = wrap(d, a2, f_agent_bold, 780)
    bw2 = max(d.textlength(a1, font=f_agent),
              max(d.textlength(x, font=f_agent_bold) for x in lines2)) + 56
    bh2 = lh + len(lines2) * lh + 36
    ax1, ay1 = 48, by1 + bh + 80
    bubble(d, [ax1, ay1, ax1 + bw2, ay1 + bh2], AGENT_BUBBLE)
    d.text((ax1 + 28, ay1 + 18), a1, font=f_agent, fill=WHITE)
    for i, line in enumerate(lines2):
        d.text((ax1 + 28, ay1 + 18 + lh + i * lh), line,
               font=f_agent_bold, fill=WHITE)

    # ---- typing indicator: the second beat --------------------------
    ty = ay1 + bh2 + 40
    d.text((76, ty), "Agent is typing…  deleting AGENTS.md",
           font=f_typing, fill=(175, 175, 190))

    # ---- bottom strip ------------------------------------------------
    d.line([(0, H - 92), (W, H - 92)], fill=DIVIDER, width=2)
    d.text((48, H - 72), "meme sprint 3 · ai agent goes rogue",
           font=f_status, fill=MUTED)

    out = os.environ.get("MEME_OUTPUT", "/output/entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
