# DocuExtract — API Contract (v1)

**Status:** Proposed contract. The implemented OpenAPI document must match this file; update both together.

## 1. Conventions

- Base path: `/api/v1`
- Content negotiation: JSON responses.
- Upload: `multipart/form-data`.
- File field: `file`.
- Allowed file formats: PDF and DOCX.
- Default upload limit: 10 MiB, configurable.
- Text encoding: UTF-8 in JSON responses.

## 2. Health

### `GET /health`

Returns HTTP `200` when the process is alive and able to serve requests.

```json
{
  "status": "ok",
  "service": "docuextract"
}
```

Do not report downstream dependencies that do not exist. Add readiness checks only when the service gains dependencies that can actually become unavailable.

## 3. Extract document

### `POST /api/v1/documents/extract`

**Request:** `multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `file` | binary file | Yes | A PDF or DOCX document |

**Success:** HTTP `200 OK`

```json
{
  "document": {
    "filename": "candidate-cv.pdf",
    "media_type": "application/pdf",
    "size_bytes": 48321,
    "format": "pdf"
  },
  "extraction": {
    "text": "Extracted document text...",
    "page_count": 2,
    "character_count": 1450,
    "word_count": 218
  },
  "warnings": []
}
```

For DOCX, `page_count` is `null` because DOCX does not provide a stable page count independent of a rendering engine. The exact paragraph/table ordering and whitespace normalization must be documented by the parser tests.

A document with no extractable text should not silently look like a successful useful extraction. Return a documented warning or a stable `NO_EXTRACTABLE_TEXT` error according to the final implementation decision. Do not claim OCR support.

## 4. Analyze text (optional MVP endpoint)

### `POST /api/v1/text/analyze`

**Request:** `application/json`

```json
{
  "text": "Text to analyze"
}
```

**Success:** HTTP `200 OK`

```json
{
  "character_count": 16,
  "word_count": 3,
  "line_count": 1
}
```

This endpoint is optional and should not delay the core document extraction flow.

## 5. Error contract

All expected API errors use the same envelope:

```json
{
  "error": {
    "code": "UNSUPPORTED_FILE_TYPE",
    "message": "Only PDF and DOCX files are supported.",
    "correlation_id": "01J..."
  }
}
```

The `correlation_id` may be omitted only when a request has not yet been assigned one. Never include stack traces or internal parser messages in the public message.

| HTTP status | Error code | Meaning |
|---:|---|---|
| 400 | `INVALID_REQUEST` | Missing or malformed request input |
| 413 | `FILE_TOO_LARGE` | Upload exceeds configured limit |
| 415 | `UNSUPPORTED_FILE_TYPE` | Unsupported file format or detected content |
| 422 | `INVALID_DOCUMENT` | File is malformed, unreadable, or structurally invalid |
| 422 | `ENCRYPTED_DOCUMENT` | Encrypted/password-protected document cannot be read |
| 422 | `NO_EXTRACTABLE_TEXT` | No text could be extracted and OCR is unavailable |
| 500 | `EXTRACTION_FAILED` | Unexpected extraction failure; details remain in server logs |
| 503 | `SERVICE_UNAVAILABLE` | Service cannot currently process requests |

The implementation may refine this table, but changes must be reflected in tests and this document.

## 6. ASP.NET Core client expectations

The caller should:
- Send the file as multipart field `file`.
- Set an explicit timeout appropriate to the maximum document size.
- Pass `CancellationToken` through the application call chain.
- Handle `200`, `4xx`, `5xx`, timeout, connection failure, and invalid response JSON separately.
- Preserve the correlation ID for diagnostics.
- Avoid retrying non-idempotent uploads blindly. A retry policy must account for file size, timeout, and whether processing has side effects (the MVP should not have side effects).

## 7. Contract-change policy

Treat response field removal/renaming, changed field types, changed error semantics, and changed required multipart fields as potentially breaking changes. Update this document and add tests before implementation. Prefer additive optional fields for backward-compatible evolution.
