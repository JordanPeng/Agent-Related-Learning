#!/usr/bin/env bash
# Quick check: which of our local models' architectures does this vLLM support?
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
VENV="$HOME/agent_learning/.venv"
# shellcheck disable=SC1091
source "$VENV/bin/activate"

python - <<'PY'
import json, os
from vllm import __version__ as vv
print("vllm:", vv)

try:
    from vllm.model_executor.models.registry import ModelRegistry
    supported = set(ModelRegistry.get_supported_archs())
except Exception as e:
    print("could not introspect registry:", e)
    supported = set()

for name, path in {
    "Qwen3-14B": "/mnt/f/agent_learning/LLM_model_weights/Qwen3-14B",
    "gemma-4-12B-it": "/mnt/f/agent_learning/LLM_model_weights/gemma-4-12B-it",
}.items():
    cfg = json.load(open(os.path.join(path, "config.json")))
    archs = cfg.get("architectures", [])
    ok = any(a in supported for a in archs)
    print(f"{name:16s} architectures={archs} supported={ok}")

# print a few gemma/qwen-related supported archs for context
rel = sorted(a for a in supported if "Gemma" in a or "Qwen" in a)
print("related supported archs:", rel)
PY
