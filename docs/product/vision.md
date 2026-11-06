# DocuExtract — Product Vision

## 1. Problem

ASP.NET Core systems sometimes need specialized document-processing capability—for example, reading a candidate CV or extracting text from a user-uploaded PDF. Implementing every parser and text-processing library inside the main backend can increase coupling and make specialized processing harder to evolve independently.

## 2. Product vision

DocuExtract is a small, independently deployable Python service that accepts supported documents and returns extracted, normalized text plus basic metadata through a stable HTTP API.

## 3. Target consumers

- ASP.NET Core Web APIs using Clean Architecture.
- Internal services that need deterministic document-to-text extraction.
- Learning projects that need a realistic Python/FastAPI service boundary.

## 4. Core value

- A single responsibility: document extraction and lightweight text processing.
- A predictable, versioned API contract.
- Safe handling of untrusted uploads.
- Easy local execution and Docker packaging.
- Independent testing and deployment.

## 5. MVP scope

**In scope**
- PDF text extraction.
- DOCX text extraction.
- Basic text normalization and statistics.
- File validation and consistent error responses.
- Health endpoint, automated tests, and OpenAPI documentation.
- HTTP integration guidance for ASP.NET Core.

**Out of scope until explicitly approved**
- OCR for scanned/image-only documents.
- LLM-based CV understanding, summarization, or scoring.
- User accounts, JWT issuance, roles, and permissions.
- Persistent document storage or application database.
- Queue/worker infrastructure and distributed orchestration.
- Frontend/UI.

## 6. Product principles

1. Keep the service stateless until persistence is genuinely needed.
2. Make extraction deterministic and testable.
3. Treat documents as untrusted input.
4. Return machine-readable errors, not stack traces.
5. Keep business ownership in the consuming ASP.NET Core system.
6. Prefer a working, observable vertical slice over speculative infrastructure.
7. Make technical choices understandable to a beginner learning Python.

## 7. Success criteria

The MVP is successful when a caller can submit a valid PDF or DOCX, receive extracted text and metadata, receive a clear error for invalid/unsupported input, and test the behavior without connecting to a database or external AI provider.
