<!--
PROGRESS template. The orchestrator creates/updates <Topic>/course/PROGRESS.md from this.
It is the resumable state of the build. Statuses: not-started | drafted | passed | blocked.
-->

# Progress — {{TOPIC}}

_Last updated: {{timestamp}} — overall: {{x/N modules passed}}_

## Module status

| # | Module | Status | Last score | Iters | Notes / open blockers |
|---|--------|--------|-----------:|------:|-----------------------|
| 0 | `00_{{slug}}.ipynb` | not-started | — | 0 | |
| 1 | `01_{{slug}}.ipynb` | not-started | — | 0 | |
| ... | ... | ... | ... | ... | |

_Interview-coverage pass: {{not-run | SUFFICIENT | GAPS}} — see `INTERVIEW_QUESTIONS.md`._

## Deferred / Out-of-scope ledger
<!-- Decide a topic once; never re-litigate. T3 = mention/going-deeper only; T4 = excluded. -->

| Topic | Tier | Decision | Reason |
|-------|------|----------|--------|
| {{...}} | T3 | going-deeper note only | {{beyond target level}} |
| {{...}} | T4 | excluded | {{too niche / off-topic / too advanced}} |

## Evaluation log
<!-- Append one entry per build->eval cycle. Newest first. Blockers are T1/T2 only. -->

### {{timestamp}} — Module {{N}} — cycle {{k}} — {{PASS/FAIL}} ({{score}}%)
- Hard gates: exec {{pass/fail}}, correctness {{pass/fail}}
- T1/T2 blockers carried forward:
  1. {{...}}
- Deferred (T3) / out-of-scope (T4) noted this cycle: {{... → added to ledger}}
