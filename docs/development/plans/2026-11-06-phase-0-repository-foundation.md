# Kế hoạch triển khai: Phase 0 — Nền tảng Repository (Repository Foundation)

- **Trạng thái:** Hoàn thành
- **Đặc tả liên quan:** `docs/product/requirements.md`, `docs/architecture/architecture.md`, `docs/architecture/api-contract.md`
- **Issue liên quan:** Phase 0 trong `docs/development/roadmap.md`

## 1. Kết quả khảo sát repository

- **Khảo sát bằng CodeGraph:** Đã gọi công cụ `codegraph_explore`. Kết quả: Hiện tại repository chưa có mã nguồn được index vì chưa có file code (`.py`, `.ts`, v.v.).
- **Hiện trạng repository:**
  - Repository hiện tại mới chỉ có bộ khung tài liệu (`AGENTS.md`, `README.md`, `CONTENTS.md`, `GEMINI.md`, thư mục `docs/`), quy tắc và kỹ năng cho agent (`.agents/`), cấu hình git và GitHub templates (`.github/`).
  - Chưa có `pyproject.toml`, `.python-version`, `.gitignore`, thư mục `app/` và `tests/`.
- **Môi trường runtime & công cụ:**
  - Hệ điều hành: Windows x64.
  - Quản lý gói: Đã có sẵn `uv 0.5.9` tại `C:\Users\Admin\.local\bin\uv.exe`.
  - Python: Đã có sẵn CPython 3.12.8 tại `C:\Users\Admin\AppData\Roaming\uv\python\cpython-3.12.8-windows-x86_64-none\python.exe`.
  - Lưu ý hệ thống: `python.exe` mặc định trên PATH của Windows là WindowsApps stub (Execution Alias) gây lỗi `os error 1920`. Cần thiết lập `UV_PYTHON` trỏ trực tiếp đến interpreter của `uv`.
- **Ràng buộc:**
  - Tuân thủ nghiêm ngặt `AGENTS.md`, `.agents/rules/python-conventions.md`, `security.md`, `testing.md`, `api-contracts.md`.
  - Không thêm database, Redis, Celery, OCR hay LLM (theo ADR-001).

## 2. Phạm vi (Scope)

### Trong phạm vi
1. Khởi tạo cấu hình Python project chuẩn (`pyproject.toml`, `.python-version`, `.gitignore`) với Python 3.12.
2. Cài đặt các dependencies cần thiết cho Phase 0:
   - Runtime: `fastapi`, `uvicorn[standard]`, `pydantic`, `pydantic-settings`.
   - Dev: `pytest`, `httpx`, `ruff`.
3. Thiết lập cấu hình linter/formatter `ruff` và test runner `pytest` trong `pyproject.toml`.
4. Xây dựng cấu trúc thư mục module hóa sạch theo `AGENTS.md`:
   - `app/core/` (config, correlation ID, error handling)
   - `app/schemas/` (Pydantic models cho health, error)
   - `app/api/routes/` (health endpoint)
   - `app/main.py` (FastAPI app factory & middleware wiring)
   - `tests/unit/` & `tests/integration/`
5. Triển khai endpoint `GET /health` trả về `{ "status": "ok", "service": "docuextract" }`.
6. Triển khai cấu trúc Error Envelope chuẩn theo API Contract `{ "error": { "code", "message", "correlation_id" } }`.
7. Triển khai Middleware Correlation ID (gán correlation ID cho mỗi request, hỗ trợ header `X-Correlation-ID`).
8. Viết integration test cho `/health` và correlation ID middleware.
9. Kiểm tra chất lượng code qua Ruff (lint + format) và Pytest.

### Ngoài phạm vi (Explicit Non-Goals)
- Không cài đặt các thư viện trích xuất tài liệu (`pypdf`, `python-docx`, `python-multipart`) cho tới Phase 1-3 để tuân thủ nguyên tắc YAGNI và lộ trình từng bước.
- Không cấu hình Dockerfile/CI cho tới Phase 4.
- Không triển khai OCR, Database, Message Queue, Background Worker.

## 3. Thiết kế

### 3.1. Cấu trúc thư mục mục tiêu
```text
DocuExtract/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Khởi tạo FastAPI app, middleware, route registration
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Settings sử dụng pydantic-settings
│   │   ├── correlation.py       # Middleware & context cho Correlation ID
│   │   └── errors.py            # Global exception handlers & error envelope formatting
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── health.py            # Model HealthResponse
│   │   └── error.py             # Model ErrorResponse & ErrorDetail
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── health.py        # Route GET /health
│   ├── services/
│   │   └── __init__.py
│   └── parsers/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Test fixtures (TestClient/AsyncClient)
│   ├── unit/
│   │   └── __init__.py
│   └── integration/
│       ├── __init__.py
│       └── test_health.py       # Kiểm thử GET /health và Correlation ID
├── .gitignore
├── .python-version
└── pyproject.toml               # Quản lý project, dependencies, ruff & pytest config
```

### 3.2. Luồng xử lý request
```text
HTTP Request ---> CorrelationIDMiddleware (sinh hoặc nhận X-Correlation-ID)
             ---> ExceptionHandler (bắt unhandled exceptions, format error envelope)
             ---> Route Handler: GET /health
             ---> HealthResponse JSON
             ---> Thêm header X-Correlation-ID vào HTTP Response
```

### 3.3. API Contract & Data Schema
- **GET /health**:
  - Response 200:
    ```json
    {
      "status": "ok",
      "service": "docuextract"
    }
    ```
- **Error Envelope** (khi có lỗi HTTP/Server):
  - Response 4xx/5xx:
    ```json
    {
      "error": {
        "code": "INVALID_REQUEST",
        "message": "Chi tiết lỗi...",
        "correlation_id": "01J..."
      }
    }
    ```

### 3.4. Định hướng UI/UX (Developer Experience & Swagger UI theo chuẩn Impeccable)
Mặc dù DocuExtract là backend service không có web client UI trong MVP, giao diện phục vụ nhà phát triển (Developer UI) chính là FastAPI Swagger UI (`/docs`) và ReDoc (`/redoc`).
- **Craftsmanship & Clarity:** Cấu hình OpenAPI metadata tường minh: title, version, summary, tags, descriptions bằng tiếng Anh chuẩn mực kỹ thuật.
- **Hierarchy:** Phân nhóm các endpoint theo Tag rõ ràng (ví dụ: `Health`).
- **Predictability:** Mọi endpoint đều hiển thị rõ response schema và error schema mẫu trong OpenAPI docs, giúp lập trình viên ASP.NET Core dễ dàng sinh typed client hoặc kiểm thử.

## 4. Các bước triển khai tuần tự

1. **Bước 1 — Khởi tạo môi trường & project file:**
   - Tạo `.gitignore` chuẩn cho Python/FastAPI (`.venv`, `__pycache__`, `.pytest_cache`, `.ruff_cache`, `.env`).
   - Tạo `.python-version` ghim `3.12`.
   - Tạo `pyproject.toml` định nghĩa metadata dự án, dependencies và cấu hình Ruff + pytest.
   - Chạy `uv sync` để tạo virtual environment `.venv` và lockfile `uv.lock`.
2. **Bước 2 — Xây dựng tầng Core:**
   - `app/core/config.py`: `Settings` class với `APP_NAME`, `DEBUG`, `API_V1_PREFIX`, `HOST`, `PORT`, `MAX_UPLOAD_SIZE_BYTES` (mặc định 10MB).
   - `app/core/correlation.py`: Quản lý context-var correlation ID và FastAPI middleware `CorrelationIdMiddleware`.
   - `app/core/errors.py`: Exception handlers chuyển đổi `HTTPException`, `RequestValidationError` và generic exceptions sang `ErrorResponse`.
3. **Bước 3 — Xây dựng Schemas:**
   - `app/schemas/health.py`: `HealthResponse(status="ok", service="docuextract")`.
   - `app/schemas/error.py`: `ErrorDetail` và `ErrorResponse` envelope.
4. **Bước 4 — Xây dựng Route & App Entry:**
   - `app/api/routes/health.py`: Router cho `GET /health`.
   - `app/main.py`: Hàm `create_app()` khởi tạo FastAPI, gắn router, gắn middleware và exception handlers.
5. **Bước 5 — Viết Tests:**
   - `tests/conftest.py`: Fixture cung cấp `TestClient`.
   - `tests/integration/test_health.py`: Kiểm thử `GET /health` trả về 200, đúng schema, có header `X-Correlation-ID`.
   - Kiểm thử error handler bắt 404 và trả về đúng envelope `{ "error": { "code", "message", "correlation_id" } }`.
6. **Bước 6 — Xác minh chất lượng:**
   - Chạy `uv run ruff check .`
   - Chạy `uv run ruff format --check .`
   - Chạy `uv run pytest`
7. **Bước 7 — Cập nhật tài liệu:**
   - Cập nhật `docs/operations/development-setup.md` nếu có lệnh thực tế cụ thể.
   - Tạo dev log theo mẫu `docs/development/dev-log-template.md`.

## 5. Kế hoạch kiểm thử

| Kịch bản | Mức độ test | Phương thức | Kết quả mong đợi |
|---|---|---|---|
| `GET /health` trả về trạng thái ok | Integration | `test_health_endpoint_returns_ok` | Status `200`, `{"status": "ok", "service": "docuextract"}` |
| Response trả về có header `X-Correlation-ID` | Integration | `test_health_returns_correlation_id_header` | Header `X-Correlation-ID` tồn tại và không rỗng |
| Request có sẵn `X-Correlation-ID` | Integration | `test_health_preserves_client_correlation_id` | Header trả về khớp với ID client đã gửi |
| Gọi endpoint không tồn tại (404) | Integration | `test_not_found_returns_standard_error_envelope` | Status `404`, body khớp schema `ErrorResponse`, code `NOT_FOUND` |

## 6. Rủi ro và biện pháp giảm thiểu

- **Rủi ro môi trường Windows:** Alias `python.exe` của Windows gây lỗi `os error 1920`.
  - *Biện pháp:* Khai báo rõ ràng và thiết lập biến môi trường `UV_PYTHON` trong quy trình chạy command.
- **Rủi ro rò rỉ thông tin nội bộ khi gặp Exception:**
  - *Biện pháp:* Exception handler toàn cục chỉ log chi tiết lỗi vào server log, không trả về stack trace cho client; client chỉ nhận được `EXTRACTION_FAILED` hoặc `INTERNAL_SERVER_ERROR` cùng `correlation_id` để tra cứu log.
- **Rủi ro sai lệch API contract:**
  - *Biện pháp:* Viết schema Pydantic khớp 100% với `docs/architecture/api-contract.md` ngay từ đầu và có integration test khóa chặt định dạng.

## 7. Tài liệu cần cập nhật sau khi hoàn thành

- [ ] `docs/development/roadmap.md` (Đánh dấu hoàn thành các checkbox của Phase 0)
- [ ] `docs/operations/development-setup.md` (Xác nhận các lệnh thực tế hoạt động)
- [ ] `docs/development/dev-logs/dev-log-phase-0.md` (Ghi lại dev log theo template)

## 8. Lệnh xác minh

```powershell
$env:UV_PYTHON = "C:\Users\Admin\AppData\Roaming\uv\python\cpython-3.12.8-windows-x86_64-none\python.exe"
& "C:\Users\Admin\.local\bin\uv.exe" run ruff check .
& "C:\Users\Admin\.local\bin\uv.exe" run ruff format --check .
& "C:\Users\Admin\.local\bin\uv.exe" run pytest
```

