# Definition of Done

A feature is done only when the applicable items below are satisfied.

## Requirements
- [ ] User story/problem and acceptance criteria are clear.
- [ ] Scope and non-goals are explicit.
- [ ] Existing behavior and relevant code were inspected.

## Implementation
- [ ] Change follows the approved plan.
- [ ] Route handlers remain thin; parsing logic is outside HTTP routes.
- [ ] Types and Pydantic schemas are used at service/API boundaries.
- [ ] No speculative dependencies or unrelated refactors were added.
- [ ] Error cases are intentional and machine-readable.

## Security
- [ ] Upload size and supported content are validated.
- [ ] Client filename/MIME type is not blindly trusted.
- [ ] No secrets or document contents are written to logs.
- [ ] No internal stack trace/path is exposed to clients.
- [ ] Temporary files/resources are cleaned up if used.

## Tests and verification
- [ ] Unit tests cover changed processing logic.
- [ ] API tests cover relevant status codes and response schemas.
- [ ] Edge and failure cases are covered.
- [ ] Relevant pytest command passes.
- [ ] Ruff lint/format checks pass when configured.
- [ ] Any test not run is explicitly disclosed.

## Documentation
- [ ] API contract and OpenAPI behavior agree.
- [ ] Setup/configuration docs are updated when needed.
- [ ] Roadmap/requirements/ADR are updated if scope or architecture changed.
- [ ] A learning/dev log is added when the change introduces an important concept.

## Final handoff
- [ ] Summary names changed files and behavior.
- [ ] Test commands and actual outcomes are reported.
- [ ] Limitations and remaining risks are disclosed.
- [ ] The owner can run or verify the feature using the instructions provided.
