---
name: implement-feature
description: Implements an approved DocuExtract feature plan with focused Python changes, tests, API documentation updates, and verification. Use when the user asks to build or modify a feature.
---

# Implement Feature

## Preconditions
- Read `AGENTS.md` and relevant docs.
- Locate the approved plan or confirm that the user explicitly asked you to implement the described task.
- Inspect Git status/diff and the current implementation. Preserve unrelated user changes.

## Procedure
1. Restate the accepted outcome and scope internally; identify any conflict with current code/docs.
2. Implement one vertical slice at a time. Keep route, schema, service, and parser responsibilities separate.
3. Add or update tests alongside the behavior.
4. Keep dependency additions minimal and explain why they are needed.
5. Handle expected parser/input errors with stable application error types and API mapping.
6. Update API contract, requirements, setup, or ADR documents when behavior or architecture changes.
7. Run targeted tests, the broader test suite when practical, and Ruff checks when configured.
8. Inspect the final diff for accidental formatting, unrelated edits, leaked secrets, and missing tests.

## Stop conditions
Stop and report rather than improvising when:
- The approved plan conflicts with the actual project structure or behavior.
- A breaking API change or architectural expansion is required but was not approved.
- A destructive operation, real credential, external account, or production environment is involved.
- Verification reveals a failure that cannot be safely explained or fixed within scope.

## Handoff
Report implemented files, key design choices, actual test commands/results, limitations, and the shortest way to try the feature. Do not claim unrun checks passed.
