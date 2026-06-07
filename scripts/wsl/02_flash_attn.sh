#!/usr/bin/env bash
# Install flash-attn in the WSL venv.
# Strategy: try a prebuilt wheel first (fast, safe). If none exists for this
# bleeding-edge torch/cuda combo, attempt a bounded source build using the
# pip-provided nvcc. Non-fatal: if it fails, we report that torch SDPA and
# vLLM's flashinfer already provide FlashAttention-class kernels.
set -uo pipefail

export PATH="$HOME/.local/bin:$PATH"
VENV="$HOME/agent_learning/.venv"
PY="$VENV/bin/python"
# shellcheck disable=SC1091
source "$VENV/bin/activate"

echo "==> Attempt 1: prebuilt wheel only (no compile)"
if uv pip install --python "$PY" flash-attn --only-binary=:all: 2>/tmp/fa_wheel.log; then
  echo "WHEEL_OK"
else
  echo "no prebuilt wheel (tail of log):"
  tail -5 /tmp/fa_wheel.log || true

  echo "==> Attempt 2: bounded source build with pip nvcc"
  # locate nvcc from the nvidia-cuda-nvcc pip package
  NVCC_DIR="$(dirname "$(find "$VENV" -name nvcc -type f 2>/dev/null | head -1)")"
  if [ -n "$NVCC_DIR" ] && [ -x "$NVCC_DIR/nvcc" ]; then
    export CUDA_HOME="$(dirname "$NVCC_DIR")"
    export PATH="$NVCC_DIR:$PATH"
    echo "using nvcc: $("$NVCC_DIR/nvcc" --version | tail -2 | head -1)"
  else
    echo "nvcc not found in venv; cannot source-build flash-attn"
    echo "FLASH_ATTN_SKIPPED_NO_NVCC"
    exit 0
  fi

  # Limit parallel jobs to avoid OOM during compile (flash-attn is RAM hungry).
  export MAX_JOBS=4
  export FLASH_ATTENTION_FORCE_BUILD=TRUE
  echo "compiling flash-attn (MAX_JOBS=$MAX_JOBS) — this can take a while..."
  if uv pip install --python "$PY" flash-attn --no-build-isolation 2>/tmp/fa_build.log; then
    echo "BUILD_OK"
  else
    echo "source build failed (tail of log):"
    tail -20 /tmp/fa_build.log || true
    echo "FLASH_ATTN_FAILED"
    echo "NOTE: torch SDPA + vLLM flashinfer already provide flash-attention kernels."
    exit 0
  fi
fi

echo "==> Verify import"
python - <<'PY'
try:
    import flash_attn, torch
    print("flash_attn:", flash_attn.__version__)
    print("torch:", torch.__version__, "cuda", torch.version.cuda)
    print("FLASH_ATTN_IMPORT_OK")
except Exception as e:
    print("import failed:", type(e).__name__, e)
PY
echo "FLASH_ATTN_DONE"
