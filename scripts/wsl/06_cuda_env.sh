#!/usr/bin/env bash
# Make the pip-provided CUDA toolkit (nvidia/cu13) discoverable so flashinfer /
# torch can JIT-compile kernels under WSL. Sets CUDA_HOME for:
#   (a) any Python process in the venv  -> via sitecustomize.py
#   (b) interactive shells              -> via an appended block in bin/activate
# Idempotent.
set -euo pipefail

VENV="$HOME/agent_learning/.venv"
SP="$VENV/lib/python3.12/site-packages"
CUDA_DIR="$SP/nvidia/cu13"

if [ ! -x "$CUDA_DIR/bin/nvcc" ]; then
  echo "ERROR: nvcc not found at $CUDA_DIR/bin/nvcc"
  exit 1
fi
echo "Using CUDA toolkit at: $CUDA_DIR"

# (a) sitecustomize.py — runs at interpreter startup for this venv.
cat > "$SP/sitecustomize.py" <<PYEOF
# Auto-loaded at Python startup for this venv.
# Point CUDA_HOME at the pip-provided toolkit (nvidia/cu13) so libraries that
# JIT-compile CUDA kernels (flashinfer, torch extensions) can find nvcc/headers
# under WSL, where there is no system CUDA at /usr/local/cuda.
import os

try:
    _here = os.path.dirname(__file__)
    _cuda = os.path.join(_here, "nvidia", "cu13")
    if os.path.isdir(_cuda) and os.path.isfile(os.path.join(_cuda, "bin", "nvcc")):
        os.environ.setdefault("CUDA_HOME", _cuda)
        os.environ.setdefault("CUDA_PATH", _cuda)
        _bin = os.path.join(_cuda, "bin")
        if _bin not in os.environ.get("PATH", "").split(os.pathsep):
            os.environ["PATH"] = _bin + os.pathsep + os.environ.get("PATH", "")
except Exception:
    pass
PYEOF
echo "wrote $SP/sitecustomize.py"

# (b) activate hook — for interactive shell usage (nvcc on PATH, vllm serve, etc.)
ACT="$VENV/bin/activate"
MARK="# >>> agent_learning cuda env >>>"
if ! grep -qF "$MARK" "$ACT"; then
  {
    echo ""
    echo "$MARK"
    echo "export CUDA_HOME=\"$CUDA_DIR\""
    echo "export CUDA_PATH=\"$CUDA_DIR\""
    echo "export PATH=\"$CUDA_DIR/bin:\$PATH\""
    echo "# <<< agent_learning cuda env <<<"
  } >> "$ACT"
  echo "appended CUDA env block to $ACT"
else
  echo "activate already has CUDA env block"
fi

# Verify nvcc is now resolvable using the exported CUDA_HOME.
export CUDA_HOME="$CUDA_DIR"
export PATH="$CUDA_DIR/bin:$PATH"
echo "nvcc: $(nvcc --version | tail -2 | head -1)"
echo "CUDA_ENV_DONE"
