---
description: "Quality bar for self-study course notebooks and specs: must run top-to-bottom on the local venv, be interview-grade, and cite primary sources."
applyTo: "**/course/**"
---

# Course content standards

These apply to any file under a `course/` folder (specs, rubrics, and notebooks).

- **Notebooks must execute top-to-bottom** on the local `.venv` kernel (`Python (agent_learning, RTX5090)`) with no errors and no manual steps. Verify with `jupyter nbconvert --to notebook --execute`, or the whole course at once with `python course_kit/run_course.py <course_dir>` (must report ALL PASS).
- **Target environment:** Windows + RTX 5090 (Blackwell). Do not depend on vLLM, flash-attention, or Docker-based harnesses in notebooks — those are WSL-only. Use them only in clearly-marked optional appendices that are skipped by default.
- **Real when possible, from-scratch when not.** Prefer real libraries (transformers, bitsandbytes, optimum, GPTQModel, llama.cpp / gguf) when they install cleanly here; otherwise implement the mechanism from scratch in PyTorch on a small tensor/model. Never leave a failing cell, or a stub mislabeled as a real run.
- **Cite primary sources.** Every quantitative claim or named method cites its arXiv id (or official doc), with numbers anchored to the source's context (model + hardware).
- **Keep demos cheap.** Prefer Qwen3-1.7B and small tensors; guard heavy/optional cells behind flags; make package installs idempotent (`%pip install` with a skip-if-present check).
- **Interview framing.** Each module ends with an "Interview drill" (Q&A) and one "Depth story". Content depth targets the interview role named in the spec.
- **Paths are relative.** Locate the workspace root by walking up for `LLM_model_weights` / `.venv`; never hardcode machine-specific absolute paths.
