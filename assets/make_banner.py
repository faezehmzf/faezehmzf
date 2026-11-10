"""Build the animated profile banner (assets/banner.webp) from the network video.

The video's own name lettering is covered with the background and the name is
drawn again in bold SF Pro, the font of the earlier banner. The result is an
animated WebP, which GitHub shows like a GIF.

Run:  python3 assets/make_banner.py VIDEO.mp4 [--ffmpeg PATH]
Needs ffmpeg, Pillow (with WebP) and NumPy; the font is macOS's SFNS.ttf.
"""
import argparse
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent / "banner.webp"
W, H = 1280, 400            # output size (the video is 1920 x 600)
FPS = 30
NAME = "Faezeh Mozaffari"
FONT = "/System/Library/Fonts/SFNS.ttf"
FONT_SIZE = 52              # as in the earlier banner
COLOUR = (243, 244, 248)    # #f3f4f8, the earlier title colour
RADIUS = 18                 # rounded corners, as in the earlier banner
# area of the video's own name lettering, in output pixels
PATCH = (725, 166, 1115, 232)


def frames(video, ffmpeg):
    cmd = [ffmpeg, "-v", "error", "-i", str(video), "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    size = W * H * 3
    while True:
        buf = proc.stdout.read(size)
        if len(buf) < size:
            break
        yield Image.frombytes("RGB", (W, H), buf)
    proc.wait()


def clean_patch(frame):
    """Fill the name area row by row, blending the background on its left and right."""
    x0, y0, x1, y1 = PATCH
    a = np.asarray(frame).astype(float)
    left, right = a[y0:y1, x0 - 1], a[y0:y1, x1]
    t = np.linspace(0, 1, x1 - x0)[None, :, None]
    fill = left[:, None, :] * (1 - t) + right[:, None, :] * t
    return Image.fromarray(fill.round().astype(np.uint8))


def name_layer():
    font = ImageFont.truetype(FONT, FONT_SIZE)
    font.set_variation_by_axes([100, FONT_SIZE, 400, 700])   # width, optical size, grade, weight
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = PATCH
    draw.text((x0 + 20, (y0 + y1) / 2), NAME, font=font, fill=COLOUR + (255,), anchor="lm")
    return layer


def rounded_mask():
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, W - 1, H - 1), RADIUS, fill=255)
    return mask


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video", type=Path)
    ap.add_argument("--ffmpeg", default="ffmpeg")
    args = ap.parse_args()

    patch, text, mask, out = None, name_layer(), rounded_mask(), []
    for frame in frames(args.video, args.ffmpeg):
        if patch is None:
            patch = clean_patch(frame)
        frame.paste(patch, PATCH[:2])
        frame = Image.alpha_composite(frame.convert("RGBA"), text)
        frame.putalpha(mask)
        out.append(frame)
    out[0].save(OUT, save_all=True, append_images=out[1:], duration=round(1000 / FPS), loop=0,
                quality=82, method=6)
    print(f"{len(out)} frames -> {OUT} ({OUT.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
