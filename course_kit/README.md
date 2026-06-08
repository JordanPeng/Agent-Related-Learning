# course_kit — a reusable multi-agent system for building your own courses

This folder turns Copilot into a **multi-agent course factory**. You point it at a topic,
and it autonomously writes a set of interview-grade Jupyter notebooks, critiques them
without bias, researches what real interviews ask, revises them, and repeats until they meet
a rubric — then **stops** (it is built to converge, not gold-plate).

It was built first for **Quantization**, but the pattern is topic-agnostic: reuse it for
KV Caching, Speculative Decoding, or anything else.

## The idea

Three specialized subagents play different roles; one orchestrator drives the loop:

```
/build-course <spec>            <- your "/goal" autopilot command
        |
        v
  course-orchestrator           reads spec + rubric + progress, runs the loop, never writes content
   |          |          \
   | build     | score      \ research real interview Qs (web)
   v           v             v
course-builder course-evaluator  interview-question-collector
 edits + RUNS   read-only judge;   deep web research; builds a
 the notebook   re-runs the nb +   tiered INTERVIEW_QUESTIONS.md;
                web-verifies facts; flags only the gaps that matter
                PASS/FAIL + fixes
```

**Why separate agents?** The evaluator is a *fresh subagent* that only sees the spec, the
rubric, and the notebook files on disk — never the builder's reasoning or its claims of
success. That context isolation is what makes the critique honest. The evaluator
*independently re-executes* each notebook (via `jupyter nbconvert --execute` into a temp dir)
and can **search the web** to verify facts/citations, so "it runs perfectly" and "the numbers
are right" are verified, not asserted. The orchestrator loops build → critique → revise until
the rubric passes, with a per-module iteration cap so it can never spin forever.

## Staying "good enough" (the convergence control)

If you keep asking "what's missing?", something always is — so the system is explicitly
bounded by a **target level** and a **4-tier scope model** defined in each `RUBRIC.md`:

| Tier | Meaning | Effect |
|------|---------|--------|
| **T1 Core** | Asked in essentially every interview | Must be present + correct + hands-on; a gap **blocks** |
| **T2 Frontier-awareness** | Current methods you must discuss fluently | Must be explained (small demo ok); a gap **blocks** |
| **T3 Optional/advanced** | Deep niche detail beyond the level | One-line "going deeper" pointer; **never blocks** (deferred) |
| **T4 Out of scope** | Too advanced/minor/off-topic | Excluded once in a ledger; **never raised again** |

Only **T1/T2** gaps can fail a module. T3/T4 findings go to a **Deferred / Out-of-scope
ledger** in `PROGRESS.md` (decided once, never re-litigated). A passing module is not
reopened to add nice-to-haves, and a revision that would only add T3/T4 or move the score
< 3 points is skipped. The default target level is **mid-level / L2 / Applied Scientist II**
at a frontier lab — edit it in the rubric to recalibrate.

## Files in the system

| File | Role |
|------|------|
| `.github/agents/course-orchestrator.agent.md` | Drives the loop; dispatches the others; maintains `PROGRESS.md` + the ledger. |
| `.github/agents/course-builder.agent.md` | Implements/repairs one module to the target level; runs the notebook to verify it. |
| `.github/agents/course-evaluator.agent.md` | Unbiased, read-only scorer; re-runs the notebook; web-verifies facts; PASS/FAIL + tiered fixes. |
| `.github/agents/interview-question-collector.agent.md` | Deep web research; builds `INTERVIEW_QUESTIONS.md`; reports only T1/T2 coverage gaps. |
| `.github/prompts/build-course.prompt.md` | `/build-course` — the autopilot entry point. |
| `.github/prompts/new-course.prompt.md` | `/new-course` — scaffolds a new topic from the templates below. |
| `.github/prompts/collect-interview-questions.prompt.md` | `/collect-interview-questions` — run the research pass on demand. |
| `.github/instructions/course-notebooks.instructions.md` | Always-on quality bar for anything under a `course/` folder. |
| `course_kit/templates/*` | Spec / rubric / progress templates (incl. tiers + ledger) used to start a new topic. |

## How a course is organized

Each topic gets a `course/` folder next to its study notes:

```
<Topic>/
  guide.md                  # (optional) your research notes — the content source of truth
  course/
    COURSE_SPEC.md          # what to build: modules, objectives, capstone, definition of done
    RUBRIC.md               # how it's judged: target level, scope tiers, weighted criteria, hard gates
    PROGRESS.md             # live state: per-module status + deferred ledger + evaluation log (resumable)
    INTERVIEW_QUESTIONS.md  # tiered, sourced question bank (written by the collector)
    notebooks/
      00_*.ipynb            # the modules the builder produces
      01_*.ipynb
      ...
```

## Use it

### Build (or finish) a course
```
/build-course Quantization/course/COURSE_SPEC.md
```
The orchestrator resumes from `PROGRESS.md`, so you can stop and re-run `/build-course`
any time and it picks up where it left off. It only pauses for you if a module is
`blocked` after hitting the iteration cap, or if the spec/rubric is missing.

### Start a brand-new topic
```
/new-course KV Caching
```
This scaffolds `KV_Caching/course/COURSE_SPEC.md`, `RUBRIC.md`, and `PROGRESS.md` from the
templates (seeding the module list from a `guide.md` if one exists). Review/edit the spec,
then run `/build-course KV_Caching/course/COURSE_SPEC.md`.

### Research interview questions on demand
```
/collect-interview-questions Quantization/course/COURSE_SPEC.md
```
Runs the `interview-question-collector` to deep-research real interview questions online,
build/refresh `INTERVIEW_QUESTIONS.md`, and report only the **T1/T2** coverage gaps that
matter for the target level. The orchestrator also runs this automatically once near the end
of `/build-course`; use the prompt when you want a standalone research sweep.

## Tips

- **New agents/prompts not showing up?** Reload the VS Code window
  (`Developer: Reload Window`) so it re-scans `.github/agents` and `.github/prompts`.
- **Less bias / fewer blind spots:** give the evaluator a *different* model than the
  builder (set `model:` in each agent's frontmatter). Disagreement between two models is a
  useful signal.
- **Recalibrate the level** by editing the rubric's **Target level** + **Scope tiers**: move a
  topic between T1/T2/T3/T4 to make the agents build more or less of it. Aiming at a senior
  role? Promote some T3 items to T2.
- **Tighten the bar** by editing `RUBRIC.md` (weights, pass threshold, hard gates,
  `max_iters_per_module`, convergence rules). The agents read it every cycle — no code changes.
- **It won't over-build:** only T1/T2 gaps block, passing modules aren't reopened for
  nice-to-haves, and excluded topics are logged in the `PROGRESS.md` ledger so they stay
  decided. To force more depth, promote the topic's tier rather than asking "what's missing".
- **Keep notebooks runnable:** everything must execute on the Windows `.venv`. WSL-only
  tools (vLLM, flash-attention) belong in optional appendices, not in the graded path.

## Guaranteeing "everything runs" + unattended runs

The system is designed so you can start it, walk away, and return to a course where **every
notebook executes top-to-bottom without errors, in order, from a cold kernel** — verified,
not claimed:

- The **builder** executes and debugs each notebook until clean; the **evaluator**
  independently re-runs it (execution is a hard gate); and the **orchestrator** runs a final
  full-suite check before declaring done.
- That final check is the verification harness, which you can also run yourself any time:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  python course_kit\run_course.py Quantization\course            # read-only verify
  python course_kit\run_course.py Quantization\course --inplace  # also save outputs
  ```
  It runs every `notebooks/NN_*.ipynb` in order, prints PASS/FAIL per notebook with the first
  failing cell, writes **`RUN_REPORT.md`** next to the course, and exits non-zero if anything
  fails. When you come back, open `RUN_REPORT.md` (and `PROGRESS.md`) to see the result.

**To truly leave it running unattended**, configure VS Code so the agent doesn't stall
waiting for you (these are the usual blockers for a long autopilot run):
- **Auto-approve tools/terminal** so it doesn't pause on each command — e.g. enable
  `chat.tools.autoApprove` (and/or an allowlist via `chat.tools.terminal.autoApprove`).
  This trades away per-command safety prompts, so only do it for a workspace you trust.
- **Raise the per-turn tool-call cap** so it doesn't pause to ask "continue?": increase
  `chat.agent.maxRequests` (e.g. to a few hundred) — a full course is many build/eval/verify
  steps.
- Make sure the `.venv` kernel is the one in use and models in `LLM_model_weights/` are
  present, so no cell blocks on a download or a kernel picker.
