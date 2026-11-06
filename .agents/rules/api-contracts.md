---
trigger: glob
globs: "app/api/**/*.py, app/schemas/**/*.py"
description: API versioning, Pydantic schemas, status codes, and stable response/error contracts.
---

# API Contract Rules

- Keep public endpoints under `/api/v1` unless an accepted ADR says otherwise.
- Define explicit Pydantic request/response models for structured payloads.
- Keep success responses and error envelopes consistent with `docs/architecture/api-contract.md`.
- Use correct HTTP status codes; never report a failed extraction as HTTP 200.
- Keep machine-readable error codes stable. Do not expose raw parser exceptions, stack traces, secrets, or absolute paths.
- Update the API contract and tests whenever request/response behavior changes.
- Do not add authentication, persistence, or a new transport protocol without an explicit requirement and design decision.
