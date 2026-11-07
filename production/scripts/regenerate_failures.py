"""
Regenerate specific failing shots with alternate seeds, saving each candidate
separately (not overwriting) so they can be visually reviewed before picking
a winner. Run after a QC pass identifies which shot keys failed.

Usage: python regenerate_failures.py
"""
import json
from pathlib import Path

from generate_image import generate, get_pipe

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_FILE = Path(__file__).resolve().parent / "shot_prompts.json"

FAILING_KEYS = [
    "generated_images/A2_S1_possessions.png",
    "generated_images/A5_S1_star.png",
    "generated_images/A5_S4_before_cross.png",
]

ALT_SEEDS = [20260303, 20260404, 20260505]


def main():
    prompts = json.loads(PROMPTS_FILE.read_text())
    get_pipe()

    for key in FAILING_KEYS:
        prompt = prompts[key]
        stem = Path(key).stem
        for seed in ALT_SEEDS:
            out_path = ROOT / "generated_images" / "candidates" / f"{stem}_seed{seed}.png"
            print(f"{stem} seed={seed}")
            generate(prompt, out_path, seed=seed, steps=32, guidance=8.0)

    print("\nDone. Review production/generated_images/candidates/ and pick winners.")


if __name__ == "__main__":
    main()
