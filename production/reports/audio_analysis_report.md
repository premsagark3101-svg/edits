# Audio Analysis — real signal data, not guesswork from titles

Method: ffprobe for exact duration/format, then ffmpeg `astats` RMS level measured
in 5-second windows across each track (raw CSVs in `audio_analysis/*.csv`). This is
genuine measurement of loudness-over-time (the track's dynamic shape), not a title-based
guess. It **cannot** tell me instrumentation/timbre (piano vs strings vs synth) — only
amplitude over time. That limitation is called out below where it matters.

## Track shapes (measured)

**Andrew Ev – Vastness** (230.8s) — flat, dense ≈ -9 dB RMS for essentially the entire
track, only dropping (to -14.8 dB) in the last ~5 seconds as an outro fade. No real
dynamic arc. Reads as a steady "beats" bed, not a track with a quiet→loud emotional
journey. Its duration coincidentally matches the film's 230s almost exactly, which made
it tempting to use start-to-end as the whole score — but a flat track contradicts the
brief's required 5-stage emotional progression, so I'm **not** doing that.

**Discover – Eugenio Mininni** (143.7s) — quiet/sparse open (0–10s, -42 to -33 dB) with
a moving, oscillating passage from 10–30s (-20 to -36 dB, suggests a repeated motif
rather than a sustained pad), settling into a fuller plateau from ~30–125s (-14 to -18
dB), then a long tail fading to near-silence by 145s (-61 dB).

**Silent Descent – Eugenio Mininni** (160.5s) — gentle open (0–35s, ≈ -30 to -26 dB),
slow intensification (35–65s, -26 to -21 dB), a clearly louder/denser middle section
(70–125s, -12 to -16 dB), then a long decay back toward silence by the track's own end
(125–160s, falling to -70 dB — essentially inaudible).

## Structural fit to the film's 5 acts

Silent Descent's own arc — quiet → building → dense middle → decay to near-silence —
lines up with Acts 1–3 almost without needing to touch it:

- **Act 1 (00:00–00:35)**: Silent Descent 0:00–0:35 (its own quiet opening). No edit needed.
- **Act 2 (00:35–01:35, 60s)**: Silent Descent continues 0:35–1:35 of track time — this
  is exactly its "slow intensification into denser middle" stretch, which matches the
  brief's Act 2 instruction ("music gradually becomes more restless") with no contrivance.
- **Act 3 (01:35–02:45, 70s)**: Silent Descent 1:35–2:40 (105s in) covers the dense
  middle (the shadow-reveal climax); the track's natural decay from ~2:05–2:40 falls
  toward -70 dB right as the story needs the "All of us" → black → **genuine silence**
  beat. This is a real alignment in the source material, not something I'm forcing —
  the track runs out of material almost exactly where the silence needs to land. I'd
  extend the last ~4–5s of true silence with a hard volume gate rather than leave any
  residual tail, to guarantee the brief's "do not shorten this moment" requirement.

- **Act 4 (02:45–03:10, 25s)**: Discover's own quiet opening (0:00–0:25, sparse/moving,
  -42 to -20 dB) fits "very soft isolated piano notes, delicate shimmer" far better than
  anything in Vastness or the tail of Silent Descent. Re-using Discover's intro here
  (rather than at its own position in the film) is a deliberate re-sequencing — normal
  music editing, and allowed by the brief ("you may combine multiple tracks").

- **Act 5 (03:10–03:50, 40s)**: **Open problem.** None of the three tracks shows a
  late warm/orchestral swell in the loudness data — Discover and Silent Descent both
  fade *down* near their own endings, and Vastness stays flat until a brief fade in its
  final 5 seconds. Amplitude data alone can't confirm whether any of them is even
  orchestral/warm in timbre (that needs an actual listen, which I can't do). My placeholder
  plan uses Vastness's sustained body (its most "full" stretch) under Act 5, pitched down
  in the mix and crossfaded in — but **I'm flagging this as unverified**, not presenting
  it as settled. Recommend you give these three tracks a 40-second gut-check specifically
  for the Act 5 climax before I lock the final mix — if none of them feel right, that's
  the one place in the whole plan where a 4th track may genuinely be needed.

## What ships now

`scripts/build_audio.py` implements the Acts 1–3 plan (Silent Descent, essentially used
as-is) and Act 4 (Discover's intro, re-sequenced) with crossfades at the trim points, a
hard silence gate for the "All of us" moment, and a provisional Act 5 cue from Vastness
clearly marked PROVISIONAL in the script's output filename so it's never mistaken for a
final, approved mix.
