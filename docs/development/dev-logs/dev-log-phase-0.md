# Dev Log: Phase 0 — Nền Tảng Repository (Repository Foundation)

- **Ngày:** 2026-11-06
- **Issue/PR liên quan:** Phase 0 ([docs/development/roadmap.md](file:///d:/DocuExtract/docs/development/roadmap.md))
- **Files:** `pyproject.toml`, `.python-version`, `.gitignore`, `.env.example`, `app/main.py`, `app/core/config.py`, `app/core/correlation.py`, `app/core/errors.py`, `app/schemas/health.py`, `app/schemas/error.py`, `app/api/routes/health.py`, `tests/conftest.py`, `tests/integration/test_health.py`

## Những gì đã xây dựng
- Khởi tạo project Python 3.12 quản lý bằng `uv` với các runtime dependencies (`fastapi`, `uvicorn[standard]`, `pydantic`, `pydantic-settings`) và dev dependencies (`pytest`, `httpx`, `ruff`).
- Xây dựng cấu trúc module hóa phân tầng: `app/core`, `app/schemas`, `app/api/routes`, `app/services`, `app/parsers`.
- Endpoint `GET /health` trả về `{ "status": "ok", "service": "docuextract" }`.
- Middleware `CorrelationIdMiddleware` tự động sinh hoặc giữ nguyên header `X-Correlation-ID`.
- Global Exception Handlers bắt các lỗi ứng dụng, Starlette HTTP exceptions (bao gồm 404), validation exceptions và unhandled exceptions, chuyển đổi thành chuẩn API Error Envelope `{ "error": { "code", "message", "correlation_id" } }`.

## Lý do chọn thiết kế này
- Áp dụng nguyên tắc tách biệt ranh giới: Route handler chỉ phụ thuộc schema và gọi service/trả status; Core config tách riêng dùng `pydantic-settings`; Middleware xử lý correlation ID đảm bảo mọi request vào và ra đều có trace ID; Exception handlers tập trung xử lý mọi lỗi và không làm rò rỉ stack trace ra client.

## Cách hoạt động
1. Request đến -> `CorrelationIdMiddleware` đọc header `X-Correlation-ID` (nếu không có thì sinh UUID mới) và lưu vào `ContextVar`.
2. Request chuyển tới route handler `GET /health` -> trả về model `HealthResponse`.
3. Middleware bổ sung header `X-Correlation-ID` vào response trả về client.
4. Nếu có lỗi (ví dụ route không tồn tại), Starlette/FastAPI raise `HTTPException` -> được `http_exception_handler` bắt và định dạng lại thành `ErrorResponse` kèm `correlation_id`.

## Những điều cần lưu ý (Gotchas)
- **Windows App Execution Alias:** Trên Windows, `python.exe` trong `WindowsApps` có thể gây lỗi `os error 1920`. Khắc phục bằng cách thiết lập biến môi trường `UV_PYTHON` trỏ thẳng tới interpreter của `uv`.
- **404 Routing Exception Handler:** Starlette bắn `starlette.exceptions.HTTPException` cho route 404 thay vì `fastapi.exceptions.HTTPException`. Do đó cần đăng ký handler trên `StarletteHTTPException` để định dạng chuẩn envelope.
- **FastAPI TestClient & asyncio:** Trên Windows sandbox, `starlette.testclient.TestClient` sử dụng `anyio` portal có thể bị ảnh hưởng nếu không có quyền mở loopback socket; khi chạy test cần lưu ý môi trường thực thi.

## Kiểm thử và bằng chứng
1. `uv run ruff check .` -> All checks passed!
2. `uv run ruff format --check .` -> 47 files already formatted!
3. `uv run pytest` -> 4 passed in 0.06s!

## Điểm phỏng vấn / học tập
- **Khái niệm đã học:** Cách tổ chức FastAPI application factory (`create_app`), quản lý correlation ID xuyên luồng bất đồng bộ bằng `contextvars.ContextVar`, và thiết lập cấu hình với `pydantic-settings`.
- **Đánh đổi (Trade-off):** Giữ Phase 0 ở mức tối giản, không thêm database hay background workers (ADR-001) để đảm bảo tính stateless và kiểm thử nhanh gọn.

