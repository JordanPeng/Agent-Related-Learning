#!/usr/bin/env bash
# Final WSL touches:
#   - register the venv as a Jupyter kernel ("agent-learning-wsl")
#   - freeze the exact package versions to a lock file
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
VENV="$HOME/agent_learning/.venv"
PY="$VENV/bin/python"
# shellcheck disable=SC1091
source "$VENV/bin/activate"

echo "==> Installing ipykernel + registering kernel"
uv pip install --python "$PY" ipykernel >/dev/null 2>&1 || true
"$PY" -m ipykernel install --user \
  --name agent-learning-wsl \
  --display-name "Python (agent_learning WSL, vLLM+CUDA)"

echo "==> Registered kernels:"
"$PY" -m jupyter kernelspec list 2>/dev/null || true

echo "==> Freezing WSL lock file -> /mnt/f/agent_learning/requirements-lock.wsl.txt"
uv pip freeze --python "$PY" > /mnt/f/agent_learning/requirements-lock.wsl.txt
echo "frozen $(wc -l < /mnt/f/agent_learning/requirements-lock.wsl.txt) packages"
echo "WSL_FINALIZE_DONE"
