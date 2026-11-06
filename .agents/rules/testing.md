---
trigger: model_decision
description: Apply when adding or changing tests, parser behavior, API endpoints, error handling, or CI verification.
---

# Testing Rules

- Test pure normalization and parser behavior independently from HTTP routes where practical.
- For endpoints, cover success, invalid input, unsupported format, oversize upload, malformed/encrypted input, and unexpected failure mapping as relevant.
- Use small deterministic fixtures; do not commit private or real user documents.
- Assert response schema, status code, and stable error code—not only that a request did not crash.
- Run the most relevant test first, then the broader suite when practical.
- Run Ruff lint and format checks when configured.
- Report exact commands and results. State clearly when a check was not run.
- Never delete/skip/loosen a test solely to obtain a green build.
