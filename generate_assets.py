#!/usr/bin/env python3
"""Generate PNG/WebP assets referenced by the static site (run before publish)."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
BG = "#CFAE87"
INK = "#2A1C12"
ACCENT = "#C4561F"

FRAME_W, FRAME_H = 405, 720
COLS, ROWS = 7, 7


def _hex(rgb: str) -> tuple[int, int, int]:
    rgb = rgb.lstrip("#")
    return tuple(int(rgb[i : i + 2], 16) for i in (0, 2, 4))


def draw_mark(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], sw: int) -> None:
    x0, y0, x1, y1 = box
    draw.arc((x0, y1 - (x1 - x0), x1, y1), 200, 340, fill=_hex(ACCENT), width=sw)
    cx, cy = x0 + int(0.78 * (x1 - x0)), y0 + int(0.22 * (y1 - y0))
    r = max(3, (x1 - x0) // 14)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=_hex(INK))


def icon_png(size: int, path: Path) -> None:
    img = Image.new("RGB", (size, size), _hex(BG))
    draw = ImageDraw.Draw(img)
    pad = size // 8
    draw.rounded_rectangle((pad, pad, size - pad, size - pad), radius=size // 5, fill=_hex(BG))
    draw_mark(draw, (pad * 2, pad * 2, size - pad * 2, size - pad * 2), max(2, size // 16))
    img.save(path, optimize=True)


def og_jpg(path: Path) -> None:
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), _hex(BG))
    draw = ImageDraw.Draw(img)
    draw_mark(draw, (w - 420, 80, w - 80, 520), 28)
    try:
        font = ImageFont.truetype("arial.ttf", 72)
        font_s = ImageFont.truetype("arial.ttf", 36)
    except OSError:
        font = ImageFont.load_default()
        font_s = font
    draw.text((80, 200), "PickForge", fill=_hex(INK), font=font)
    draw.text(
        (80, 300),
        "Editorial product guides · Affiliate disclosure",
        fill=_hex(INK),
        font=font_s,
    )
    img.save(path, "JPEG", quality=88, optimize=True)


def sprite_webp(path: Path) -> None:
    sheet_w, sheet_h = COLS * FRAME_W, ROWS * FRAME_H
    sheet = Image.new("RGB", (sheet_w, sheet_h), _hex(BG))
    for i in range(COLS * ROWS):
        c, r = i % COLS, i // COLS
        frame = Image.new("RGB", (FRAME_W, FRAME_H), _hex(BG))
        draw = ImageDraw.Draw(frame)
        t = i / max(1, COLS * ROWS - 1)
        ox = int(40 + 120 * t)
        draw_mark(draw, (ox, 80, FRAME_W - 40, FRAME_H - 40), 18)
        sheet.paste(frame, (c * FRAME_W, r * FRAME_H))
    sheet.save(path, "WEBP", quality=82, method=6)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    icon_png(32, ASSETS / "favicon-32.png")
    icon_png(192, ASSETS / "icon-192.png")
    icon_png(512, ASSETS / "icon-512.png")
    og_jpg(ASSETS / "og.jpg")
    sprite_webp(ASSETS / "sprite.webp")
    print("Wrote assets to", ASSETS)


if __name__ == "__main__":
    main()
