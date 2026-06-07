#!/usr/bin/env bash
# End-to-end verification of the WSL2 GPU + serving + container stack:
#   1) torch sees the GPU (sm_120)
#   2) vLLM runs a real generation on a local model from /mnt/f
#   3) Docker works and (bonus) can see the GPU if nvidia-container-toolkit is present
set -uo pipefail

export PATH="$HOME/.local/bin:$PATH"
VENV="$HOME/agent_learning/.venv"
PY="$VENV/bin/python"
# shellcheck disable=SC1091
source "$VENV/bin/activate"

MODEL="${1:-/mnt/f/agent_learning/LLM_model_weights/Qwen3-1.7B}"

# Auto-download the small test/draft model if missing (fits easily; doubles as a
# speculative-decoding draft for Qwen3-14B — same tokenizer family).
if [ ! -f "$MODEL/config.json" ]; then
  echo "==> test model not found; downloading Qwen/Qwen3-1.7B -> $MODEL"
  HF_HUB_DISABLE_XET=1 hf download Qwen/Qwen3-1.7B --local-dir "$MODEL"
fi

echo "==================================================="
echo " 1) torch GPU check"
echo "==================================================="
python - <<'PY'
import torch
print("torch:", torch.__version__, "| cuda:", torch.version.cuda)
print("cuda available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("device:", torch.cuda.get_device_name(0))
    print("capability: sm_%d%d" % torch.cuda.get_device_capability(0))
    print("bf16 supported:", torch.cuda.is_bf16_supported())
PY

echo
echo "==================================================="
echo " 2) vLLM real generation"
echo "    model: $MODEL"
echo "==================================================="
# Run from a real .py file (NOT heredoc/stdin): vLLM uses 'spawn' under WSL and
# the spawned workers must be able to re-import the main module.
python "$(dirname "$0")/vllm_smoke.py" "$MODEL"

echo
echo "==================================================="
echo " 3) Docker checks"
echo "==================================================="
if docker info >/dev/null 2>&1; then
  echo "docker daemon: reachable (non-root)"
  echo "running hello-world..."
  docker run --rm hello-world >/dev/null 2>&1 && echo "DOCKER_RUN_OK" || echo "DOCKER_RUN_FAILED"
  echo "checking GPU-in-Docker (needs nvidia-container-toolkit)..."
  if docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi -L >/tmp/gpu_docker.log 2>&1; then
    echo "GPU_IN_DOCKER_OK: $(cat /tmp/gpu_docker.log)"
  else
    echo "GPU_IN_DOCKER_UNAVAILABLE (optional; SWE-bench/Terminal-Bench CPU containers still work)"
  fi
else
  echo "docker not reachable in this shell (try 'wsl --shutdown' then reopen)"
fi

echo "WSL_VERIFY_DONE"
