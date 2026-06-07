"""Standalone vLLM generation test (must be a real file so vLLM's `spawn`
workers can re-import it under WSL, where NVML is not fork-safe).

    python vllm_smoke.py [/path/to/model]
"""
import os
import sys
import time

# WSL workarounds (must be set before importing vllm):
#  - V2 model runner requires UVA, reported unavailable under WSL2 -> use V1.
#  - flashinfer's sampler JIT-compiles CUDA kernels that are incompatible with the
#    pip CUDA 13.3 headers; use vLLM's native Torch sampler instead. Attention still
#    uses prebuilt FlashAttention-2, so this only affects token sampling.
os.environ.setdefault("VLLM_USE_V2_MODEL_RUNNER", "0")
os.environ.setdefault("VLLM_USE_FLASHINFER_SAMPLER", "0")

from vllm import LLM, SamplingParams


def main() -> None:
    model = sys.argv[1] if len(sys.argv) > 1 else \
        "/mnt/f/agent_learning/LLM_model_weights/Qwen3-1.7B"

    t0 = time.time()
    llm = LLM(
        model=model,
        dtype="bfloat16",
        gpu_memory_utilization=float(os.environ.get("VLLM_GPU_UTIL", "0.55")),
        max_model_len=4096,
        enforce_eager=True,  # skip CUDA-graph capture for a faster one-shot test
    )
    print(f"vLLM engine ready in {time.time()-t0:.1f}s")

    prompts = ["Explain speculative decoding in one sentence."]
    sp = SamplingParams(temperature=0.0, max_tokens=64)
    t0 = time.time()
    outs = llm.generate(prompts, sp)
    dt = time.time() - t0
    out = outs[0].outputs[0]
    ntok = len(out.token_ids)
    print(f"generated {ntok} tokens in {dt:.2f}s ({ntok/dt:.1f} tok/s)")
    print("--- output ---")
    print(out.text.strip())
    print("VLLM_GEN_OK")


if __name__ == "__main__":
    main()
