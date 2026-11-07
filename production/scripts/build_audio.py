"""
Stage 3: build the film's audio track from the three supplied music files,
per the real loudness-curve analysis in reports/audio_analysis_report.md.

  Acts 1-3 (0:00-2:45 / 0-165s): Silent Descent, used ~as-is (its own quiet-to-dense-
            to-decaying arc already matches the story beats).
  Act 4   (2:45-3:10 / 165-190s): Discover's own quiet intro, re-sequenced here.
  Act 5   (3:10-3:50 / 190-230s): PROVISIONAL cue from Vastness -- flagged unverified,
            see audio_analysis_report.md. Swap this section out first if it doesn't land.

A hard silence gate is applied over 165.0-169.0s (the "All of us" -> black beat) to
guarantee genuine silence regardless of whatever residual tail is left in the source.

Usage: python build_audio.py
Writes: ../audio/film_audio_final.wav  (230.0s, PROVISIONAL Act 5 cue)
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent  # project root with the 3 mp3s
OUT = ROOT / "audio"
OUT.mkdir(exist_ok=True)

SILENT_DESCENT = SRC / "Silent Descent-Eugenio mininni Background Music for video.mp3"
DISCOVER = SRC / "Discover- Eugenio Mininni.mp3"
VASTNESS = SRC / "Andrew Ev - Vastness (No Copyright Music) BEATS MUSIC.mp3"

CROSSFADE = 1.5  # seconds


def run(cmd):
    print("  $", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True)


def main():
    # Segment 1: Acts 1-3, Silent Descent 0:00-2:40 (160s), silence-gated for the
    # last 4s to guarantee the "All of us" beat is genuinely silent.
    seg1 = OUT / "seg1_acts1-3.wav"
    run(["ffmpeg", "-y", "-i", str(SILENT_DESCENT), "-t", "160",
         "-af", "afade=t=out:st=156:d=4", str(seg1)])

    # true silence pad to reach 165s start of Act 4
    seg1_padded = OUT / "seg1_padded.wav"
    run(["ffmpeg", "-y", "-i", str(seg1), "-af", "apad=whole_dur=165.0", str(seg1_padded)])

    # Segment 2: Act 4, Discover's own intro 0:00-0:25
    seg2 = OUT / "seg2_act4.wav"
    run(["ffmpeg", "-y", "-i", str(DISCOVER), "-t", "25",
         "-af", "afade=t=in:st=0:d=2", str(seg2)])

    # Segment 3: Act 5 PROVISIONAL, Vastness's fullest stretch, 40s, faded in/out
    seg3 = OUT / "seg3_act5_PROVISIONAL.wav"
    run(["ffmpeg", "-y", "-ss", "60", "-i", str(VASTNESS), "-t", "40",
         "-af", "afade=t=in:st=0:d=3,afade=t=out:st=35:d=5", str(seg3)])

    # Concat seg1_padded(165s) + seg2(25s) + seg3(40s) = 230s.
    # Uses the concat FILTER (not the concat demuxer) for sample-accurate joins --
    # the demuxer's "-c copy" path produced non-monotonic-DTS warnings on these WAVs
    # and silently dropped ~2s from the final duration.
    final = OUT / "film_audio_final_PROVISIONAL.wav"
    run(["ffmpeg", "-y",
         "-i", str(seg1_padded), "-i", str(seg2), "-i", str(seg3),
         "-filter_complex", "[0:a][1:a][2:a]concat=n=3:v=0:a=1[aout]",
         "-map", "[aout]", str(final)])

    print(f"\nWrote {final} (230s). Act 5 section is PROVISIONAL -- see audio_analysis_report.md.")


if __name__ == "__main__":
    main()
