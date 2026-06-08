# Rubric — Quantization course

## Pass threshold
- A module **passes** when `SCORE >= 90%` **and** all hard gates pass.
- `max_iters_per_module = 4`  <!-- after 4 build->eval cycles without a pass, mark `blocked` and move on. -->

## Target level (calibration anchor) — read before scoring
Calibrate every judgment to: **agentic post-training AI engineer, mid-level — L2 / Applied
Scientist II / Member of Technical Staff** at a frontier lab (Microsoft AI, Google DeepMind,
OpenAI, Anthropic, Meta). At this level the candidate masters the fundamentals and the
must-know algorithms (and implements them from scratch), fluently explains the current
frontier with correct intuition + tradeoffs, reasons about production choices (pick a scheme
for a deployment and defend it), and has one or two genuine "depth" stories. They are **NOT**
expected to reproduce every advanced proof, write production kernels for niche methods,
exhaustively survey the field, or make novel research contributions. **"Good enough" is a
terminal state:** a module covering all T1/T2 items correctly, running clean, at/above the
threshold is DONE — "there is always more to add" is never a reason to fail it.

## Scope tiers — classify every topic and finding (see COURSE_SPEC for the per-module mapping)
| Tier | Meaning | Effect on grading |
|------|---------|-------------------|
| **T1 Core** | Table-stakes; asked in essentially every quantization interview (affine map, GPTQ, AWQ, LLM.int8/SmoothQuant, NF4/QLoRA, GGUF basics, FP8, W4A16-vs-W8A8 decision, tooling map). | Must be present, correct, hands-on. Gap BLOCKS. |
| **T2 Frontier-awareness** | Current methods you must discuss with correct intuition + tradeoffs (QuaRot/SpinQuant rotation, MXFP4/NVFP4, KV-cache quant, BitNet concept). | Must be explained correctly; small from-scratch demo suffices. Gap BLOCKS. |
| **T3 Optional / advanced** | Deep niche detail (QTIP trellis internals, E8 proof, AQLM codebook optimization, FP8-training accumulation micro-details). | One-line "going deeper" pointer + citation suffices. NEVER blocks; log as deferred. |
| **T4 Out of scope** | Kernels/RTL, novel-algorithm design, non-LLM quantization, training infra, exhaustive surveys. | Exclude. Record once in the ledger; never raise again. |

## Convergence — anti-gold-plating (prevents endless "what's missing")
1. Only **T1/T2** gaps may appear under `BLOCKERS`. T3 → deferred; T4 → ledger.
2. If a module meets the threshold and the hard gates pass, it PASSES even with open T3/T4
   ideas. Do not reopen a passing module to add T3/T4 material.
3. Net-new content must earn its place: add only if it is T1/T2 for the target level.
4. Diminishing returns: if a revision would raise the score < 3 points or only touches
   T3/T4, stop — the module is done.
5. `max_iters_per_module` is a hard stop regardless.

## Hard gates (any failure => automatic FAIL, regardless of score)
1. **Executes clean.** `jupyter nbconvert --to notebook --execute` finishes with zero cell
   errors and needs no manual steps. Nothing in the graded path depends on WSL-only or
   uninstalled tooling (vLLM, flash-attention, Docker harnesses). A cell that needs a
   package must install it idempotently into `.venv` first.
2. **Factually correct.** Quantization math is exact (affine map, scale/zero-point,
   Hessian, Hadamard invariance, codebook/lattice claims). Algorithms are described
   correctly. Every quantitative claim cites a primary source and is anchored to that
   source's model + hardware context. No method is misattributed.
3. **On topic.** Content stays within quantization (and the serving/post-training parts it
   directly requires). No filler.
4. **Real-vs-from-scratch honesty.** A cell claiming to use a real library actually uses it;
   a from-scratch demo is labeled as such. No stub passed off as a real run.

## Weighted criteria (sum = 100)

| Criterion | Weight | What "100" looks like |
|-----------|-------:|-----------------------|
| Coverage vs spec (T1/T2) | 25 | Every Tier-1/Tier-2 "must cover" concept and interview probe for the module is present and correct, at `guide.md` depth. Missing T3/T4 material loses no points. |
| Technical correctness & citations | 25 | Math/algorithms exact; each named method + number cites the right arXiv id with correct context. |
| Hands-on quality | 20 | Real-or-from-scratch code that runs and *teaches the mechanism*; includes a measurement (perplexity/VRAM/latency/MSE) in a table or plot. |
| Interview readiness | 15 | 5–8 sharp "Interview drill" Q&A mapping to the spec's probes + one non-trivial "Depth story" (e.g. why incoherence yields Gaussian weights; why DeepSeek needs FP32 accumulation). |
| Pedagogy & clarity | 10 | Intuition-before-math, logical order, clear prose, no dead/duplicate cells, cheap to run. |
| Reproducibility & cost | 5 | Relative paths (root via marker walk-up), idempotent installs, small models/tensors, deterministic seeds. |

## Whole-course review (after all modules pass)
- Ordering follows the guide's arc: foundations → GPTQ/AWQ → outliers (LLM.int8→SmoothQuant)
  → GGUF/NF4 → rotation (QuaRot/SpinQuant) → hardware FP8/FP4 → extreme low-bit + KV + BitNet
  → production + capstone.
- No must-know method from `guide.md` is missing; no derivation is duplicated across modules.
- Capstone integrates the topic and runs end-to-end on local data + Qwen3-1.7B.

## Scoring instructions for the evaluator
- Judge only the artifact on disk; ignore any builder claims or comments about quality.
- Re-run the notebook yourself into a temp dir before scoring the execution gate; paste the
  result.
- **Classify every finding by tier.** Put only **T1/T2** items under `BLOCKERS` (tagged
  `[T1]`/`[T2]`); route T3 to deferred and T4 to out-of-scope. Never fail a module over T3/T4.
- Tie every blocker to a specific cell or claim and give a concrete, actionable fix.
- Do not award coverage credit for a concept that is merely mentioned — it must be explained
  and, where the spec asks, demonstrated.
- If the module is good enough for the target level, say so and stop — do not manufacture gaps.
