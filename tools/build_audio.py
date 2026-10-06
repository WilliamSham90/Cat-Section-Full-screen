"""Make the page's sound files from the originals in "Cat sounds" and music/.

The originals are large WAVs (up to 96 kHz) and Ogg Vorbis, which iPhone
Safari may not play. This writes small MP3s, which every browser plays,
levelled so no sound is much louder than the others:

  audio/sfx/<name>.mp3    mono, leading silence trimmed, -20 LUFS
  audio/music/<name>.mp3  stereo, -20 LUFS (the page plays music quieter still)

Levelling is ffmpeg's two-pass loudnorm in linear mode, so each file is
just turned up or down as a whole; the music's dynamics are untouched.

Run from the repository root after adding or changing sounds:

    python3 tools/build_audio.py

Needs ffmpeg with libmp3lame.
"""
import json
import subprocess
from pathlib import Path

OUT = Path('audio')

SFX = {
    'meow1': 'Cat sounds/Cat_SFX_Meow1.wav',
    'meow2': 'Cat sounds/Cat_SFX_Meow2.wav',
    'meow3': 'Cat sounds/Cat_SFX_Meow3.wav',
    'meow4': 'Cat sounds/Cat_SFX_Meow4.wav',
    'hiss': 'Cat sounds/Cat_SFX_Hiss.wav',
    'purr': 'Cat sounds/Cat_SFX_Purr.wav',
    'scratch': 'Cat sounds/Cat_SFX_Litter.wav',
}
MUSIC = {
    'forgotten-biomes': 'music/Forgotten Biomes.ogg',
    'polar-lights': 'music/Polar Lights.ogg',
    'sunlight-through-leaves': 'music/Sunlight Through Leaves.ogg',
    'what-clouds-are-made-of': 'music/What Clouds Are Made Of.ogg',
}
TARGET = 'I=-20:TP=-2:LRA=11'


def measure(src, pre):
    """First loudnorm pass: how loud the file is."""
    out = subprocess.run(
        ['ffmpeg', '-hide_banner', '-i', src, '-af', f'{pre}loudnorm={TARGET}:print_format=json', '-f', 'null', '-'],
        capture_output=True, text=True, check=True).stderr
    return json.loads(out[out.rindex('{'):out.rindex('}') + 1])


def encode(src, dest, pre, args):
    m = measure(src, pre)
    norm = (f'loudnorm={TARGET}:linear=true:measured_I={m["input_i"]}:measured_TP={m["input_tp"]}'
            f':measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}')
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', src,
                    '-af', f'{pre}{norm}', *args, str(dest)], check=True)
    print(f'{dest}  {dest.stat().st_size // 1024} KB  (was {m["input_i"]} LUFS)')


def main():
    (OUT / 'sfx').mkdir(parents=True, exist_ok=True)
    (OUT / 'music').mkdir(parents=True, exist_ok=True)
    trim = 'silenceremove=start_periods=1:start_threshold=-50dB,'
    for name, src in SFX.items():
        encode(src, OUT / 'sfx' / f'{name}.mp3', trim, ['-ac', '1', '-ar', '44100', '-c:a', 'libmp3lame', '-q:a', '4'])
    for name, src in MUSIC.items():
        encode(src, OUT / 'music' / f'{name}.mp3', '', ['-ar', '44100', '-c:a', 'libmp3lame', '-q:a', '5'])


if __name__ == '__main__':
    main()
