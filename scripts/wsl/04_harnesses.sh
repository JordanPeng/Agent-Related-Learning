#!/usr/bin/env bash
# Install the agent benchmark harnesses into the WSL venv:
#   - swebench         (SWE-bench evaluation harness; uses Docker)
#   - terminal-bench   (Terminal-Bench harness + `tb` CLI; uses Docker)
# These are separate from the HF *datasets* (already on /mnt/f); they are the
# code that actually RUNS the benchmarks.
set -uo pipefail

export PATH="$HOME/.local/bin:$PATH"
VENV="$HOME/agent_learning/.venv"
PY="$VENV/bin/python"
# shellcheck disable=SC1091
source "$VENV/bin/activate"

echo "==> Installing swebench + terminal-bench (+ docker SDK)"
uv pip install --python "$PY" swebench terminal-bench docker

echo "==> Versions / CLIs"
python - <<'PY'
import importlib
for m in ["swebench", "terminal_bench", "docker"]:
    try:
        mod = importlib.import_module(m)
        print(f"{m:16s} {getattr(mod, '__version__', 'installed')}")
    except Exception as e:
        print(f"{m:16s} IMPORT FAIL: {type(e).__name__}: {e}")
PY

echo "--- console scripts ---"
for c in tb swebench; do
  if command -v "$c" >/dev/null 2>&1; then
    echo "$c -> $(command -v "$c")"
  else
    echo "$c -> (module entrypoint)"
  fi
done

echo "==> Docker reachable from this shell?"
if docker info >/dev/null 2>&1; then
  echo "DOCKER_OK_NONROOT"
else
  echo "docker not reachable without sudo yet (group membership applies after 'wsl --shutdown')"
fi

echo "HARNESSES_DONE"
