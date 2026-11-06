---
trigger: glob
globs: "**/*.py, **/*_test.py"
description: Python style, typing, FastAPI implementation, and maintainability conventions.
---

# Python Conventions

- Follow the repository's Python version and package manager; do not silently change either.
- Use type hints for public functions and module boundaries. Prefer explicit return types.
- Use Pydantic models for structured API input/output; keep parser internals independent of FastAPI.
- Use `async def` only when awaiting async I/O or async dependencies. Do not treat CPU-bound parsing as asynchronous automatically.
- Keep functions focused and side effects visible. Avoid mutable module globals and import-time work.
- Catch specific expected exceptions. Never swallow exceptions or return success-shaped fallback data after a failure.
- Prefer standard-library features and existing dependencies. Explain any new dependency.
- Keep route handlers thin; put document parsing in `app/parsers/` and processing orchestration in `app/services/`.
- Follow Ruff configuration if present. Do not reformat unrelated files.
