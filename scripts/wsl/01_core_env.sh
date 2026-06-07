#!/usr/bin/env bash
# Build the core WSL2 GPU environment: uv + venv (ext4) + vLLM + essential ML stack.
# vLLM is installed first so it dictates a self-consistent torch (cu128) build; the
# lighter mirror stack is layered on top.
set -euo pipefail

VENV="$HOME/agent_learning/.venv"
PROJ="$HOME/agent_learning"
mkdir -p "$PROJ"

echo "==> [1/5] Ensure uv is installed"
if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"
uv --version

echo "==> [2/5] Create venv (Python 3.12) at $VENV"
uv venv --python 3.12 "$VENV"
# shellcheck disable=SC1091
source "$VENV/bin/activate"
python --version
echo "venv python: $(which python)"

echo "==> [3/5] Install vLLM (brings a consistent cu128 torch)"
# Let vLLM resolve its matching torch/cuda. --torch-backend=auto picks cu128 for Blackwell.
uv pip install --python "$VENV/bin/python" vllm --torch-backend=auto

echo "==> [4/5] Layer the essential HF / training stack"
uv pip install --python "$VENV/bin/python" \
  transformers accelerate datasets tokenizers safetensors \
  "huggingface_hub" hf_transfer hf_xet \
  sentencepiece protobuf einops \
  peft trl bitsandbytes \
  jupyterlab ipykernel ipywidgets rich pandas numpy \
  openai anthropic

echo "==> [5/5] Versions"
python - <<'PY'
import importlib
mods = ["torch", "vllm", "transformers", "accelerate", "datasets", "peft", "trl", "bitsandbytes"]
for m in mods:
    try:
        mod = importlib.import_module(m)
        print(f"{m:14s} {getattr(mod, '__version__', '?')}")
    except Exception as e:
        print(f"{m:14s} IMPORT FAIL: {type(e).__name__}: {e}")
import torch
print("torch.cuda.is_available:", torch.cuda.is_available())
print("torch.version.cuda      :", torch.version.cuda)
if torch.cuda.is_available():
    print("device                  :", torch.cuda.get_device_name(0))
    cap = torch.cuda.get_device_capability(0)
    print("capability              : sm_%d%d" % cap)
# is flash_attn already available (e.g. via vllm)?
try:
    import flash_attn
    print("flash_attn (preinstalled):", flash_attn.__version__)
except Exception:
    print("flash_attn (preinstalled): not present")
PY

echo "CORE_ENV_DONE venv=$VENV"
