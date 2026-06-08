---
description: "Research real interview questions for a course topic online and build/refresh a tiered INTERVIEW_QUESTIONS.md bank, reporting only the coverage gaps that matter for the target level. Pass a COURSE_SPEC.md path (or a topic)."
name: "Collect Interview Questions"
argument-hint: "<path to COURSE_SPEC.md or a topic>, e.g. Quantization/course/COURSE_SPEC.md"
agent: interview-question-collector
---

Build or refresh the interview-question bank for: **${input:target}**

If that argument is a `COURSE_SPEC.md` path, use it. If it is a topic name, search for `**/course/COURSE_SPEC.md` under a matching folder. If it is empty, list the candidate specs and ask which one.

Then do your deep-research routine exactly as defined in your instructions:
- Read the spec, rubric (target level + scope tiers), `guide.md`, and the existing notebooks.
- Research real interview questions online from several reputable sources and triangulate.
- Curate, dedupe, tier (T1/T2/T3/T4), and map each question to where the course covers it.
- Write/refresh `<course>/INTERVIEW_QUESTIONS.md`.

Report back the artifact path, counts by tier, and **only the actionable T1/T2 gaps** (with the module each belongs to and a one-line fix). List T3/T4 items separately for the Deferred / Out-of-scope ledger. Finish with the explicit verdict line `INTERVIEW COVERAGE: SUFFICIENT` or `INTERVIEW COVERAGE: GAPS (T1/T2): <n>`. Do not inflate scope — if coverage is sufficient for the target level, say so.
