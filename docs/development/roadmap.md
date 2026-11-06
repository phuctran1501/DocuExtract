# DocuExtract — Development Roadmap

The roadmap is ordered to create a working vertical slice early. A later phase is not permission to build its infrastructure now.

## Phase 0 — Repository foundation

- [ ] Initialize Python project and package manager.
- [ ] Create FastAPI application entry point.
- [ ] Add settings/configuration and `/health` endpoint.
- [ ] Add Ruff and pytest configuration.
- [ ] Add local setup instructions and initial CI checks.

**Exit criteria:** application starts locally; health endpoint and its test pass; setup is reproducible.

## Phase 1 — Text-processing foundation

- [ ] Define text normalization policy.
- [ ] Implement deterministic character/word/line statistics.
- [ ] Add unit tests for Unicode, whitespace, empty input, and line endings.
- [ ] Add optional `POST /api/v1/text/analyze` endpoint.

**Exit criteria:** service behavior is covered by unit and API tests.

## Phase 2 — PDF extraction

- [ ] Add PDF parser module using a focused library.
- [ ] Validate PDF signature and malformed/encrypted files.
- [ ] Extract text and page count.
- [ ] Normalize text and produce response metadata.
- [ ] Test empty/scanned-like PDFs and parser failure paths.

**Exit criteria:** valid text-based PDFs work; limitations are explicit; bad files do not crash the app.

## Phase 3 — DOCX extraction

- [ ] Add DOCX parser module.
- [ ] Define paragraph/table extraction ordering.
- [ ] Validate DOCX container/content.
- [ ] Add tests for paragraphs, tables, empty files, and malformed ZIP content.

**Exit criteria:** valid DOCX files return deterministic text and metadata.

## Phase 4 — Hardening and packaging

- [ ] Enforce and test configurable upload-size limit.
- [ ] Add correlation ID and structured logging.
- [ ] Verify no document content is logged.
- [ ] Add Dockerfile and non-root runtime.
- [ ] Add CI for lint, format check, and tests.
- [ ] Document health checks and service configuration.

**Exit criteria:** clean local build/test and container startup; expected failure modes are covered.

## Phase 5 — ASP.NET Core integration proof

- [ ] Finalize the API contract.
- [ ] Prepare a .NET `IDocumentExtractor` abstraction and Infrastructure typed `HttpClient` adapter in the consuming ASP.NET Core application.
- [ ] Pass cancellation and correlation IDs.
- [ ] Map timeout, connection failure, and downstream error responses.
- [ ] Add an integration test against a running DocuExtract instance or a controlled HTTP stub.

**Exit criteria:** the ASP.NET Core Application layer depends on an abstraction, while the Infrastructure adapter owns HTTP transport details.

## Later ideas — only after evidence

- OCR for scanned PDFs.
- Asynchronous job processing / queue / worker.
- Object storage.
- LLM-based CV understanding.
- Authentication between services, rate limits, and production network policies.

Create an ADR and update requirements before adding any of these.
