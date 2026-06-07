"""Verify every downloaded dataset actually loads and report real row counts.

    python scripts/verify_data.py

For each dataset under datasets/, load it with the `datasets` library and print
splits + row counts, confirming the download is complete and usable rather than
guessing from folder size. A few datasets need special handling:
  - RULER is multi-config (4096 / 8192 / 16384 context lengths).
  - BFCL and tau2-bench are collections of per-task JSON files with *different*
    schemas, so they are validated file-by-file rather than merged into one table.
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

from datasets import get_dataset_config_names, load_dataset  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DS = ROOT / "datasets"

GREEN, RED, RST = "\033[92m", "\033[91m", "\033[0m"

# Datasets loadable directly with the HF folder loader (single schema).
HF_SIMPLE = [
    "IFEval",
    "SWE-bench_Verified",
    "Terminal-Bench",
    "LiveCodeBench",
    "MMLU-Pro",
    "LiveBench/reasoning",
    "LiveBench/coding",
    "LiveBench/math",
    "LiveBench/language",
    "LiveBench/data_analysis",
    "LiveBench/instruction_following",
]


def check_simple(name: str) -> tuple[bool, str]:
    folder = DS / name
    if not folder.exists():
        return False, "folder missing"
    d = load_dataset(str(folder))
    parts = ", ".join(f"{k}={v.num_rows}" for k, v in d.items())
    total = sum(v.num_rows for v in d.values())
    return True, f"splits[{parts}] total={total}"


def check_ruler() -> tuple[bool, str]:
    """RULER ships multiple context-length configs (4096/8192/16384)."""
    folder = DS / "RULER"
    if not folder.exists():
        return False, "folder missing"
    cfgs = get_dataset_config_names(str(folder))
    bits, grand = [], 0
    for cfg in cfgs:
        d = load_dataset(str(folder), cfg)
        n = sum(v.num_rows for v in d.values())
        grand += n
        bits.append(f"{cfg}={n}")
    return True, f"configs[{', '.join(bits)}] total={grand}"


def check_json_collection(name: str) -> tuple[bool, str]:
    """Validate every *.json file parses; report file + total record counts.

    BFCL and tau2-bench are collections of per-task files with different
    schemas, so they cannot be merged into a single table — we instead confirm
    every file is present and parseable.
    """
    folder = DS / name
    if not folder.exists():
        return False, "folder missing"
    files = [p for p in folder.rglob("*.json") if ".cache" not in p.parts]
    if not files:
        return False, "no .json files found"
    total_records, bad = 0, []
    for f in files:
        try:
            with open(f, encoding="utf-8") as fh:
                first = fh.read(1)
                fh.seek(0)
                if first == "[":  # json array
                    total_records += len(json.load(fh))
                else:  # jsonl
                    total_records += sum(1 for line in fh if line.strip())
        except Exception as e:  # noqa: BLE001
            bad.append(f"{f.name}: {type(e).__name__}")
    if bad:
        return False, f"{len(files)} files, {len(bad)} unreadable: {bad[:3]}"
    return True, f"{len(files)} task files parsed, {total_records} total records"


def main() -> int:
    print(f"Verifying datasets under {DS}\n")
    results: list[tuple[str, bool, str]] = []

    for name in HF_SIMPLE:
        try:
            ok, msg = check_simple(name)
        except Exception as e:  # noqa: BLE001
            ok, msg = False, f"{type(e).__name__}: {str(e)[:100]}"
        results.append((name, ok, msg))

    specials = [
        ("RULER", check_ruler),
        ("BFCL_Berkeley-Function-Calling-Leaderboard",
         lambda: check_json_collection("BFCL_Berkeley-Function-Calling-Leaderboard")),
        ("tau2-bench", lambda: check_json_collection("tau2-bench")),
    ]
    for name, fn in specials:
        try:
            ok, msg = fn()
        except Exception as e:  # noqa: BLE001
            ok, msg = False, f"{type(e).__name__}: {str(e)[:100]}"
        results.append((name, ok, msg))

    ok = bad = 0
    for name, good, msg in sorted(results):
        if good:
            print(f"{GREEN}OK{RST}      {name:46s} {msg}")
            ok += 1
        else:
            print(f"{RED}FAIL{RST}    {name:46s} {msg}")
            bad += 1

    print(f"\n{'='*60}")
    color = GREEN if bad == 0 else RED
    print(f"{color}{ok} ok, {bad} failed{RST}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
