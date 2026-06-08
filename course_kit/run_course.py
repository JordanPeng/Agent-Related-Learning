"""Course verification harness — execute every notebook in a course, in order, clean.

This is the single source of truth for the "the whole course runs without errors"
guarantee. It executes each `NN_*.ipynb` from a cold kernel, in numeric order, the way a
learner would run them, and reports per-notebook PASS/FAIL with the first failing cell. It
exits non-zero if any notebook fails, and writes a `RUN_REPORT.md` next to the course.

Used by the course-orchestrator as the final gate (and any time you want to re-check), and
runnable by hand:

    # from the repo root, with the venv active
    python course_kit/run_course.py Quantization/course
    python course_kit/run_course.py Quantization/course --inplace      # also save outputs
    python course_kit/run_course.py Quantization/course --timeout 1200 --kernel python3

By default it does NOT modify the source notebooks (executes them read-only). Pass
`--inplace` to write the executed outputs back so the saved notebooks show their results.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors.execute import CellExecutionError


def find_notebooks(target: Path):
    """Return (notebooks_dir, [notebook paths sorted]). Accepts a course folder or a
    notebooks/ folder directly."""
    nb_dir = target / "notebooks" if (target / "notebooks").is_dir() else target
    nbs = sorted(
        p
        for p in nb_dir.glob("*.ipynb")
        if not p.name.startswith(".") and "checkpoint" not in p.name
    )
    return nb_dir, nbs


def first_error(nb) -> tuple[int, str, str] | None:
    """Find the first code cell that produced an error output."""
    code_idx = -1
    for cell in nb.cells:
        if cell.get("cell_type") != "code":
            continue
        code_idx += 1
        for out in cell.get("outputs", []):
            if out.get("output_type") == "error":
                return code_idx, out.get("ename", ""), out.get("evalue", "")
    return None


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Execute every notebook in a course in order and report pass/fail."
    )
    ap.add_argument(
        "course", help="path to a course folder (containing notebooks/) or a notebooks/ folder"
    )
    ap.add_argument("--timeout", type=int, default=900, help="per-cell timeout in seconds")
    ap.add_argument("--kernel", default="python3", help="Jupyter kernel name")
    ap.add_argument(
        "--inplace",
        action="store_true",
        help="save executed outputs back into the notebooks (default: read-only verify)",
    )
    args = ap.parse_args()

    target = Path(args.course).resolve()
    if not target.exists():
        print(f"Path not found: {target}")
        return 2
    nb_dir, nbs = find_notebooks(target)
    if not nbs:
        print(f"No notebooks found under {nb_dir}")
        return 2

    course_dir = nb_dir.parent if nb_dir.name == "notebooks" else nb_dir
    print(
        f"Running {len(nbs)} notebook(s) in {nb_dir}\n"
        f"  kernel={args.kernel}  timeout={args.timeout}s  "
        f"mode={'inplace' if args.inplace else 'read-only verify'}\n"
    )

    results = []
    for nb_path in nbs:
        t0 = time.time()
        nb = nbformat.read(nb_path, as_version=4)
        ep = ExecutePreprocessor(timeout=args.timeout, kernel_name=args.kernel)
        status, detail = "PASS", ""
        try:
            ep.preprocess(nb, {"metadata": {"path": str(nb_path.parent)}})
        except CellExecutionError:
            status = "FAIL"
            err = first_error(nb)
            detail = (
                f"code cell {err[0]}: {err[1]}: {err[2]}".strip()
                if err
                else "cell execution error"
            )
        except Exception as e:  # kernel start failure, timeout, etc.
            status = "FAIL"
            detail = f"{type(e).__name__}: {e}"
        dt = time.time() - t0
        if status == "PASS" and args.inplace:
            nbformat.write(nb, nb_path)
        results.append((nb_path.name, status, dt, detail))
        line = f"  [{status}] {nb_path.name}  ({dt:.0f}s)"
        if detail:
            line += f"  -> {detail}"
        print(line)

    n_fail = sum(1 for _, s, _, _ in results if s == "FAIL")

    report = course_dir / "RUN_REPORT.md"
    out = [
        "# Course run report",
        "",
        f"_Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}_  ",
        f"Notebooks: {len(results)} | Passed: {len(results) - n_fail} | Failed: {n_fail}",
        "",
        "| # | Notebook | Status | Time (s) | Detail |",
        "|---|----------|--------|---------:|--------|",
    ]
    for i, (name, status, dt, detail) in enumerate(results):
        out.append(f"| {i} | {name} | {status} | {dt:.0f} | {detail} |")
    report.write_text("\n".join(out) + "\n", encoding="utf-8")

    print(
        f"\n{'ALL PASS' if n_fail == 0 else str(n_fail) + ' FAILED'} "
        f"({len(results) - n_fail}/{len(results)} clean) — report: {report}"
    )
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
