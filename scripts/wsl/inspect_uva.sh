#!/usr/bin/env bash
# Inspect vLLM's UVA check and probe whether UVA is reported by torch.
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
# shellcheck disable=SC1091
source "$HOME/agent_learning/.venv/bin/activate"

BU="$HOME/agent_learning/.venv/lib/python3.12/site-packages/vllm/v1/worker/gpu/buffer_utils.py"
echo "=== buffer_utils.py lines 1-60 ==="
sed -n '1,60p' "$BU"

echo
echo "=== grep UVA detection / env flags ==="
grep -rn "UVA\|unified\|VLLM_.*UVA\|is not available" "$BU" || true

echo
echo "=== torch UVA / device attribute probe ==="
python - <<'PY'
import torch
print("torch", torch.__version__, "cuda", torch.version.cuda)
print("cuda available:", torch.cuda.is_available())
try:
    # try a pinned tensor (UVA-ish)
    t = torch.empty(16, pin_memory=True)
    print("pin_memory alloc: OK")
except Exception as e:
    print("pin_memory alloc FAILED:", type(e).__name__, e)
PY

echo
echo "=== vLLM env flags mentioning UVA/V2/MODEL_RUNNER ==="
python - <<'PY'
try:
    import vllm.envs as e
    names = [n for n in dir(e) if any(k in n for k in ("UVA","V2","RUNNER","PIN","WSL"))]
    print("candidate env flags:", names)
except Exception as ex:
    print("could not import vllm.envs:", ex)
PY
echo "INSPECT_DONE"
