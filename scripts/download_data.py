"""Download the benchmark/eval datasets for the agent-learning workspace.

Usage (from the workspace root, with the venv active):
    python scripts/download_data.py            # download all
    python scripts/download_data.py bfcl ruler # download only the named ones

Each dataset is fetched into:  datasets/<local_folder>/
Re-running is safe and resumable (already-present files are skipped).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Prefer the high-performance Xet transfer backend.
os.environ.setdefault("HF_XET_HIGH_PERFORMANCE", "1")

from huggingface_hub import snapshot_download  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "datasets"

# key -> (repo_id, local_folder)
DATASETS: dict[str, tuple[str, str]] = {
    # 1. Function / tool calling accuracy (BFCL V4)
    "bfcl": ("gorilla-llm/Berkeley-Function-Calling-Leaderboard", "BFCL_Berkeley-Function-Calling-Leaderboard"),
    # 2. Multi-turn user-agent-tool interaction with policies + backend state
    "tau2": ("HuggingFaceH4/tau2-bench-data", "tau2-bench"),
    # 3. Real coding-agent repair
    "swebench": ("princeton-nlp/SWE-bench_Verified", "SWE-bench_Verified"),
    # 4. Long-horizon terminal agents
    "terminalbench": ("ia03/terminal-bench", "Terminal-Bench"),
    # 5. Modern coding ability (contamination-free)
    "livecodebench": ("livecodebench/code_generation_lite", "LiveCodeBench"),
    # 6. Instruction following / format + schema constraints
    "ifeval": ("google/IFEval", "IFEval"),
    # 7. Long-context retrieval / multi-hop reliability
    "ruler": ("simonjegou/ruler", "RULER"),
    # 8. LiveBench (contamination-free, multiple categories -> separate repos)
    "livebench_reasoning": ("livebench/reasoning", "LiveBench/reasoning"),
    "livebench_coding": ("livebench/coding", "LiveBench/coding"),
    "livebench_math": ("livebench/math", "LiveBench/math"),
    "livebench_language": ("livebench/language", "LiveBench/language"),
    "livebench_data_analysis": ("livebench/data_analysis", "LiveBench/data_analysis"),
    "livebench_instruction": ("livebench/instruction_following", "LiveBench/instruction_following"),
    # extra. MMLU-Pro general knowledge/reasoning
    "mmlu_pro": ("TIGER-Lab/MMLU-Pro", "MMLU-Pro"),
}


def main(argv: list[str]) -> int:
    keys = argv or list(DATASETS)
    unknown = [k for k in keys if k not in DATASETS]
    if unknown:
        print(f"Unknown dataset keys: {unknown}\nAvailable: {list(DATASETS)}")
        return 2

    ok, failed = [], []
    for key in keys:
        repo_id, folder = DATASETS[key]
        target = DEST / folder
        print(f"\n=== [{key}] {repo_id} -> datasets/{folder} ===", flush=True)
        try:
            snapshot_download(
                repo_id=repo_id,
                repo_type="dataset",
                local_dir=str(target),
            )
            ok.append(key)
            print(f"    done: {repo_id}", flush=True)
        except Exception as exc:  # keep going; report at the end
            failed.append((key, repo_id, repr(exc)))
            print(f"    FAILED: {repo_id}: {exc}", flush=True)

    print("\n================ SUMMARY ================")
    print(f"OK ({len(ok)}): {ok}")
    if failed:
        print(f"FAILED ({len(failed)}):")
        for key, repo_id, err in failed:
            print(f"  - {key} ({repo_id}): {err}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
