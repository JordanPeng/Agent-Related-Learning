---
description: "Autonomously build or finish a self-study course of Jupyter notebooks until it meets its rubric, via a build -> critique -> revise loop with two subagents. Pass the path to a COURSE_SPEC.md. This is the '/goal'-style autopilot that iterates to the end."
name: "Build Course"
argument-hint: "<path to COURSE_SPEC.md>, e.g. Quantization/course/COURSE_SPEC.md"
agent: course-orchestrator
---

Drive the course whose spec is at: **${input:spec}**

If that argument is empty, search the workspace for `**/course/COURSE_SPEC.md`. If exactly one exists, use it; otherwise list the candidates and ask which to build.

Run the build → critique → revise loop to completion, exactly as defined in your orchestrator instructions:

- Resume from `PROGRESS.md` if it exists; otherwise initialize it from the spec's module list.
- For each module that is not yet `passed`: dispatch `course-builder` to implement or repair it, then dispatch `course-evaluator` (fresh, unbiased, artifact-only) to score it. Record the verdict in `PROGRESS.md`. Repeat until PASS or the per-module iteration cap is hit.
- After all modules pass, run one whole-course evaluation; route any failures back to the relevant module and continue.
- **Final execution gate:** run `python course_kit/run_course.py <course_dir> --inplace` yourself and require **ALL PASS** before declaring done. If any notebook errors, send its first failing cell back to that module's builder and loop again. The course is not finished until this harness is green and `RUN_REPORT.md` shows every notebook clean.
- Keep going autonomously until the course meets the rubric **and** the runner reports ALL PASS, or remaining items are genuinely `blocked`, then print the final report (including the `RUN_REPORT.md` summary).

I will start this and walk away, so run **fully unattended**: do not stop to ask for confirmation between modules or before running build/eval/verify steps. Only surface to me if a module is `blocked` after hitting the iteration cap, or if the spec or rubric is missing.
