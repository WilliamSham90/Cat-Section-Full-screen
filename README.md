# Cat Playground

A cozy pixel-art cat room that runs in the browser. Drag cats, food, toys,
beds and furniture into an isometric room, put plants and bowls up on the
tables and shelves, watch the cats get on with their day, and send them out
to the play area. Click a cat to name it, tell it what to do, or (for the
cream cat) pick a mood: hide in a box, dance, flop over… Each of the
15 room types comes furnished in its own colours, and the Photo button
pauses everything and saves a picture of the room or the whole screen.

Made by [William Sham](https://williamsham90.github.io/Portfolio/).

## Running it

The page loads images and sounds, so it needs to be served rather than
opened straight from disk. From the repository root:

```sh
python3 -m http.server 8000
```

then open <http://localhost:8000>. Any static server works (VS Code Live
Server, `npx serve`, …).

Pushing to `main` publishes the site to GitHub Pages
(`.github/workflows/static.yml`). Only `index.html`, `site.webmanifest` and
`assets/` are published.

## Layout

```
index.html            the whole app: markup, styles and script
site.webmanifest      name, colours and icons for "add to home screen"
assets/               everything the page loads
  cats/<cat>/         one strip of frames per animation: idle.png, run.png, sit.png, …
  items/              food/, toys/, beds/, furniture/, decor/
  rooms/              the 15 room types (room-01.png … room-15.png)
  skies/              backgrounds behind the room (fajr, dawn, noon, sunset, night)
  ui/                 frames, buttons and icons        ← made by tools/build_ui.py
  effects/            pixel effects                    ← made by tools/build_effects.py
  audio/sfx/          cat sounds                       ← made by tools/build_audio.py
  audio/music/        background music                 ← made by tools/build_audio.py
  icons/              favicon and app icons            ← made by tools/build_icons.py
  vendor/pixi.min.js  PixiJS 8.22.0, the renderer
  vendor/snapdom.mjs  SnapDOM 3.3.0 (MIT), draws the bar for whole-screen photos
source/               originals that the tools turn into assets (not published)
  ui/                 cat-ui.png and pastel-ui.png sheets
  effects/            pixel effect GIFs
  sounds/, music/     original WAV and Ogg files
  items/              Aseprite files and animated previews
tools/                the scripts that make the generated assets
```

File and folder names are lowercase with hyphens, so they work the same in
every browser and on every server.

## Changing the generated assets

Each tool has a list at the top of what it makes; edit it and run it from
the repository root:

| Tool | Makes | Needs |
|---|---|---|
| `python3 tools/build_ui.py` | `assets/ui/` from `source/ui/cat-ui.png` | Pillow |
| `python3 tools/build_effects.py` | `assets/effects/` from `source/effects/` | Pillow |
| `python3 tools/build_audio.py` | `assets/audio/` from `source/sounds/` and `source/music/` | ffmpeg |
| `python3 tools/build_icons.py` | `assets/icons/` (favicon, home-screen and app icons) from Coco's sprite | Pillow |

Install Pillow with `pip install pillow`.

## Adding things

- **A cat:** add a folder under `assets/cats/` with `idle.png`, `run.png`,
  `sit.png`, `sleep.png`, `jump.png` and `attack.png` (strips of square
  frames), then add a line to `CATS` in `index.html`. A cat with more
  animations gets more to do: with the mood ones (`box1`, `dance`,
  `excited`, `surprised`, `tickle`, `crying`, `dead2`, `happy`, like the
  cream cat) it gets a Moods section in its menu (see `MOODS`), and with
  `idle2` it looks round now and then.
- **An item:** add the picture under `assets/items/` and a line to `ITEMS`.
  Give big furniture `solid: true` so cats walk around it, and balls and the
  mouse bounce off it (tables are left open, because cats walk under them).
  A table or shelf lists its `surfaces` (front, left and right corners and
  height, in the picture's pixels) so small things can be put on it; see
  `SHELF` and `TABLE`.
- **A wall object:** add a line to `WALL_ITEMS` with `wall: 'left'` or
  `'right'`. A window also gets a `sill` (its bottom edge in picture
  pixels), which is where its light falls on the floor. In the app, click a
  wall object and move it with the arrow keys (Shift for bigger steps),
  remove it with Delete, or drag it to the trash.
- **A room's furniture:** each line of `ROOM_TYPES` names one of the
  `ARRANGEMENTS` (where things go) and the colours to use for it.
- **A song:** put the original in `source/music/`, add it to `MUSIC` in
  `tools/build_audio.py` and to `SONGS` in `index.html`, then run the tool.
