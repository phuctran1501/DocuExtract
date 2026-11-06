# DocuExtract — Requirements

**Status:** Proposed baseline for the first MVP. Update this document when product scope changes.

## 1. Actors

- **API Consumer:** an ASP.NET Core API or another trusted internal service that sends a document for extraction.
- **Operator/Developer:** runs, configures, observes, and tests DocuExtract.

There is no end-user account or public self-service UI in the MVP.

## 2. Functional requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | The service exposes a health endpoint. | Must |
| FR-02 | The service accepts PDF files and extracts text. | Must |
| FR-03 | The service accepts DOCX files and extracts text. | Must |
| FR-04 | The service returns filename metadata, detected media type, byte size, extracted text, character count, and word count. | Must |
| FR-05 | The service rejects unsupported file types with a stable error code. | Must |
| FR-06 | The service rejects files exceeding a configurable size limit. | Must |
| FR-07 | The service handles malformed, empty, and encrypted documents without crashing. | Must |
| FR-08 | The service normalizes extracted text using documented deterministic rules. | Should |
| FR-09 | The service reports when a document contains no extractable text; it does not pretend to perform OCR. | Must |
| FR-10 | The service exposes an optional endpoint for basic text statistics. | Could |

## 3. Non-functional requirements

### NFR-01 — Security
- Uploaded bytes and document contents are untrusted.
- Enforce maximum size and supported formats.
- Do not trust client MIME type or filename as proof of file type.
- Never log extracted text or secrets.
- Do not return stack traces or internal paths.

### NFR-02 — Reliability
- A bad document must fail as a request-level error, not crash the service process.
- Every expected failure must map to a documented error code.
- Cleanup temporary resources on both success and failure if temporary files are ever used.

### NFR-03 — Performance
- The MVP targets small documents within the configured upload limit.
- Establish a baseline before adding concurrency, queues, or a worker system.
- Avoid unbounded reads and response sizes.

### NFR-04 — Maintainability
- Separate HTTP routes, schemas, services, and format-specific parsers.
- Use type hints and explicit schemas.
- Test parsers independently from HTTP routes.

### NFR-05 — Interoperability
- Use versioned REST endpoints and JSON responses.
- Keep API field names and error codes stable.
- Document multipart field names, content types, size limits, and status codes.

### NFR-06 — Operability
- Configuration comes from environment variables/settings.
- Provide health visibility and structured logs.
- Provide reproducible local setup and Docker instructions when containerization is implemented.

## 4. Initial limits and policies

| Setting | Initial policy |
|---|---|
| Upload limit | 10 MiB default; configurable |
| Formats | `.pdf`, `.docx` only |
| OCR | Not supported in MVP |
| Persistence | No persistent upload storage |
| API version | `/api/v1` |
| Health | `/health` |
| Auth | Trusted internal network for local MVP; production service-to-service auth must be designed before external exposure |

These values are defaults for implementation planning. Any production deployment must revisit upload size, access control, rate limits, timeouts, and resource limits.

## 5. Acceptance criteria for the first extraction slice

- A valid text-based PDF returns non-empty extracted text and correct metadata.
- A valid DOCX returns paragraph/table text according to documented extraction rules.
- A renamed or unsupported file is rejected when its actual content does not match an allowed format.
- An oversized upload is rejected without reading an unlimited payload into memory.
- A malformed, encrypted, or empty document returns a predictable error/warning.
- Tests cover success and failure cases.
- API documentation describes the actual response and error contract.
