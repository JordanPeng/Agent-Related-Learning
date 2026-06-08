<!--
COURSE_SPEC template. Copy to <Topic>/course/COURSE_SPEC.md and fill every {{...}}.
This file answers: WHAT to build. The RUBRIC answers HOW it is judged.
Keep it concrete — the builder and evaluator read it literally.
-->

# Course spec — {{TOPIC}}

## Target outcome
A learner who completes this course can {{what they can do}}, and is ready to be
interviewed as a **{{target role, e.g. agentic post-training AI engineer}}** on this topic.
Scope is limited strictly to **{{TOPIC}}** — do not drift into adjacent topics.

## Scope & leveling (defines "good enough" so the build converges)
- **Target level:** {{e.g. mid-level / L2 / Applied Scientist II / Member of Technical Staff}}
  at a frontier lab ({{e.g. Microsoft AI, Google DeepMind, OpenAI, Anthropic, Meta}}). The
  course must be *sufficient to interview at this level*, not exhaustive. The full tier
  definitions and convergence rules live in `RUBRIC.md`.
- **In scope (T1 Core + T2 Frontier-awareness):** {{the must-master fundamentals + the
  current frontier you must discuss fluently}}.
- **Optional / advanced (T3 — mention only):** {{deep niche detail, proofs, kernel internals
  — a one-line "going deeper" pointer is enough; do not implement}}.
- **Intentionally out of scope (T4 — excluded on purpose):** {{too-advanced or too-minor or
  off-topic items, each with a one-line reason}}. These are decided once and not revisited.

## Source of truth
- Primary content source: {{path to guide.md / notes, e.g. Quantization/guide.md}}
- Treat that file's claims and citations as the canonical outline and depth target.

## Environment contract
- Notebooks live in `{{Topic}}/course/notebooks/` and MUST run top-to-bottom on the
  Windows `.venv` kernel (RTX 5090 / Blackwell, PyTorch 2.11 + CUDA 12.8).
- Real libraries preferred; from-scratch PyTorch demos where tooling can't run here.
- WSL-only tools (vLLM, flash-attention, Docker harnesses) → optional appendix only.

## Pedagogical rules (every module)
- Learning objectives up top; prerequisites named.
- Intuition first, then the math (KaTeX), then code (real or from-scratch), then a
  measurement (a number/table/plot), then an "Interview drill" Q&A, then one "Depth story".
- Every named method / number cites a primary source (arXiv id or official doc).
- Demos stay cheap (small models/tensors; guard heavy cells behind a flag).

## Modules
<!-- 6–10 rows. NN is the notebook number. "Must cover" = the non-negotiable concepts and
     interview probes for that module. "Hands-on" = what the learner actually runs. -->

| # | Notebook | Must cover (concepts + interview probes) | Hands-on (runs on this machine) |
|---|----------|------------------------------------------|---------------------------------|
| 0 | `00_{{slug}}.ipynb` | {{...}} | {{...}} |
| 1 | `01_{{slug}}.ipynb` | {{...}} | {{...}} |
| ... | ... | ... | ... |

## Capstone
{{A final applied notebook that ties the topic together and proves end-to-end competence.
e.g. apply the technique to a real local model and measure the quality/cost tradeoff.}}

## Definition of done
- Every module and the capstone reach `passed` under `RUBRIC.md`.
- The whole-course review passes: correct ordering, no gaps vs the source of truth, no
  duplicated content, and a learner could self-study it front to back.
- A short `README.md` in `notebooks/` lists the modules and how to run them (the builder
  creates this in the final pass).
