"""
Stage 1: render each shot in scenes_manifest.json into a clip (no text, no audio).

For shots with a real generated image present on disk, applies the requested
camera move (dolly in/out, static, approximated pan for orbit/track) via ffmpeg
zoompan. For shots whose image does not exist yet, renders a clearly labeled
PLACEHOLDER clip (grey card + shot id/description burned in) so the timeline
can be verified end-to-end without pretending real footage exists. True
"static_black" shots (intentional black holds in the story) render as plain
black with no label.

Usage:
    python render_shots.py
Reads:  scenes_manifest.json, generated_images/*.png (if present)
Writes: ../scenes/<shot_id>.mp4  and  ../renders/full_novoice.mp4
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # production/
MANIFEST = ROOT / "scripts" / "scenes_manifest.json"
SCENES_DIR = ROOT / "scenes"
RENDERS_DIR = ROOT / "renders"


SCRIPT_DIR = Path(__file__).resolve().parent


def run(cmd):
    print("  $", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True, cwd=SCRIPT_DIR)


def render_camera_clip(image_path, out_path, duration, camera, width, height, fps):
    frames = max(1, round(duration * fps))
    base_scale = f"scale={width*2}:-1,crop={width*2}:{int(height*2)}"
    if camera == "static":
        vf = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1"
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", str(image_path),
               "-vf", vf, "-t", f"{duration}", "-r", str(fps),
               "-pix_fmt", "yuv420p", str(out_path)]
    elif camera == "dolly_in":
        vf = (f"{base_scale},zoompan=z='min(zoom+0.0012,1.18)':d={frames}:"
              f"s={width}x{height}:fps={fps}")
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", str(image_path),
               "-vf", vf, "-frames:v", str(frames), "-r", str(fps),
               "-pix_fmt", "yuv420p", str(out_path)]
    elif camera == "dolly_out":
        vf = (f"{base_scale},zoompan=z='if(eq(on,0),1.18,max(zoom-0.0012,1.0))':"
              f"d={frames}:s={width}x{height}:fps={fps}")
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", str(image_path),
               "-vf", vf, "-frames:v", str(frames), "-r", str(fps),
               "-pix_fmt", "yuv420p", str(out_path)]
    else:  # orbit / track / low_angle_static -> approximated slow pan + slight zoom
        vf = (f"{base_scale},zoompan=z='min(zoom+0.0006,1.1)':d={frames}:"
              f"x='iw/2-(iw/zoom/2)+sin(on/{frames}*3.14159)*40':"
              f"y='ih/2-(ih/zoom/2)':s={width}x{height}:fps={fps}")
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", str(image_path),
               "-vf", vf, "-frames:v", str(frames), "-r", str(fps),
               "-pix_fmt", "yuv420p", str(out_path)]
    run(cmd)


def render_black(out_path, duration, width, height, fps):
    cmd = ["ffmpeg", "-y", "-f", "lavfi",
           "-i", f"color=c=black:s={width}x{height}:d={duration}:r={fps}",
           "-pix_fmt", "yuv420p", str(out_path)]
    run(cmd)


FONT = "segoeui.ttf"  # local copy (next to this script) avoids drive-letter colon in ffmpeg filter syntax


def render_placeholder(out_path, duration, width, height, fps, shot_id, label):
    text = f"PLACEHOLDER -- {shot_id}\\n{label}".replace("'", "\\'")
    cmd = ["ffmpeg", "-y", "-f", "lavfi",
           "-i", f"color=c=0x303030:s={width}x{height}:d={duration}:r={fps}",
           "-vf", (f"drawtext=fontfile={FONT}:text='{text}':fontcolor=white:fontsize=36:"
                   f"x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=10"),
           "-pix_fmt", "yuv420p", str(out_path)]
    run(cmd)


def main():
    manifest = json.loads(MANIFEST.read_text())
    width, height, fps = manifest["width"], manifest["height"], manifest["fps"]
    SCENES_DIR.mkdir(exist_ok=True)
    RENDERS_DIR.mkdir(exist_ok=True)

    clip_paths = []
    missing_images = []
    for shot in manifest["shots"]:
        duration = round(shot["end"] - shot["start"], 3)
        out_path = SCENES_DIR / f"{shot['id']}.mp4"
        image_rel = shot.get("image")
        image_path = (ROOT / image_rel) if image_rel else None

        print(f"[{shot['id']}] act={shot['act']} dur={duration}s camera={shot['camera']}")

        if shot["camera"] == "static_black" or image_path is None:
            render_black(out_path, duration, width, height, fps)
        elif image_path.exists():
            render_camera_clip(image_path, out_path, duration, shot["camera"], width, height, fps)
        else:
            missing_images.append(str(image_rel))
            render_placeholder(out_path, duration, width, height, fps, shot["id"], shot["label"])

        clip_paths.append(out_path)

    concat_list = RENDERS_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        for p in clip_paths:
            f.write(f"file '{p.resolve().as_posix()}'\n")

    out_novoice = RENDERS_DIR / "full_novoice.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
         "-c", "copy", str(out_novoice)])

    print(f"\nWrote {out_novoice}")
    if missing_images:
        print(f"\n{len(missing_images)} shots rendered as PLACEHOLDER (no generated image yet):")
        for m in missing_images:
            print("  -", m)
    else:
        print("\nAll shots used real generated images.")


if __name__ == "__main__":
    main()
