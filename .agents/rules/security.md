---
trigger: model_decision
description: Apply when handling uploaded files, document contents, secrets, logging, configuration, network exposure, or security-sensitive error paths.
---

# Security Rules

- Treat uploaded bytes, filenames, MIME types, and document contents as untrusted.
- Enforce a configurable file-size limit before unbounded reads. Validate extension and actual content/signature; do not trust client headers alone.
- Never use the uploaded filename as a filesystem path. Use server-generated temporary names and guaranteed cleanup if disk is required.
- Do not log document text, file bytes, credentials, tokens, or raw multipart bodies.
- Return safe, stable error messages; keep diagnostic details in protected server logs.
- Avoid unrestricted file types, decompression bombs, unbounded parsing, and uncontrolled response sizes.
- Do not claim OCR support for scanned documents unless an OCR implementation and tests exist.
- Never commit secrets or real `.env` values. Production exposure requires service-to-service authentication and network controls.
