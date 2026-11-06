---
name: plan-feature
description: Inspects the DocuExtract repository and creates an implementation plan for a new feature, endpoint, refactor, dependency, or architecture change. Use before medium or large coding tasks.
---

# Plan Feature

## Objective
Create an evidence-based implementation plan without changing application source code.

## Procedure
1. Read `AGENTS.md`, the relevant product requirements, architecture, API contract, ADRs, and Definition of Done.
2. Inspect the repository tree, current Git status/diff, dependency configuration, relevant source files, and tests.
3. Trace the existing request/data flow. Search for reusable code before proposing new modules.
4. Separate confirmed facts from assumptions. If a missing detail does not block a safe plan, state a reasonable assumption rather than asking a broad question.
5. Define the user-visible outcome, in-scope work, and explicit non-goals.
6. Identify API/schema/configuration changes and backward-compatibility implications.
7. List ordered implementation steps with the exact modules/files likely to change.
8. Define positive, negative, boundary, and regression tests.
9. Assess security, resource, concurrency, and operational risks.
10. Identify documentation and ADR updates.

## Output
Write or present a plan using `docs/development/implementation-plan-template.md`. For a tracked task, save it under `docs/development/plans/` using a descriptive filename. Do not create the folder unless needed.

End with:
- Recommended implementation sequence.
- Important decisions that require owner approval.
- What will explicitly not be built.

Do not edit application source code during this skill. If the user explicitly requested plan-and-implement in the same task, present the plan first in the interaction and proceed only within that explicit authorization.
