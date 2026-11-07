# THE EMPTY SPACE — Shot List & Generation Prompts

Status: no reference images exist in the project folder, so every prompt below is built
from the brief's written description only. Once real reference images are supplied,
swap them in via img2img/IP-Adapter conditioning for tighter character consistency.

Character lock (reused verbatim in every prompt):
`a single faceless gender-neutral humanoid figure, smooth featureless oval head with no eyes nose mouth ears or hair, no clothing, no accessories, natural human body proportions, slim average build, smooth matte material, minimalist 3D render, photorealistic lighting, octane render, studio lighting`

Negative prompt (reused everywhere): `face, eyes, mouth, nose, facial features, text, watermark, logo, multiple characters unless specified, cartoon, anime, low quality, blurry, extra limbs`

Fixed seed for the character across all shots: **SEED_CHARACTER = 884471** (set once pipeline is up; do not change between acts).

---

## ACT 1 — I AM FINE (00:00–00:35)

1. **[00:00–00:02] Black frame.** No generation needed — pure #000000, 2s, held in edit.
2. **[00:02–00:10] Establishing wide.** Prompt: `extreme wide shot, enormous empty white minimalist room, smooth white walls and floor, soft diffused overhead light, single faceless humanoid standing centered in the distance, vast negative space, architectural minimalism, long soft shadow, 3D render` + character lock.
3. **[00:10–00:18] Slow dolly-in.** Same room, tighter composition, character mid-ground, camera-forward framing (generate 2–3 frames at increasing scale to fake a dolly via ffmpeg zoompan).
4. **[00:18–00:26] Mirror shot.** Prompt: `floor-to-ceiling minimalist mirror in white room, faceless humanoid standing confidently facing its own reflection, symmetrical composition, soft directional light, subtle long shadow on floor` + character lock.
5. **[00:26–00:35] Walk-away wide.** Prompt: `wide shot, faceless humanoid walking away from camera across white minimalist room, long dramatic shadow trailing behind, calm confident posture, soft overhead lighting` + character lock.

Text overlays (white, minimal sans-serif, centered lower third, 1.5s fade in/out each):
"I'm doing fine." / "I'm a good person." / "I don't hurt anyone." / "I'm not like those people."

---

## ACT 2 — THE SEARCH (00:35–01:35)

**Scene 1 — Material possessions (00:35–00:51)**
Prompt: `faceless humanoid standing in white void, floating luxury wristwatch, stack of paper currency, and golden trophy hovering nearby, humanoid reaching toward them, objects rendered with soft dissolve/particle disintegration, minimalist 3D render, dramatic side lighting` + character lock.
Text: "Maybe I need more."

**Scene 2 — Acceptance / mirrors (00:51–01:07)**
Prompt: `faceless humanoid surrounded by dozens of floor-to-ceiling mirrors in a circular white room, infinite reflections, humanoid looking around searching, symmetrical kaleidoscope composition, cool white lighting` + character lock.
Text: "Maybe I need to be accepted."

**Scene 3 — Distraction / screens (01:07–01:21)**
Prompt: `faceless humanoid in dark void surrounded by floating glowing rectangular screens and abstract notification light orbs, humanoid reaching toward the lights, screens powering off one by one, cold blue-white glow against black background, minimalist 3D render` + character lock.
Text: "Maybe I just need a distraction."

**Scene 4 — The doorway (01:21–01:35)**
Prompt: `wide shot, bright rectangular doorway glowing in a dark minimalist corridor, faceless humanoid walking through into another identical empty white room, symmetrical architectural framing, dramatic contrast lighting` + character lock, then a second wide: `faceless humanoid standing alone in center of vast empty white room, extreme wide shot, tiny figure in negative space, soft overhead light, long shadow` + character lock.
Text: "Maybe then I'll feel complete."

---

## ACT 3 — THE REALIZATION (01:35–02:45)

1. **[01:35–01:47] Corridor passerby.** `minimalist grey corridor, second faceless humanoid sitting on floor against wall, main faceless humanoid walking past in foreground without stopping, dramatic side lighting, long shadows, monochrome palette` + character lock (two humanoids, same material/proportions).
2. **[01:47–01:58] Reaching figure.** `faceless humanoid figure reaching one arm out from the floor toward camera, main humanoid hesitating a few steps away then turning its body away, moody low-key lighting, deep shadow, grayscale` + character lock. Text: "Sometimes, we look away."
3. **[01:58–02:10] Pointing / mirror reveal.** `faceless humanoid standing with arm extended pointing forward, camera slowly orbiting 180 degrees to reveal the pointing arm is aimed at a floor-to-ceiling mirror showing its own reflection, dramatic high-contrast lighting, monochrome` + character lock. Text: "We see what's wrong with others." / "But what about us?"
4. **[02:10–02:22] Symbolic vignettes (4 quick shots, ~3s each):**
   - `faceless humanoid standing with one arm hidden behind its back concealing a broken object, dim side light, grayscale`
   - `faceless humanoid turning its back on a second humanoid kneeling on the floor, cold lighting, long shadow`
   - `faceless humanoid standing upright and proud on a small platform while a second humanoid struggles below it, high contrast lighting`
   - `faceless humanoid with arms crossed, body language of refusal, facing away from camera, dark minimalist room`
   All with character lock.
5. **[02:22–02:38] The growing shadow.** `faceless humanoid standing before a massive blank wall, dramatic low-angle key light casting an enormous distorted shadow on the wall far larger than the figure itself, the shadow looming and towering, body of character stays unchanged and small, high-contrast black and white, cinematic` + character lock. Text sequence: "Our excuses." / "Our selfishness." / "Our hidden moments."
6. **[02:38–02:45] Turning toward the shadow.** `faceless humanoid slowly turning to face its own enormous towering shadow on the wall, wide shot, dramatic chiaroscuro lighting, monochrome` + character lock. Text: "Not just them." / "Not just those people." / "All of us." — then hard cut to black, hold in silence (duration per brief, do not shorten).

---

## ACT 4 — THE EMPTY SPACE (02:45–03:10)

1. **[02:45–02:55] Sitting alone.** `extreme wide shot, enormous empty white room completely bare, no objects, faceless humanoid sitting alone on the floor in the center, camera slowly pulling backward making the figure appear smaller and smaller, soft even lighting, vast negative space, minimalist 3D render` + character lock. Text: "We kept searching." / "In everything."
2. **[02:55–03:10] The light appears.** `same vast white room now shifting to soft dim tone, a single small distant point of warm golden light glowing far away near the horizon of the room, faceless humanoid lifting its head toward the light, subtle peaceful atmosphere, soft bloom, cinematic` + character lock. Text: "But what if we were missing Someone?"

---

## ACT 5 — LOVE CAME DOWN (03:10–03:50)

1. **[03:10–03:20] Star forms, character walks toward it.** `distant point of golden light growing into a glowing symbolic Christmas star above a dark horizon, faceless humanoid standing and walking toward the light across a dark minimalist plane, warm golden rim lighting against cool dark background, cinematic wide shot` + character lock. Text: "Love came looking for us."
2. **[03:20–03:28] Manger silhouette.** `simple elegant silhouette of a minimalist manger structure beneath a glowing star, warm golden backlight, no figures inside, symbolic and abstract, soft atmospheric haze, cinematic wide shot`. Text: "Jesus."
3. **[03:28–03:40] Cross on the hill.** `simple wooden cross standing alone on a distant hill silhouette, warm golden hour lighting, dramatic sky, cinematic horizon shot, beautifully illuminated, minimalist composition`. Text: "Born for us."
4. **[03:40–03:48] Character before the cross.** `faceless humanoid standing in silhouette before a distant illuminated wooden cross on a hill, warm golden light gently washing over the figure, its once-enormous shadow now soft and small behind it, wide cinematic shot` + character lock. Text: "LOVE CAME DOWN." then "JESUS".
5. **[03:48–03:50] Fade to black.** Cross lingers briefly, then full fade to black, music resolves.

---

## Pipeline note
Every "shot" above is a still composition. The brief's camera moves (dolly-in, orbit, pull-back)
will be simulated in ffmpeg via zoompan/crop keyframing on the generated stills, per the
chosen production path (local image generation + programmatic camera motion, not true
AI video generation).
