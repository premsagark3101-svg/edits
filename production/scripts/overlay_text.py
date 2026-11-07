"""
Stage 2: burn in the storyboard's text overlays onto the concatenated clean
video. Produces TWO outputs, satisfying the brief's "clean version without
text" requirement without re-rendering the camera moves twice:

  renders/full_novoice.mp4  (input, already clean -- this is the deliverable
                              clean version, untouched)
  renders/full_text.mp4     (output, same video with text burned in)

Each overlay's text is written to its own small .txt file and referenced via
drawtext's textfile= option -- this sidesteps ffmpeg filtergraph quoting bugs
that apostrophes (I'm, don't, etc.) trigger when embedded inline with text=.

Usage: python overlay_text.py
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "scripts" / "scenes_manifest.json"
IN_PATH = ROOT / "renders" / "full_novoice.mp4"
OUT_PATH = ROOT / "renders" / "full_text.mp4"

SCRIPT_DIR = Path(__file__).resolve().parent
OVERLAY_TXT_DIR = SCRIPT_DIR / "overlay_txt"
FONT = "segoeui.ttf"  # local copy (next to this script) avoids drive-letter colon in ffmpeg filter syntax
FADE = 0.4  # seconds of fade in/out for each line


def build_drawtext(idx, entry):
    start, end = entry["start"], entry["end"]
    txt_path = OVERLAY_TXT_DIR / f"ov_{idx:02d}.txt"
    txt_path.write_text(entry["text"], encoding="utf-8")
    textfile_rel = f"overlay_txt/ov_{idx:02d}.txt"
    alpha = (f"if(lt(t\\,{start})\\,0\\,"
             f"if(lt(t\\,{start+FADE})\\,(t-{start})/{FADE}\\,"
             f"if(lt(t\\,{end-FADE})\\,1\\,"
             f"if(lt(t\\,{end})\\,({end}-t)/{FADE}\\,0))))")
    enable = f"between(t\\,{start}\\,{end})"
    return (f"drawtext=fontfile={FONT}:textfile={textfile_rel}:fontcolor=white:fontsize=46:"
            f"x=(w-text_w)/2:y=h*0.82:alpha={alpha}:enable={enable}")


def main():
    manifest = json.loads(MANIFEST.read_text())
    overlays = manifest["text_overlays"]
    OVERLAY_TXT_DIR.mkdir(exist_ok=True)
    filters = ",".join(build_drawtext(i, e) for i, e in enumerate(overlays))

    cmd = ["ffmpeg", "-y", "-i", str(IN_PATH), "-vf", filters,
           "-c:v", "libx264", "-preset", "slow", "-crf", "18",
           "-pix_fmt", "yuv420p", str(OUT_PATH)]
    print("  $", " ".join(cmd[:6]), "... [{} overlays]".format(len(overlays)))
    subprocess.run(cmd, check=True, cwd=SCRIPT_DIR)
    print(f"\nWrote {OUT_PATH}")


if __name__ == "__main__":
    main()
