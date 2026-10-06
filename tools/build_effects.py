"""Turn the pixel-effect GIFs into PNG strips the page can use.

The GIFs in "Pixel effects/Guide/img" are previews on a solid black
background. For each effect listed in EFFECTS this writes
effects/<name>.png: every frame side by side, with the black made
transparent. The art never uses pure black, so nothing else is lost.

Run from the repository root after changing EFFECTS:

    python3 tools/build_effects.py

Needs Pillow (pip install pillow).
"""
from pathlib import Path

from PIL import Image, ImageChops, ImageSequence

SOURCE = Path('Pixel effects/Guide/img')
OUT = Path('effects')

# name in the page -> GIF it comes from
EFFECTS = {
    'hearts': 'directional_heart_burst_002_small_red.gif',
    'sparkle': 'round_sparkle_burst_001_small_blue.gif',
    'sleep': 'spell_sleep_001_small_blue.gif',
    'smoke': 'symmetrical_smoke_burst_003_small_white.gif',
    'alert': 'symbol_alert_001_small_red.gif',
    'scrap': 'symmetrical_impact_002_small_blue.gif',
    'pounce': 'toon_impact_001_small_yellow.gif',
    'music': 'round_music_burst_001_small_violet.gif',
    'party': 'directional_party_burst_001_small_red.gif',
    'death': 'stylized_skull_smoke_burst_001_small_white.gif',
}


def strip(gif_path):
    with Image.open(gif_path) as gif:
        frames = [frame.convert('RGBA') for frame in ImageSequence.Iterator(gif)]
    w, h = frames[0].size
    sheet = Image.new('RGBA', (w * len(frames), h))
    for i, frame in enumerate(frames):
        sheet.paste(frame, (i * w, 0))
    r, g, b, _ = sheet.split()
    brightest = ImageChops.lighter(ImageChops.lighter(r, g), b)
    sheet.putalpha(brightest.point(lambda v: 255 if v else 0))   # pure black -> transparent
    return sheet, len(frames)


def main():
    OUT.mkdir(exist_ok=True)
    for name, file in EFFECTS.items():
        sheet, count = strip(SOURCE / file)
        sheet.save(OUT / f'{name}.png', optimize=True)
        print(f'{name}.png  {count} frames of {sheet.height}x{sheet.height}  <- {file}')


if __name__ == '__main__':
    main()
