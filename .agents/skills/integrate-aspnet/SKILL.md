---
name: integrate-aspnet
description: Designs or reviews the boundary between DocuExtract and an ASP.NET Core Clean Architecture consumer, including typed HttpClient, API contract mapping, timeout, cancellation, and downstream failures.
---

# ASP.NET Core Integration

## Objective
Keep DocuExtract independent while making its HTTP contract safe and straightforward for an ASP.NET Core application to consume.

## Procedure
1. Read `docs/architecture/api-contract.md` and confirm it matches the implemented OpenAPI schema.
2. Identify the .NET use case that needs extraction and the exact request/response fields it consumes.
3. Define an Application-layer abstraction such as `IDocumentExtractor`; keep `HttpClient`, multipart construction, and JSON transport in Infrastructure.
4. Use a typed `HttpClient` registered through dependency injection.
5. Pass `CancellationToken` from the API/request boundary to the outbound HTTP call.
6. Configure an explicit timeout and map network failure, timeout, non-success HTTP response, invalid JSON, and known DocuExtract error codes separately.
7. Preserve or create a correlation ID and include it in logs on both services without logging document contents.
8. Consider upload size, request streaming, response size, retries, and service authentication. Do not introduce automatic retries without analyzing timeout/idempotency behavior.
9. Recommend contract/integration tests, including a controlled failure response.

## Architecture constraints
- ASP.NET Core owns business validation, authorization, workflow, and business-data persistence.
- Application depends on an abstraction, not on FastAPI or transport details.
- Infrastructure owns HTTP implementation details.
- Do not add .NET code to the DocuExtract repository unless explicitly requested.
- Do not share a database between the two services.

## Output
Provide the request/response mapping, C# interface/DTO/client-registration outline, error mapping, configuration requirements, and integration-test cases. Explain non-obvious .NET choices in Vietnamese for a developer who knows C# but is learning Python.
