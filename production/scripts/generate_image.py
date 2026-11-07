"""
Local image generation for THE EMPTY SPACE, using SDXL base 1.0 with model
CPU-offload (needed to fit the pipeline on a 6GB laptop GPU).

Usage:
    python generate_image.py <prompt_key_or_literal_prompt> <output_path> [seed]

If <prompt_key_or_literal_prompt> matches an id in shot_prompts.json, its prompt
is used; otherwise the raw string is used as the prompt directly.
"""
import json
import sys
from pathlib import Path

import torch
from diffusers import StableDiffusionXLPipeline

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_FILE = Path(__file__).resolve().parent / "shot_prompts.json"

NEGATIVE = ("face, eyes, mouth, nose, facial features, hair, text, watermark, logo, "
            "cartoon, anime, low quality, blurry, extra limbs, deformed, "
            "nudity, nipples, navel, genitalia, anatomical detail, muscle definition, "
            "sexualized, nsfw, pedestal, plinth, display stand, mannequin stand, base platform, "
            "clothing, dress, robe, garment, fabric, fashion, realistic human skin, "
            "fashion editorial, fashion photography, portrait photography, model photoshoot")

_pipe = None


def get_pipe():
    global _pipe
    if _pipe is None:
        print("Loading SDXL base 1.0 (first run downloads ~7GB)...")
        _pipe = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True,
        )
        _pipe.enable_model_cpu_offload()
        _pipe.enable_attention_slicing()
    return _pipe


def generate(prompt, out_path, seed=884471, steps=30, guidance=7.0, width=1024, height=576):
    pipe = get_pipe()
    gen = torch.Generator(device="cpu").manual_seed(seed)
    image = pipe(
        prompt=prompt,
        negative_prompt=NEGATIVE,
        num_inference_steps=steps,
        guidance_scale=guidance,
        width=width,
        height=height,
        generator=gen,
    ).images[0]
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path)
    print(f"Saved {out_path}")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    key = sys.argv[1]
    out_path = sys.argv[2]
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 884471

    prompt = key
    if PROMPTS_FILE.exists():
        prompts = json.loads(PROMPTS_FILE.read_text())
        if key in prompts:
            prompt = prompts[key]

    generate(prompt, out_path, seed=seed)


if __name__ == "__main__":
    main()
