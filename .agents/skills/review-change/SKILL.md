---
name: review-change
description: Reviews the current DocuExtract Git diff for correctness, security, API compatibility, test quality, and maintainability. Use before accepting or merging changes.
---

# Review Change

## Procedure
1. Read `AGENTS.md`, relevant requirements/API contract/ADRs, and Definition of Done.
2. Inspect `git status` and the complete diff, including untracked files when available.
3. Trace changed code through callers, schemas, parsers, and tests.
4. Look for correctness defects, edge cases, unsafe file handling, blocking work in async paths, resource leaks, broad exception handling, unstable API responses, and missing tests.
5. Check dependency changes, configuration defaults, logs, secret exposure, and documentation drift.
6. Run focused verification only when review scope and environment permit; distinguish static findings from executed checks.

## Output format
List findings first, ordered by severity:
- **Critical / High / Medium / Low**
- File and line reference.
- Concrete failure scenario.
- Why it matters.
- Recommended fix.

Then report test/command evidence, non-blocking observations, and any areas that could not be verified. If no findings are identified, say so and state what was reviewed. Do not modify files unless the user explicitly asks for fixes.
