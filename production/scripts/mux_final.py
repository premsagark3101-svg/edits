"""
Stage 4: mux picture + audio into the final deliverables.

Writes:
  renders/THE_EMPTY_SPACE_FINAL.mp4   (full_text.mp4 + film audio)
  renders/THE_EMPTY_SPACE_CLEAN.mp4   (full_novoice.mp4 + film audio, no text)

Usage: python mux_final.py
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RENDERS = ROOT / "renders"
AUDIO = ROOT / "audio" / "film_audio_final_PROVISIONAL.wav"


def run(cmd):
    print("  $", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True)


def mux(video_in, out_name):
    out_path = RENDERS / out_name
    run(["ffmpeg", "-y", "-i", str(video_in), "-i", str(AUDIO),
         "-c:v", "libx264", "-preset", "slow", "-crf", "18",
         "-c:a", "aac", "-b:a", "256k",
         "-map", "0:v:0", "-map", "1:a:0",
         "-shortest", "-r", "24", str(out_path)])
    print(f"Wrote {out_path}")


def main():
    mux(RENDERS / "full_text.mp4", "THE_EMPTY_SPACE_FINAL.mp4")
    mux(RENDERS / "full_novoice.mp4", "THE_EMPTY_SPACE_CLEAN.mp4")


if __name__ == "__main__":
    main()
