# DocuExtract

> A learning-first document-processing microservice built with Python and FastAPI, designed to integrate with ASP.NET Core applications.

## 1. Project overview

DocuExtract receives supported documents, extracts their text, performs lightweight normalization/analysis, and returns a predictable JSON response. It is intended to be a specialized service behind an ASP.NET Core API—not a replacement for the main business backend.

**Initial supported formats:** PDF and DOCX.

**MVP principle:** start stateless and synchronous. Do not add a database, Redis, RabbitMQ, Celery, OCR, or LLM until a real requirement justifies it.

## 2. Goals

- Learn Python backend development through a real, bounded service.
- Build REST APIs with FastAPI and Pydantic.
- Handle uploaded files safely.
- Separate HTTP routes from parsing and processing logic.
- Produce a stable API contract that an ASP.NET Core typed client can consume.
- Practice automated testing, Docker, and service-to-service failure handling.

## 3. Initial technology baseline

| Technology | Purpose |
|---|---|
| Python 3.12+ | Runtime |
| FastAPI | REST API |
| Pydantic | Request/response validation |
| Uvicorn | ASGI server |
| pypdf | PDF text extraction |
| python-docx | DOCX text extraction |
| pytest + HTTPX | Automated tests |
| Ruff | Linting and formatting |
| Docker | Container packaging in a later milestone |

The actual repository configuration takes precedence over this proposed baseline once implementation begins.

## 4. Architecture at a glance

```text
ASP.NET Core API
      |
      | HTTP / multipart upload + JSON response
      v
DocuExtract (FastAPI)
  API routes
      |
  Processing services
      |
  Format parsers (PDF / DOCX)
      |
  Structured response
```

ASP.NET Core remains responsible for identity, authorization, business workflows, and business-data persistence. DocuExtract is responsible for document extraction and document-oriented processing only.

## 5. Repository structure

```text
DocuExtract/
├── app/
│   ├── main.py
│   ├── api/routes/
│   ├── schemas/
│   ├── services/
│   ├── parsers/
│   └── core/
├── tests/
├── docs/
│   ├── product/
│   ├── architecture/decisions/
│   ├── development/
│   ├── operations/
│   └── ai/
├── .agents/
│   ├── rules/
│   └── skills/
├── .github/
├── AGENTS.md
├── GEMINI.md
└── README.md
```

The `app/` tree is the proposed MVP layout. Inspect and adapt to the actual project before creating or moving files.

## 6. Documentation map

| Document | Purpose |
|---|---|
| `AGENTS.md` | Persistent AI-agent instructions |
| `docs/product/vision.md` | Product purpose and boundaries |
| `docs/product/requirements.md` | Functional and non-functional requirements |
| `docs/architecture/architecture.md` | Service architecture and dependencies |
| `docs/architecture/api-contract.md` | HTTP endpoints and JSON contract |
| `docs/architecture/decisions/` | Accepted architecture decisions |
| `docs/development/roadmap.md` | Incremental implementation milestones |
| `docs/development/definition-of-done.md` | Acceptance and quality checklist |
| `docs/ai/prompt-playbook.md` | Practical prompts for Gemini in Antigravity |

## 7. Getting started

The detailed local setup instructions will be maintained in [`docs/operations/development-setup.md`](docs/operations/development-setup.md). The project is still in its planning/scaffolding stage; do not assume application endpoints exist until they are implemented and tested.

## 8. AI-assisted development

This repository uses Antigravity's workspace instructions, rules, and skills:

- `AGENTS.md` is the canonical always-on project guide.
- `.agents/rules/` contains scoped constraints for Python, API contracts, security, and testing.
- `.agents/skills/` contains repeatable procedures for planning, implementing, reviewing, and preparing ASP.NET integration.

Give the agent one bounded task at a time. Ask it to inspect and plan before it edits a medium/large feature. Review the diff and test evidence before accepting the result.
