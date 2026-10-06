"""Cut the pieces of the cat UI sheet that the page uses into assets/ui/.

CSS can only frame things (border-image) or show icons from whole images,
not from a region of a sprite sheet, so each piece gets its own small PNG.
The cat-ear panel also has PLAY / SETTINGS / EXIT baked into its middle;
that is painted over with the panel colour so it can be stretched.

Run from the repository root after changing PIECES:

    python3 tools/build_ui.py

Needs Pillow (pip install pillow).
"""
from pathlib import Path

from PIL import Image, ImageDraw

SHEET = Path('source/ui/cat-ui.png')
OUT = Path('assets/ui')

# name -> (x, y, w, h) on the sheet
PIECES = {
    'panel': (358, 454, 85, 115),          # cream panel with cat ears
    'button': (70, 177, 52, 15),           # tan button, darker bottom edge
    'button-dark': (6, 241, 52, 15),       # dark brown button
    'tile': (1, 257, 14, 14),              # cream rounded square
    'tile-down': (17, 258, 14, 13),        # the same, pressed
    'tile-sand': (1, 273, 14, 14),         # darker sand square, for "on"
    'nameplate': (230, 198, 66, 19),       # cat head + name bar
    'icon-plus': (321, 273, 14, 14),
    'icon-minus': (353, 289, 14, 14),
    'paw': (327, 153, 35, 30),
    'fish': (470, 195, 20, 11),
    'sleeping-cat': (466, 811, 43, 32),
    'bubble': (215, 663, 32, 18),          # speech bubble, tail at the bottom right
}

# The panel's inside, below the ears and within the outline, in panel pixels.
PANEL_INSIDE = (8, 34, 77, 104)


def main():
    OUT.mkdir(exist_ok=True)
    sheet = Image.open(SHEET).convert('RGBA')
    for name, (x, y, w, h) in PIECES.items():
        piece = sheet.crop((x, y, x + w, y + h))
        if name == 'panel':
            fill = piece.getpixel((PANEL_INSIDE[0], PANEL_INSIDE[1]))
            ImageDraw.Draw(piece).rectangle(PANEL_INSIDE, fill=fill)
        piece.save(OUT / f'{name}.png', optimize=True)
        print(f'{name}.png  {w}x{h}')


if __name__ == '__main__':
    main()
