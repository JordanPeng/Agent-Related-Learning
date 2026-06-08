---
description: "Scaffold a new self-study course for a topic. Creates <Topic>/course/COURSE_SPEC.md, RUBRIC.md, and PROGRESS.md from the course_kit templates so you can edit the spec and then run /build-course."
name: "New Course"
argument-hint: "<Topic name>, e.g. 'KV Caching' or 'Speculative Decoding'"
agent: agent
---

Scaffold a new course for the topic: **${input:topic}**

Steps:
1. **Pick the target folder.** If the topic maps to an existing top-level study folder (e.g. `KV_Caching`, `Speculative_Decoding`, `Quantization`), use it. Otherwise create a new folder named after the topic.
2. **Read the templates** in [course_kit/templates](../../course_kit/templates): `COURSE_SPEC.template.md`, `RUBRIC.template.md`, `PROGRESS.template.md`.
3. **Create** `<folder>/course/COURSE_SPEC.md`, `RUBRIC.md`, and `PROGRESS.md` by filling the templates for this topic:
   - Draft a 6–10 module outline from any `guide.md` / study notes already in the topic folder. If none exist, propose a sensible interview-focused outline and flag it for my review.
   - Set the target role / interview framing, the pass threshold, the hard gates, and the per-module iteration cap.
   - Mark every module `not-started` in `PROGRESS.md`.
4. **Do not build notebooks.** Print the proposed module list and the three file paths, then tell me to review and edit `COURSE_SPEC.md` and run `/build-course <folder>/course/COURSE_SPEC.md` when ready.
