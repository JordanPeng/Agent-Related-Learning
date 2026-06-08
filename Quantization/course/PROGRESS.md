# Progress — Quantization course

_Last updated: 2026-06-07 (Module 0 seeded by hand) — overall: 0/9 modules formally passed_

## Module status

| # | Module | Status | Last score | Iters | Notes / open blockers |
|---|--------|--------|-----------:|------:|-----------------------|
| 0 | `00_foundations.ipynb` | drafted | — | 0 | Seeded as a reference module; executes clean via nbconvert. Pending formal evaluation on first `/build-course` run. |
| 1 | `01_gptq.ipynb` | not-started | — | 0 | |
| 2 | `02_awq.ipynb` | not-started | — | 0 | |
| 3 | `03_outliers_int8_smoothquant.ipynb` | not-started | — | 0 | |
| 4 | `04_gguf_nf4_qlora.ipynb` | not-started | — | 0 | |
| 5 | `05_rotation_quarot_spinquant.ipynb` | not-started | — | 0 | |
| 6 | `06_fp8_mxfp4_nvfp4.ipynb` | not-started | — | 0 | |
| 7 | `07_extreme_lowbit_kv_bitnet.ipynb` | not-started | — | 0 | |
| 8 | `08_production_and_capstone.ipynb` | not-started | — | 0 | |

_Interview-coverage pass: not-run — will populate `INTERVIEW_QUESTIONS.md` after modules pass._

## Deferred / Out-of-scope ledger
<!-- Decide a topic once; never re-litigate. T3 = going-deeper note only; T4 = excluded. -->

| Topic | Tier | Decision | Reason |
|-------|------|----------|--------|
| QTIP trellis-coded-quantization decoder internals | T3 | going-deeper note only | Beyond L2; conceptual awareness (incoherence + codebooks) is enough. |
| E8-lattice optimality proof (QuIP#) | T3 | going-deeper note only | Proof depth is research-scientist territory. |
| AQLM codebook joint-optimization details | T3 | going-deeper note only | Know the idea (additive multi-codebook); skip the optimizer internals. |
| DeepSeek FP8 FP32-accumulation micro-details | T3 | going-deeper note only | Mention as a depth story; full numerics not required. |
| OmniQuant / HQQ | T3 | going-deeper note only | Useful contrast points; not core for L2. |
| Writing production CUDA/Triton quant kernels | T4 | excluded | Specialist/systems role, not this course. |
| Designing a novel quantization algorithm | T4 | excluded | Research-scientist scope. |
| Non-LLM / vision-CNN quantization specifics | T4 | excluded | Off-topic for LLM post-training. |
| Tensor-Core microarchitecture / RTL | T4 | excluded | Hardware role, not post-training engineer. |

## Evaluation log
<!-- Append one entry per build->eval cycle. Newest first. Blockers are T1/T2 only. -->

### 2026-06-07 — Module 0 — seed — executes clean (not yet rubric-scored)
- Hard gates: exec PASS (nbconvert ran all cells with no errors), correctness pending evaluator review.
- Built by hand as the worked example for the loop. On the first `/build-course` run, the
  orchestrator will dispatch `course-evaluator` to score it against the rubric and revise if needed.
