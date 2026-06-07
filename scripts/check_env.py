"""Environment smoke test for the agent-learning workspace.

Run a quick health check of the GPU + ML stack:
    python scripts/check_env.py

Add --full to also load a local model and run a real generation:
    python scripts/check_env.py --full
"""
from __future__ import annotations

import argparse
import importlib
import os
import platform
import time
import warnings
from pathlib import Path

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "LLM_model_weights"
DATASETS_DIR = ROOT / "datasets"

GREEN, RED, YEL, DIM, RST = "\033[92m", "\033[91m", "\033[93m", "\033[2m", "\033[0m"
OK, BAD, WARN = f"{GREEN}OK{RST}", f"{RED}FAIL{RST}", f"{YEL}WARN{RST}"


def hr(title: str) -> None:
    print(f"\n{'='*62}\n {title}\n{'='*62}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="load a local model and generate")
    args = ap.parse_args()

    failures = 0

    # ----- System -----
    hr("System")
    import psutil  # bundled with gpustat dep

    print(f"OS            : {platform.platform()}")
    print(f"Python        : {platform.python_version()} ({platform.architecture()[0]})")
    print(f"CPU           : {platform.processor() or 'n/a'}")
    print(f"Logical cores : {psutil.cpu_count()}")
    print(f"RAM           : {psutil.virtual_memory().total / 1e9:.1f} GB")

    # ----- PyTorch / CUDA -----
    hr("PyTorch + CUDA")
    import torch

    print(f"torch         : {torch.__version__}")
    print(f"built cuda    : {torch.version.cuda}")
    cuda = torch.cuda.is_available()
    print(f"cuda.is_available: {OK if cuda else BAD} ({cuda})")
    if not cuda:
        print(f"{RED}No CUDA device visible — aborting GPU tests.{RST}")
        return 1
    name = torch.cuda.get_device_name(0)
    cap = torch.cuda.get_device_capability(0)
    props = torch.cuda.get_device_properties(0)
    print(f"device        : {name}")
    print(f"capability    : sm_{cap[0]}{cap[1]}")
    print(f"total VRAM    : {props.total_memory / 1e9:.1f} GB")
    bf16 = torch.cuda.is_bf16_supported()
    print(f"bf16 support  : {OK if bf16 else WARN} ({bf16})")
    if cap[0] < 12:
        print(f"{YEL}Note: expected Blackwell sm_120 for RTX 5090.{RST}")

    # ----- GPU compute benchmark -----
    hr("GPU compute benchmark (bf16 matmul)")
    n = 8192
    a = torch.randn(n, n, device="cuda", dtype=torch.bfloat16)
    b = torch.randn(n, n, device="cuda", dtype=torch.bfloat16)
    for _ in range(3):  # warmup
        c = a @ b
    torch.cuda.synchronize()
    iters = 20
    t0 = time.time()
    for _ in range(iters):
        c = a @ b
    torch.cuda.synchronize()
    dt = (time.time() - t0) / iters
    tflops = 2 * n**3 / dt / 1e12
    print(f"{n}x{n} matmul : {dt*1e3:6.2f} ms/iter  ->  {GREEN}{tflops:6.1f} TFLOP/s{RST} (bf16)")

    # ----- bitsandbytes 4-bit -----
    hr("bitsandbytes 4-bit on GPU")
    try:
        import bitsandbytes as bnb
        from bitsandbytes.nn import Linear4bit

        lin = Linear4bit(2048, 2048, bias=False, compute_dtype=torch.bfloat16).cuda()
        x = torch.randn(16, 2048, device="cuda", dtype=torch.bfloat16)
        y = lin(x)
        print(f"bitsandbytes {bnb.__version__}: 4-bit forward {OK}  (out {tuple(y.shape)})")
    except Exception as exc:
        failures += 1
        print(f"bitsandbytes  : {BAD}  {exc}")

    # ----- Library versions -----
    hr("Key library versions")
    libs = [
        "transformers", "accelerate", "datasets", "tokenizers", "peft", "trl",
        "optimum", "sentence_transformers", "huggingface_hub", "safetensors",
        "langchain", "langgraph", "openai", "anthropic", "numpy", "pandas",
    ]
    from importlib.metadata import version as _pkg_version, PackageNotFoundError

    dist_names = {"sentence_transformers": "sentence-transformers", "huggingface_hub": "huggingface-hub"}
    for mod in libs:
        try:
            m = importlib.import_module(mod)
            ver = getattr(m, "__version__", None)
            if ver is None:
                try:
                    ver = _pkg_version(dist_names.get(mod, mod))
                except PackageNotFoundError:
                    ver = "?"
            print(f"  {mod:22s} {ver}")
        except Exception as exc:
            failures += 1
            print(f"  {mod:22s} {BAD} {exc}")

    # ----- Local assets -----
    hr("Local models & datasets")
    models = [p.name for p in MODELS_DIR.iterdir() if p.is_dir()] if MODELS_DIR.exists() else []
    ds = [p.name for p in DATASETS_DIR.iterdir() if p.is_dir()] if DATASETS_DIR.exists() else []
    print(f"models  ({len(models)}): {models or '(none yet)'}")
    print(f"datasets({len(ds)}): {ds or '(none yet)'}")

    # tokenizer load test on first available model (fast, no weights)
    if models:
        from transformers import AutoTokenizer

        mpath = MODELS_DIR / models[0]
        try:
            tok = AutoTokenizer.from_pretrained(str(mpath))
            n_tok = len(tok("Hello, agent world!")["input_ids"])
            print(f"tokenizer load ({models[0]}): {OK}  (vocab={tok.vocab_size}, {n_tok} toks)")
        except Exception as exc:
            print(f"tokenizer load: {WARN}  {exc}")

    # dataset load test on first available dataset
    if ds:
        from datasets import load_dataset

        for cand in ("IFEval", "MMLU-Pro"):
            p = DATASETS_DIR / cand
            if p.exists():
                try:
                    d = load_dataset(str(p))
                    split = next(iter(d))
                    print(f"dataset load ({cand}): {OK}  splits={list(d)}, n={d[split].num_rows}")
                except Exception as exc:
                    print(f"dataset load ({cand}): {WARN}  {exc}")
                break

    # ----- Optional full generation -----
    if args.full and models:
        hr("Full model generation test")
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        # prefer a text model for the causal-LM path
        pick = next((m for m in models if "Qwen" in m), models[0])
        mpath = MODELS_DIR / pick
        print(f"loading {pick} (bf16) ...", flush=True)
        t0 = time.time()
        tok = AutoTokenizer.from_pretrained(str(mpath))
        model = AutoModelForCausalLM.from_pretrained(
            str(mpath), dtype=torch.bfloat16, device_map="cuda"
        )
        print(f"loaded in {time.time()-t0:.1f}s, VRAM used {torch.cuda.memory_allocated()/1e9:.1f} GB")
        msgs = [{"role": "user", "content": "In one sentence, what is speculative decoding?"}]
        inputs = tok.apply_chat_template(
            msgs, add_generation_prompt=True, return_tensors="pt", return_dict=True
        ).to("cuda")
        prompt_len = inputs["input_ids"].shape[1]
        t0 = time.time()
        out = model.generate(**inputs, max_new_tokens=64, do_sample=False)
        dt = time.time() - t0
        new = out[0, prompt_len:]
        print(f"generated {new.shape[0]} tokens in {dt:.2f}s ({new.shape[0]/dt:.1f} tok/s):")
        print(DIM + tok.decode(new, skip_special_tokens=True) + RST)

    hr("Result")
    if failures:
        print(f"{RED}{failures} check(s) failed.{RST}")
        return 1
    print(f"{GREEN}All checks passed. Environment is ready.{RST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
