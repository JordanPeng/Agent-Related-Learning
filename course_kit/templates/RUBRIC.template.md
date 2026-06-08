<!--
RUBRIC template. Copy to <Topic>/course/RUBRIC.md and tune the weights/threshold.
The evaluator reads this literally every cycle: criteria + weights + gates + threshold.
-->

# Rubric — {{TOPIC}}

## Pass threshold
- A module **passes** when `SCORE >= {{90}}%` **and** all hard gates pass.
- `max_iters_per_module = {{4}}`  <!-- orchestrator stops revising a module after this many build->eval cycles and marks it `blocked`. -->

## Target level (calibration anchor) — read before scoring
Calibrate every judgment to: **{{target role}}, {{e.g. mid-level / L2 / Applied Scientist II}}**
at a frontier lab ({{labs}}). At this level the candidate is expected to master fundamentals
and the must-know methods (and implement them from scratch), fluently explain the current
frontier with correct intuition + tradeoffs, reason about production choices, and have one or
two genuine "depth" stories. They are **NOT** expected to reproduce every advanced proof,
write production kernels for niche methods, exhaustively survey the field, or make novel
research contributions. **"Good enough" is a real, terminal state:** a module that covers all
T1/T2 items correctly, runs clean, and hits the threshold is DONE. "There is always more to
add" is never a reason to fail it.

## Scope tiers — classify every topic and every finding
| Tier | Meaning | Effect on grading |
|------|---------|-------------------|
| **T1 Core** | Table-stakes; asked in essentially every interview. | Must be present, correct, hands-on. A gap here BLOCKS (fail). |
| **T2 Frontier-awareness** | Current methods you must discuss with correct intuition + tradeoffs. | Must be explained correctly; a small from-scratch demo suffices. A gap here BLOCKS (fail). |
| **T3 Optional / advanced** | Deep niche detail beyond the level (proofs, kernel internals, exhaustive variants). | A one-line "going deeper" pointer + citation suffices. NEVER blocks; log as deferred. |
| **T4 Out of scope** | Too advanced, too minor, or off-topic for this course/level. | Exclude. Record once in the ledger with a reason; never raise again. |

## Convergence — anti-gold-plating (prevents endless "what's missing")
1. Only **T1/T2** gaps may appear under `BLOCKERS`. T3 → deferred "nice-to-have"; T4 → ledger.
2. If a module meets the score threshold and the hard gates pass, it PASSES even with open
   T3/T4 ideas. Do not reopen a passing module to add T3/T4 material.
3. Net-new content must earn its place: add only if it is T1/T2 for the target level.
4. Diminishing returns: if a revision would raise the score by < 3 points or only touches
   T3/T4, stop — the module is done.
5. `max_iters_per_module` is a hard stop regardless.

## Hard gates (any failure => automatic FAIL, regardless of score)
1. **Executes clean.** `jupyter nbconvert --to notebook --execute` completes with zero cell
   errors and no manual steps. No dependence on WSL-only / uninstalled tooling in the
   graded path.
2. **Factually correct.** No wrong formulas, no misdescribed algorithms, no uncited or
   misattributed quantitative claims. Numbers anchored to their source's context.
3. **On topic.** Content stays within {{TOPIC}}; no filler from adjacent areas.

## Weighted criteria
<!-- Weights must sum to 100. Each scored 0–100; SCORE = weighted average. -->

| Criterion | Weight | What "100" looks like |
|-----------|-------:|-----------------------|
| Coverage vs spec (T1/T2) | {{25}} | Every Tier-1/Tier-2 "must cover" concept + interview probe for the module is present and correct. Missing T3/T4 material loses no points. |
| Technical correctness & citations | {{25}} | Math/algorithms exact; every claim cites a primary source with correct context. |
| Hands-on quality | {{20}} | Real-or-from-scratch code that runs; a measurement (perplexity/VRAM/latency/MSE) shown in a table/plot. |
| Interview readiness | {{15}} | Strong "Interview drill" Q&A + one non-trivial "Depth story" at the role's depth. |
| Pedagogy & clarity | {{10}} | Logical order, clear prose, intuition-before-math, no dead/duplicate cells. |
| Reproducibility & cost | {{5}} | Relative paths, idempotent installs, cheap to run, deterministic where it matters. |

## Whole-course review (after all modules pass)
- Correct ordering and smooth difficulty ramp; later modules build on earlier ones.
- No gaps vs the source of truth and no duplicated explanations across modules.
- Capstone genuinely integrates the topic and runs end-to-end.

## Scoring instructions for the evaluator
- Judge only the artifact on disk; ignore any claims about it.
- Re-run the notebook yourself into a temp dir before scoring the execution gate.
- **Classify every finding by tier.** Put only **T1/T2** items under `BLOCKERS`; route T3 to
  deferred and T4 to out-of-scope. Do not fail a module over T3/T4.
- Be specific: tie every blocker to a cell or claim, tag it `[T1]`/`[T2]`, and give a
  concrete fix.
- If the module is good enough for the target level, say so and stop — do not invent gaps.
