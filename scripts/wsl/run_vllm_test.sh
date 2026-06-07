#!/usr/bin/env bash
# Focused vLLM smoke test with clean output (filters vLLM's verbose logging).
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
# shellcheck disable=SC1091
source "$HOME/agent_learning/.venv/bin/activate"

MODEL="${1:-/mnt/f/agent_learning/LLM_model_weights/Qwen3-1.7B}"
echo "Running vLLM smoke test on: $MODEL"
python "$(dirname "$0")/vllm_smoke.py" "$MODEL" 2>/tmp/vllm_full.log
rc=$?
echo "--- key lines ---"
grep -E "Resolved architecture|engine ready|generated [0-9]+ tokens|VLLM_GEN_OK|Error|error|UVA|OutOfMemory|raise " /tmp/vllm_full.log | tail -25 || true
echo "--- generated text ---"
sed -n '/--- output ---/,/VLLM_GEN_OK/p' /tmp/vllm_full.log || true
echo "exit_code=$rc"
if [ $rc -ne 0 ]; then
  echo "=== last 25 lines of full log (for debugging) ==="
  tail -25 /tmp/vllm_full.log
fi
