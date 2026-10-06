"""Make the site icons from Coco's face (the first frame of her idle strip).

Writes into assets/icons/:
  favicon.ico            16, 32 and 48 px, for browser tabs
  icon-32.png            the tab icon as a PNG
  apple-touch-icon.png   180 px, for iPhone/iPad home screens (no transparency)
  icon-192.png, icon-512.png       for the web app manifest
  icon-maskable-512.png  for Android, which crops icons to its own shape

The face sits on a cocoa tile so it reads on light and dark tab bars, and
is enlarged by whole pixels so the pixel art stays crisp.

Run from the repository root:  python3 tools/build_icons.py  (needs Pillow)
"""
from pathlib import Path

from PIL import Image, ImageDraw

SOURCE = Path('assets/cats/cream/idle.png')
FACE = (0, 19, 27, 38)            # Coco's head, ears to chin, in the first frame
OUT = Path('assets/icons')
TILE = (110, 86, 74, 255)         # --cocoa
EDGE = (79, 61, 53, 255)          # --cocoa-dark


def face():
    img = Image.open(SOURCE).convert('RGBA').crop(FACE)
    return img.crop(img.getchannel('A').getbbox())


def icon(size, fill=0.8, rounded=True):
    """`fill`: how much of the icon the face may take up."""
    head = face()
    k = max(1, int(size * fill / max(head.size)))
    head = head.resize((head.width * k, head.height * k), Image.NEAREST)
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(out)
    if rounded:
        r = max(2, size // 6)
        draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=r, fill=TILE, outline=EDGE, width=max(1, size // 32))
    else:
        draw.rectangle((0, 0, size, size), fill=TILE)
    out.alpha_composite(head, ((size - head.width) // 2, (size - head.height) // 2 + size // 32))
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    icon(32).save(OUT / 'icon-32.png', optimize=True)
    icon(64).save(OUT / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
    icon(180, fill=0.7, rounded=False).convert('RGB').save(OUT / 'apple-touch-icon.png', optimize=True)
    icon(192).save(OUT / 'icon-192.png', optimize=True)
    icon(512).save(OUT / 'icon-512.png', optimize=True)
    icon(512, fill=0.55, rounded=False).save(OUT / 'icon-maskable-512.png', optimize=True)   # safe zone is the middle 80%
    for f in sorted(OUT.iterdir()):
        print(f, f.stat().st_size, 'bytes')


if __name__ == '__main__':
    main()
