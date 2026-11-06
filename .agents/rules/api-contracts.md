---
trigger: glob
globs: "app/api/**/*.py, app/schemas/**/*.py"
description: Phiên bản API, Pydantic schemas, status codes, và các quy tắc về response/error contract ổn định.
---

# Quy Tắc API Contract

- Giữ các endpoint công khai dưới `/api/v1` trừ khi có ADR được chấp nhận nói khác.
- Định nghĩa rõ ràng các Pydantic request/response models cho các payload có cấu trúc.
- Giữ các success response và error envelope nhất quán với `docs/architecture/api-contract.md`.
- Sử dụng đúng HTTP status codes; không bao giờ báo cáo một lần trích xuất thất bại là HTTP 200.
- Giữ các machine-readable error codes ổn định. Không để lộ raw parser exceptions, stack traces, secrets, hoặc absolute paths.
- Cập nhật API contract và tests bất cứ khi nào hành vi request/response thay đổi.
- Không thêm authentication, persistence, hoặc một transport protocol mới mà không có yêu cầu rõ ràng và quyết định thiết kế.
