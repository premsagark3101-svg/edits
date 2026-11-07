"""
Composite the black silhouette character cutout onto a background image.
Used for shots where text-to-image generation couldn't reliably keep the
character faceless/unclothed in an outdoor golden-hour context (the model
kept defaulting to "person in a dark coat" regardless of prompt wording).

This is standard compositing: a known-good character plate (generated once,
cleanly, against a flat background) placed onto a known-good background
plate -- matches the brief's own "standing in silhouette" description.

Usage: python composite_silhouette.py <bg_path> <out_path> <scale> <x_frac> <y_frac>
  scale: character height as a fraction of background height
  x_frac, y_frac: character's horizontal center / vertical bottom as fraction of bg size
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SILHOUETTE = ROOT / "character" / "silhouette_cutout_isolated.png"


def make_alpha_silhouette(silhouette_path, threshold=128):
    img = Image.open(silhouette_path).convert("RGB")
    gray = img.convert("L")
    # black shape (low luminosity) -> opaque; white bg (high luminosity) -> transparent
    alpha = gray.point(lambda p: 255 if p < threshold else 0)
    rgba = Image.new("RGBA", img.size, (0, 0, 0, 0))
    black = Image.new("RGBA", img.size, (10, 10, 10, 255))
    rgba.paste(black, (0, 0), mask=alpha)
    bbox = alpha.getbbox()
    if bbox:
        rgba = rgba.crop(bbox)
    return rgba


def composite(bg_path, out_path, scale=0.45, x_frac=0.5, y_frac=0.88):
    bg = Image.open(bg_path).convert("RGBA")
    char = make_alpha_silhouette(SILHOUETTE)

    target_h = int(bg.height * scale)
    ratio = target_h / char.height
    target_w = int(char.width * ratio)
    char = char.resize((target_w, target_h), Image.LANCZOS)

    x = int(bg.width * x_frac - target_w / 2)
    y = int(bg.height * y_frac - target_h)

    out = bg.copy()
    out.alpha_composite(char, (x, y))
    out = out.convert("RGB")
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.save(out_path)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    bg_path, out_path = sys.argv[1], sys.argv[2]
    scale = float(sys.argv[3]) if len(sys.argv) > 3 else 0.45
    x_frac = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
    y_frac = float(sys.argv[5]) if len(sys.argv) > 5 else 0.88
    composite(bg_path, out_path, scale, x_frac, y_frac)
