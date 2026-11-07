"""
Generate all 19 scene stills from shot_prompts.json (everything except
character_ref, which is already approved). Loads the SDXL pipeline once and
reuses it for all images, rather than paying the ~10-20s load cost per image.

Usage: python generate_all_scenes.py
"""
import json
from pathlib import Path

from generate_image import generate, get_pipe

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_FILE = Path(__file__).resolve().parent / "shot_prompts.json"


def main():
    prompts = json.loads(PROMPTS_FILE.read_text())
    get_pipe()  # load once

    todo = [(k, v) for k, v in prompts.items() if k != "character_ref"]
    print(f"Generating {len(todo)} scene images...")
    for i, (rel_path, prompt) in enumerate(todo, 1):
        out_path = ROOT / rel_path
        if out_path.exists():
            print(f"[{i}/{len(todo)}] SKIP (exists): {rel_path}")
            continue
        print(f"[{i}/{len(todo)}] {rel_path}")
        generate(prompt, out_path, seed=884471)

    print("\nDone.")


if __name__ == "__main__":
    main()
