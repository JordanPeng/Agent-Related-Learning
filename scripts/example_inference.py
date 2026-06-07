"""Minimal local-inference examples for the agent-learning workspace.

Run a quick chat generation with either local model:

    python scripts/example_inference.py --model qwen      # Qwen3-14B (text)
    python scripts/example_inference.py --model gemma     # gemma-4-12B-it (multimodal-capable)
    python scripts/example_inference.py --model qwen --4bit   # load in 4-bit (bitsandbytes)

This is intentionally small and dependency-light so it doubles as a
"does my stack actually run a real model end to end?" check.
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
MODELS = {
    "qwen": ROOT / "LLM_model_weights" / "Qwen3-14B",
    "gemma": ROOT / "LLM_model_weights" / "gemma-4-12B-it",
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=list(MODELS), default="qwen")
    ap.add_argument("--prompt", default="Explain KV caching in two sentences.")
    ap.add_argument("--max-new-tokens", type=int, default=128)
    ap.add_argument("--4bit", dest="four_bit", action="store_true", help="load in 4-bit via bitsandbytes")
    args = ap.parse_args()

    path = MODELS[args.model]
    if not path.exists():
        raise SystemExit(f"Model not found: {path}\nDownload it first (see README).")

    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"Loading {args.model} from {path} ...", flush=True)
    quant_kwargs = {}
    if args.four_bit:
        from transformers import BitsAndBytesConfig

        quant_kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )

    tok = AutoTokenizer.from_pretrained(str(path))
    t0 = time.time()
    model = AutoModelForCausalLM.from_pretrained(
        str(path),
        dtype=torch.bfloat16,
        device_map="cuda",
        **quant_kwargs,
    )
    print(f"Loaded in {time.time()-t0:.1f}s | VRAM {torch.cuda.memory_allocated()/1e9:.1f} GB")

    messages = [{"role": "user", "content": args.prompt}]
    inputs = tok.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt", return_dict=True
    ).to("cuda")
    prompt_len = inputs["input_ids"].shape[1]

    t0 = time.time()
    out = model.generate(**inputs, max_new_tokens=args.max_new_tokens, do_sample=False)
    dt = time.time() - t0
    new = out[0, prompt_len:]
    text = tok.decode(new, skip_special_tokens=True)

    print("\n--- prompt ---")
    print(args.prompt)
    print("\n--- response ---")
    print(text)
    print(f"\n{new.shape[0]} tokens in {dt:.2f}s -> {new.shape[0]/dt:.1f} tok/s")


if __name__ == "__main__":
    main()
