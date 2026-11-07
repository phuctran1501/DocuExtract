# Dev Log: Phase 1 — Nền Tảng Xử Lý Văn Bản (Text Processing Foundation)

- **Ngày:** 2026-11-07
- **Issue/PR liên quan:** Phase 1 ([docs/development/roadmap.md](file:///d:/DocuExtract/docs/development/roadmap.md))
- **Files:** `app/services/text_service.py`, `app/schemas/text.py`, `app/api/routes/text.py`, `app/main.py`, `tests/unit/test_text_service.py`, `tests/integration/test_text_api.py`

## Những gì đã xây dựng
- Triển khai `app/services/text_service.py` với 2 hàm chính: `normalize_text` (chuẩn hóa văn bản Unicode NFC, làm sạch ký tự điều khiển, ngắt dòng LF, chuẩn hóa khoảng trắng) và `compute_text_stats` (tính số ký tự, số từ, số dòng xác định).
- Định nghĩa schemas Pydantic trong `app/schemas/text.py`: `TextAnalyzeRequest` (có ràng buộc `max_length=1_000_000`) và `TextAnalyzeResponse`.
- Triển khai endpoint `POST /api/v1/text/analyze` trong `app/api/routes/text.py` và đăng ký vào `app/main.py`.
- Viết bộ unit tests `tests/unit/test_text_service.py` (10 tests) và integration tests `tests/integration/test_text_api.py` (5 tests).

## Lý do chọn thiết kế này
- **Tách biệt ranh giới (Separation of Concerns):** `text_service.py` là pure Python, không import hay phụ thuộc vào FastAPI/HTTP. Thiết kế này giúp parser PDF/DOCX ở các phase sau dễ dàng gọi trực tiếp để chuẩn hóa văn bản trích xuất mà không cần đi qua HTTP layer.
- **Thư viện chuẩn (Standard Library First):** Tận dụng `unicodedata` và `re`, không cần cài đặt thêm thư viện NLP nặng nào, đảm bảo hiệu năng cao và footprint nhỏ.

## Cách hoạt động
1. Request gửi JSON `{ "text": "..." }` tới `POST /api/v1/text/analyze`.
2. FastAPI validate qua schema `TextAnalyzeRequest`.
3. Route gọi `analyze_text(payload.text)` -> thực hiện pipeline chuẩn hóa 7 bước -> đếm thống kê xác định -> trả về `TextStats`.
4. Endpoint chuyển đổi `TextStats` thành `TextAnalyzeResponse` và trả về mã HTTP `200 OK`.
5. `CorrelationIdMiddleware` tự động thêm header `X-Correlation-ID` vào response.

## Những điều cần lưu ý (Gotchas)
- **Tiếng Việt tổ hợp (NFD) vs dựng sẵn (NFC):** Một số bộ gõ tiếng Việt xuất ra ký tự tổ hợp (ví dụ: `a` + combining acute thay vì `á`). Hàm `unicodedata.normalize("NFC", text)` chuyển toàn bộ về dạng dựng sẵn đồng nhất.
- **Đếm từ xác định:** `text.split()` tách theo chuỗi khoảng trắng bất kỳ theo chuẩn POSIX. Điều này hoạt động ổn định và nhất quán trên đa ngôn ngữ có dấu cách phân từ.

## Kiểm thử và bằng chứng
1. `uv run ruff check .` -> `All checks passed!`
2. `uv run ruff format --check .` -> `54 files already formatted!`
3. `uv run pytest` -> `19 passed, 1 warning in 0.10s!`

## Điểm phỏng vấn / học tập
- **Khái niệm đã học:** Chuẩn hóa Unicode Canonical Decomposition/Composition (NFD vs NFC), cơ chế POSIX-style whitespace tokenization, cách thiết kế pure business service tách rời khỏi framework HTTP.
- **Đánh đổi (Trade-off):** Lựa chọn đếm từ theo khoảng trắng (`text.split()`) thay vì dùng mô hình segmentation học máy giúp service cực nhanh, không phụ thuộc C-extensions hay model weights, hoàn toàn đáp ứng mục tiêu của MVP.

