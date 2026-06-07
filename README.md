# agent_learning

A local workspace for learning and testing LLM inference, agents, and efficiency
techniques (KV caching, quantization, speculative decoding) on **Windows + RTX 5090**.

## Hardware / environment (verified)

| Component | Value |
|-----------|-------|
| GPU | NVIDIA GeForce RTX 5090, 32 GB VRAM, Blackwell `sm_120` |
| Driver | 591.86 (supports up to CUDA 13.1) |
| Python | 3.12.13 (in `.venv`, created by `uv`) |
| PyTorch | 2.11.0 + CUDA 12.8 (`cu128` wheels — required for Blackwell) |
| bf16 | supported | 
| bitsandbytes 4-bit | working on GPU |

Measured: ~`8192³` bf16 matmul throughput is printed by `scripts/check_env.py`.

## Layout

```
agent_learning/
├─ .venv/                     # Python 3.12 environment (uv-managed)
├─ scripts/
│  ├─ check_env.py            # GPU + library health check  (add --full to generate)
│  ├─ download_data.py        # (re)download the benchmark datasets
│  └─ example_inference.py    # minimal local chat generation (--model qwen|gemma, --4bit)
├─ LLM_model_weights/         # downloaded model weights
│  ├─ gemma-4-12B-it/         # google/gemma-4-12B-it   (Apache-2.0, ~24 GB)
│  └─ Qwen3-14B/              # Qwen/Qwen3-14B           (Apache-2.0, ~30 GB)
├─ datasets/                  # downloaded benchmarks (see table below)
├─ KV_Caching/                # your study area
├─ Quantization/              # your study area
├─ Speculative_Decoding/      # your study area
├─ requirements.txt           # top-level deps (human-readable)
└─ requirements-lock.txt      # exact pinned versions (reproducible)
```

## Quick start

```powershell
# 1. activate the environment
.\.venv\Scripts\Activate.ps1

# 2. sanity-check the GPU + stack
python scripts\check_env.py            # fast checks
python scripts\check_env.py --full     # also loads Qwen3-14B and generates

# 3. run a real generation
python scripts\example_inference.py --model qwen
python scripts\example_inference.py --model gemma --4bit
```

## Models

| Folder | HF repo | Params | License | Notes |
|--------|---------|--------|---------|-------|
| `gemma-4-12B-it` | [google/gemma-4-12B-it](https://hf.co/google/gemma-4-12B-it) | ~12 B | Apache-2.0 | newest general model; reasoning/coding/agents/multimodal |
| `Qwen3-14B` | [Qwen/Qwen3-14B](https://hf.co/Qwen/Qwen3-14B) | 14.8 B | Apache-2.0 | strong general text; reasoning + coding + multilingual + agents |
| `Qwen3-1.7B` | [Qwen/Qwen3-1.7B](https://hf.co/Qwen/Qwen3-1.7B) | 1.7 B | Apache-2.0 | small/fast; vLLM smoke tests + speculative-decoding **draft** model |

Both fit on the 5090 in bf16 (≈24 GB / ≈30 GB on disk; bf16 weights are smaller in
VRAM than on-disk for Qwen due to sharding). Use `--4bit` to cut VRAM roughly in half.

## Datasets / benchmarks

Downloaded into `datasets/` via `scripts/download_data.py`.

| # | Folder | HF repo | What it measures |
|---|--------|---------|------------------|
| 1 | `BFCL_Berkeley-Function-Calling-Leaderboard` | [gorilla-llm/Berkeley-Function-Calling-Leaderboard](https://hf.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard) | Function/tool-calling accuracy, multi-step, format sensitivity (BFCL V4) |
| 2 | `tau2-bench` | [HuggingFaceH4/tau2-bench-data](https://hf.co/datasets/HuggingFaceH4/tau2-bench-data) | Multi-turn user–agent–tool interaction w/ policies + backend state |
| 3 | `SWE-bench_Verified` | [princeton-nlp/SWE-bench_Verified](https://hf.co/datasets/princeton-nlp/SWE-bench_Verified) | Real coding-agent repair (human-validated 500) |
| 4 | `Terminal-Bench` | [ia03/terminal-bench](https://hf.co/datasets/ia03/terminal-bench) | Long-horizon terminal agents: setup/debug/test |
| 5 | `LiveCodeBench` | [livecodebench/code_generation_lite](https://hf.co/datasets/livecodebench/code_generation_lite) | Modern, contamination-free coding ability |
| 6 | `IFEval` | [google/IFEval](https://hf.co/datasets/google/IFEval) | Instruction following: formatting, constraints, schema |
| 7 | `RULER` | [simonjegou/ruler](https://hf.co/datasets/simonjegou/ruler) | Long-context retrieval / multi-hop reliability |
| 8 | `LiveBench/*` | [livebench](https://hf.co/livebench) | Contamination-free general eval (reasoning, coding, math, language, data_analysis, instruction_following) |
| 9 | `MMLU-Pro` | [TIGER-Lab/MMLU-Pro](https://hf.co/datasets/TIGER-Lab/MMLU-Pro) | Harder multi-task knowledge + reasoning |

> **Note on Terminal-Bench & SWE-bench:** the HF datasets contain the *task data*.
> Actually *running* these agent harnesses also needs their execution frameworks
> (`pip install terminal-bench`, and SWE-bench's Docker-based harness). Those run
> best under **WSL2/Linux + Docker**; see below.

Re-download or fetch a subset any time:

```powershell
python scripts\download_data.py                 # everything
python scripts\download_data.py ifeval ruler    # just these keys
```

## Known Windows caveats

- **vLLM / flash-attention**: not reliably available as native Windows wheels. For
  high-throughput serving or FlashAttention-2/3, use the **WSL2** stack (already set
  up — see below). The transformers/bitsandbytes path works natively on Windows.
- **Docker-based harnesses** (SWE-bench, Terminal-Bench execution) → run under WSL2.
- **triton-windows** is installed to enable `torch.compile`/Triton kernels on Windows.
- **llama-cpp-python** is the CUDA build; a `sitecustomize.py` in the venv preloads
  PyTorch's CUDA DLLs so it finds the GPU automatically (no manual setup needed).

## Jupyter notebooks

Both environments are registered as Jupyter kernels and verified on the GPU:

| Kernel display name | Where | Use for |
|---------------------|-------|---------|
| `Python (agent_learning, RTX5090)` | Windows venv | day-to-day learning, transformers, llama.cpp |
| `Python (agent_learning WSL, vLLM+CUDA)` | WSL2 venv | vLLM serving, agent harnesses |

In VS Code: open an `.ipynb`, pick the kernel in the top-right. Or run JupyterLab:

```powershell
.\.venv\Scripts\Activate.ps1
jupyter lab
```

Starter notebook (runs a GPU smoke test): [notebooks/00_smoke_test.ipynb](notebooks/00_smoke_test.ipynb).
The first cell run warms up the kernel (a few seconds to import torch + load CUDA), then it's fast.

## WSL2 GPU stack (vLLM, Docker, agent harnesses)

A parallel Linux environment is set up for the things that need native Linux. The
Windows models/datasets are shared (no re-download) via `/mnt/f/agent_learning`.

| Component | Version / status |
|-----------|------------------|
| Ubuntu | 24.04.2 LTS (WSL2), GPU passthrough working |
| PyTorch | 2.11.0 + **CUDA 13.0**, RTX 5090 `sm_120` |
| vLLM | 0.22.1 — generation **verified** (FlashAttention-2 backend) |
| Docker | 29.5.3 (systemd) — `hello-world` verified |
| Harnesses | `swebench` 4.1.0, `terminal-bench` 0.2.18 (`tb` CLI) |
| Venv | `~/agent_learning/.venv` (on ext4, Python 3.12) |

The setup is reproducible via ordered scripts in [scripts/wsl/](scripts/wsl):

```bash
# inside WSL (wsl -d Ubuntu), from /mnt/f/agent_learning
bash scripts/wsl/00_probe.sh        # environment probe
bash scripts/wsl/01_core_env.sh     # uv venv + vLLM + ML stack
bash scripts/wsl/06_cuda_env.sh     # point CUDA_HOME at pip toolkit (for JIT)
sudo bash scripts/wsl/07_build_deps.sh   # python3-dev etc. (Triton JIT needs Python.h)
sudo bash scripts/wsl/03_docker.sh jordanpeng   # Docker engine
bash scripts/wsl/04_harnesses.sh    # swebench + terminal-bench
bash scripts/wsl/05_verify.sh       # torch + vLLM gen + docker checks
```

Run a vLLM generation any time:

```bash
wsl -d Ubuntu
cd /mnt/f/agent_learning && bash scripts/wsl/run_vllm_test.sh
```

### WSL2 gotchas (already handled in the scripts)

- vLLM uses `spawn` under WSL → test code must live in a real `.py` file, not a heredoc.
- vLLM 0.22 V2 model runner needs UVA (unavailable in WSL) → `VLLM_USE_V2_MODEL_RUNNER=0`.
- flashinfer's sampler JIT clashes with CUDA 13.3 headers → `VLLM_USE_FLASHINFER_SAMPLER=0`
  (uses vLLM's Triton sampler; attention still uses prebuilt FlashAttention-2).
- `flash-attn` has no wheel for this torch/CUDA yet and won't source-build — not needed;
  FlashAttention-2 ships inside vLLM and torch SDPA covers the rest.
- `gemma-4-12B-it` isn't supported by vLLM 0.22 (new `Gemma4Unified` arch) — use it via
  transformers; use Qwen3 models with vLLM. `Qwen3-1.7B` was added as a small vLLM/
  speculative-decoding draft model.

## Tips

- Set a token for faster, rate-limit-free downloads: `setx HF_TOKEN "hf_xxx"` (new shell).
- Enable fast transfers: `$env:HF_XET_HIGH_PERFORMANCE = "1"`.
- Monitor the GPU: `gpustat -i` or `nvidia-smi -l 1`.
