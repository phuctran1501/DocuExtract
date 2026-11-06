# Development Setup

> This file documents the intended setup baseline. Adjust commands to the actual package manager and project files once the repository is initialized.

## 1. Prerequisites

- Git
- Python 3.12 or newer
- `uv` for Python project/dependency management (recommended for this project)
- Antigravity with the workspace opened at the repository root

## 2. Initialize the Python project (first setup only)

If the repository does not yet have a `pyproject.toml`:

```bash
uv init --python 3.12
```

If `pyproject.toml` already exists, do not run `uv init` over it. Inspect it and preserve its current package-manager setup.

## 3. Add the initial dependencies

```bash
uv add fastapi "uvicorn[standard]" pydantic-settings python-multipart pypdf python-docx
uv add --dev pytest httpx ruff
uv sync
```

Only add dependencies that the current milestone actually uses. For example, `python-multipart` is needed for FastAPI multipart uploads; document parsers are needed when PDF/DOCX parsing is implemented.

## 4. Run the API

After the application entry point exists:

```bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open the generated API documentation at `http://127.0.0.1:8000/docs` and the health endpoint at `http://127.0.0.1:8000/health` when implemented.

## 5. Run checks

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

To format files intentionally:

```bash
uv run ruff format .
```

Review the diff after formatting; do not format unrelated files.

## 6. Environment variables

Create a local `.env` only when settings require it. Commit `.env.example` with placeholder values and add `.env` to `.gitignore`. Never put API keys, passwords, JWT secrets, or private URLs in tracked Markdown.

## 7. Docker (later milestone)

Docker commands should be added after a Dockerfile and compose configuration exist. Do not instruct contributors to run commands that are not present in the repository. Avoid destructive volume-reset commands unless the owner explicitly intends to delete local data.
