# ADR-001: Keep the first DocuExtract release stateless

- **Status:** Accepted for MVP
- **Date:** 2026-11-05
- **Decision owners:** Project owner

## Context

The first goal is to learn Python/FastAPI and prove a useful document-processing boundary for ASP.NET Core. Adding storage, queues, or databases would increase setup and operational work before the extraction behavior is validated.

## Decision

The MVP processes an upload within the request lifecycle and returns extracted text and metadata. It does not persist the uploaded file or extracted text. The service does not own business entities, user accounts, or application data.

## Consequences

**Positive**
- Fewer components and simpler local setup.
- Easier tests and reproducible behavior.
- Clear ownership: the ASP.NET Core application stores business data when appropriate.

**Negative / limitations**
- Large or slow documents may hold an HTTP request open.
- The result is not recoverable from DocuExtract after the response is lost.
- Memory/CPU limits and request timeouts must be considered.

## Revisit when

- Documents routinely exceed the synchronous processing budget.
- Results must survive caller disconnects or be polled later.
- Multiple consumers need shared processing state.
- Throughput requires a dedicated worker/queue model.

Any change should compare synchronous processing, FastAPI background tasks, and a dedicated queue/worker architecture based on measured needs.
