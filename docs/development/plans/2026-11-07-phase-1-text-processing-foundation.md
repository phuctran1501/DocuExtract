# Kế hoạch triển khai: Phase 1 — Nền tảng Xử lý Văn bản (Text Processing Foundation)

- **Trạng thái:** Đề xuất
- **Đặc tả liên quan:** `docs/product/requirements.md` (FR-04, FR-08, FR-10), `docs/architecture/architecture.md`, `docs/architecture/api-contract.md` (Mục 4)
- **Issue liên quan:** Phase 1 trong `docs/development/roadmap.md`

## 1. Kết quả khảo sát repository

- **Khảo sát bằng CodeGraph:**
  - `app/main.py`: Đang có `create_app()` đăng ký `health_router`. Chưa đăng ký router cho versioned API `/api/v1`.
  - `app/core/config.py`: Đã có `Settings.api_v1_prefix = "/api/v1"`.
  - `app/services/`: Hiện tại mới chỉ có file `__init__.py` rỗng.
  - `app/schemas/`: Đã có `health.py` và `error.py`. Chưa có schema cho Text Processing.
  - `app/api/routes/`: Đã có `health.py`. Chưa có route cho `/api/v1/text`.
  - `tests/`: Đã có `conftest.py` với fixture `client`, `tests/integration/test_health.py`. Chưa có unit test cho text service.
- **Ràng buộc:**
  - Logic xử lý text (chuẩn hóa và thống kê) là **pure Python**, không được phụ thuộc vào FastAPI hay các đối tượng HTTP request (theo Mục 5 của `AGENTS.md` và `docs/architecture/architecture.md`).
  - Không thêm thư viện ngoài (external dependencies); chỉ sử dụng thư viện chuẩn của Python (`unicodedata`, `re`) để giữ service gọn nhẹ, tốc độ cao.
  - Chưa chỉnh sửa mã nguồn ứng dụng cho đến khi kế hoạch được phê duyệt.

## 2. Phạm vi (Scope)

### Trong phạm vi
1. **Xác định và triển khai Chính sách chuẩn hóa văn bản (Text Normalization Policy):**
   - Chuẩn hóa Unicode sang dạng dựng sẵn `NFC` (`unicodedata.normalize('NFC', text)`), xử lý triệt để ký tự tiếng Việt dạng tổ hợp vs dựng sẵn.
   - Thống nhất ký tự xuống dòng: Chuyển đổi `\r\n` (Windows CRLF) và `\r` (Classic Mac) thành `\n` (Unix LF).
   - Làm sạch ký tự điều khiển không hợp lệ (null bytes `\x00`, control characters ngoại trừ `\t` và `\n`).
   - Xử lý khoảng trắng: Thay thế khoảng trắng Unicode đặc biệt (non-breaking space `\u00a0`, zero-width space `\u200b`, en-space, em-space, v.v.) thành khoảng trắng chuẩn hoặc loại bỏ.
   - Thu gọn khoảng trắng ngang liên tiếp (`[ \t]+` -> ` `) trên cùng một dòng và xóa khoảng trắng ở đầu/cuối mỗi dòng.
   - Thu gọn các dòng trống liên tiếp thừa (giới hạn tối đa 2 dòng trống liên tiếp `\n\n\n+` -> `\n\n`).
   - Xóa khoảng trắng thừa ở đầu và cuối văn bản (strip).
2. **Triển khai thuật toán thống kê văn bản xác định (Deterministic Text Statistics):**
   - `character_count`: Số ký tự của văn bản sau khi chuẩn hóa (`len(normalized_text)`).
   - `word_count`: Số lượng từ xác định bằng cách tách khoảng trắng (`len(normalized_text.split())`), phù hợp với định dạng đa ngôn ngữ (tiếng Việt, tiếng Anh, số, ký hiệu).
   - `line_count`: Số dòng xác định (`0` nếu chuỗi rỗng; ngược lại `len(normalized_text.splitlines())`).
3. **Triển khai Pydantic Schemas:**
   - `TextAnalyzeRequest`: Nhận `text: str` (có giới hạn độ dài hợp lý để chống DoS bộ nhớ).
   - `TextAnalyzeResponse`: Khớp chính xác API contract `{ "character_count": int, "word_count": int, "line_count": int }`.
4. **Triển khai Endpoint API:**
   - `POST /api/v1/text/analyze` nhận request JSON, gọi `TextService`, trả về `TextAnalyzeResponse`.
   - Đăng ký vào router của FastAPI với prefix `/api/v1`.
5. **Kiểm thử tự động:**
   - Unit tests bao phủ toàn diện: Unicode tiếng Việt (tổ hợp/dựng sẵn), whitespace đa dạng, input rỗng, xuống dòng CRLF/LF/CR, control characters, số đếm từ và dòng.
   - Integration tests cho API endpoint: Happy path, input rỗng, payload sai định dạng (400 `INVALID_REQUEST`), kiểm tra bảo toàn `X-Correlation-ID`.

### Ngoài phạm vi (Explicit Non-Goals)
- Không bổ sung tokenizers phức tạp (NLTK, spaCy) hay thư viện NLP nặng.
- Không triển khai OCR hay trích xuất PDF/DOCX (dành cho Phase 2 và 3).
- Không lưu trữ văn bản vào database hay cache Redis.

## 3. Thiết kế

### 3.1. Ranh giới module & Luồng dữ liệu

```text
HTTP Request (POST /api/v1/text/analyze)
      │
      ▼
app/api/routes/text.py (Validation qua Pydantic schema)
      │
      ▼
app/services/text_service.py (normalize_text -> count_stats)
      │
      ▼
app/schemas/text.py (Serialization thành TextAnalyzeResponse)
      │
      ▼
HTTP Response (200 OK + Header X-Correlation-ID)
```

### 3.2. Chi tiết các module

1. **`app/services/text_service.py`**:
   - `normalize_text(text: str) -> str`: Thực hiện pipeline chuẩn hóa tuần tự:
     1. Loại bỏ null byte và control chars (giữ lại `\t`, `\n`).
     2. Chuẩn hóa Unicode `NFC`.
     3. Chuẩn hóa các loại khoảng trắng Unicode về khoảng trắng chuẩn.
     4. Chuẩn hóa ký tự xuống dòng thành `\n`.
     5. Cắt tỉa khoảng trắng ở cuối mỗi dòng và thu gọn chuỗi khoảng trắng ngang (` ` và `\t`) thành 1 dấu cách.
     6. Giới hạn các dòng trống liên tiếp (tối đa 2 dòng trống: `\n\n`).
     7. Strip đầu và cuối chuỗi.
   - `analyze_text(text: str) -> TextAnalysisResult`:
     1. Gọi `normalize_text(text)`.
     2. Tính toán `character_count`, `word_count`, `line_count`.
     3. Trả về `TextAnalysisResult(text, character_count, word_count, line_count)`.

2. **`app/schemas/text.py`**:
   ```python
   class TextAnalyzeRequest(BaseModel):
       text: str = Field(..., description="Văn bản cần phân tích và tính toán thống kê.")

   class TextAnalyzeResponse(BaseModel):
       character_count: int = Field(..., ge=0, description="Tổng số ký tự sau khi chuẩn hóa.")
       word_count: int = Field(..., ge=0, description="Tổng số từ.")
       line_count: int = Field(..., ge=0, description="Tổng số dòng.")
   ```

3. **`app/api/routes/text.py`**:
   - Router với prefix `/text`, tag `Text Analysis`.
   - Endpoint: `@router.post("/analyze", response_model=TextAnalyzeResponse)`.

4. **`app/main.py`**:
   - Đăng ký `text.router` vào `app` với prefix từ settings: `settings.api_v1_prefix` (`/api/v1`).

### 3.3. Ảnh hưởng API Contract
- Hoàn toàn tuân thủ và hiện thực hóa Mục 4 trong `docs/architecture/api-contract.md`:
  `POST /api/v1/text/analyze` trả về:
  ```json
  {
    "character_count": 16,
    "word_count": 3,
    "line_count": 1
  }
  ```
- Không có breaking change nào đối với các endpoint hiện có.

## 4. Các bước triển khai tuần tự

1. **Bước 1 — Xây dựng Core Service (`app/services/text_service.py`):**
   - Triển khai dataclass `TextStats`.
   - Triển khai `normalize_text(text: str) -> str`.
   - Triển khai `compute_text_stats(text: str) -> TextStats`.
2. **Bước 2 — Xây dựng Schemas (`app/schemas/text.py`):**
   - Khai báo `TextAnalyzeRequest` và `TextAnalyzeResponse`.
3. **Bước 3 — Xây dựng Route & Đăng ký Router (`app/api/routes/text.py` & `app/main.py`):**
   - Viết route handler trong `app/api/routes/text.py`.
   - Gắn `api_router` vào `app/main.py` với tiền tố `/api/v1`.
4. **Bước 4 — Viết Unit Tests (`tests/unit/test_text_service.py`):**
   - Test chuẩn hóa Unicode: Tiếng Việt dựng sẵn (`Đại học Bách Khoa`) vs tổ hợp (`Đại học Bách Khoa`) -> đồng nhất.
   - Test xuống dòng: CRLF (`\r\n`), CR (`\r`), LF (`\n`).
   - Test khoảng trắng: Non-breaking space (`\u00a0`), tab, nhiều dấu cách liên tiếp.
   - Test dòng trống: 4 dòng trống liên tiếp rút về 2 dòng trống.
   - Test ký tự điều khiển: Null bytes và ký tự không in được.
   - Test chuỗi rỗng: `""` -> 0 chars, 0 words, 0 lines.
   - Test chuỗi chỉ có khoảng trắng: `"   \n\n   "` -> 0 chars, 0 words, 0 lines.
5. **Bước 5 — Viết Integration Tests (`tests/integration/test_text_api.py`):**
   - Happy path: `POST /api/v1/text/analyze` với văn bản chuẩn.
   - Edge cases: Chuỗi rỗng, chuỗi tiếng Việt phức tạp.
   - Validation failure: Body không phải JSON, thiếu field `text` -> Trả về 400 `INVALID_REQUEST` với envelope chuẩn.
   - Header `X-Correlation-ID` được duy trì.
6. **Bước 6 — Xác minh chất lượng & CI:**
   - Chạy `uv run ruff check .`
   - Chạy `uv run ruff format --check .`
   - Chạy `uv run pytest`
7. **Bước 7 — Cập nhật tài liệu:**
   - Cập nhật `docs/development/roadmap.md` (Đánh dấu hoàn thành Phase 1).
   - Thêm `docs/development/dev-logs/dev-log-phase-1.md`.

## 5. Kế hoạch kiểm thử

| Kịch bản | Mức độ test | Phương thức | Kết quả mong đợi |
|---|---|---|---|
| Chuẩn hóa Unicode tiếng Việt tổ hợp | Unit | `test_normalize_vietnamese_unicode` | Dạng tổ hợp chuyển về dựng sẵn NFC, khớp chính xác chuỗi gốc |
| Chuẩn hóa CRLF / CR về LF | Unit | `test_normalize_line_endings` | Tất cả `\r\n` và `\r` chuyển thành `\n` |
| Làm sạch khoảng trắng & dòng trống thừa | Unit | `test_normalize_whitespace_and_blank_lines` | Không có khoảng trắng đầu/cuối dòng, tối đa 2 dòng trống liên tiếp |
| Thống kê văn bản rỗng | Unit | `test_stats_empty_string` | `character_count=0, word_count=0, line_count=0` |
| Thống kê văn bản nhiều dòng | Unit | `test_stats_multiline_text` | Trả về chính xác số ký tự, số từ, số dòng |
| `POST /api/v1/text/analyze` thành công | Integration | `test_analyze_text_api_success` | Status `200`, trả về đúng schema JSON |
| `POST /api/v1/text/analyze` thiếu trường `text` | Integration | `test_analyze_text_api_missing_field` | Status `400`, error code `INVALID_REQUEST` |
| `POST /api/v1/text/analyze` bảo toàn `X-Correlation-ID` | Integration | `test_analyze_text_api_correlation_id` | Header `X-Correlation-ID` được giữ nguyên từ request |

## 6. Rủi ro và biện pháp giảm thiểu

- **Rủi ro DoS do chuỗi đầu vào quá dài:** Một client có thể gửi chuỗi văn bản hàng trăm megabytes làm cạn kiệt CPU/RAM trong quá trình chuẩn hóa regex.
  - *Biện pháp:* Đặt giới hạn `max_length` trên Pydantic model `TextAnalyzeRequest` (ví dụ: tối đa 1,000,000 ký tự cho endpoint phân tích văn bản trực tiếp).
- **Rủi ro sai lệch số từ giữa các ngôn ngữ:** `text.split()` có thể đếm sai với các ngôn ngữ không dùng dấu cách (tiếng Trung, tiếng Nhật).
  - *Biện pháp:* Ghi rõ trong tài liệu và docstring: Thuật toán thống kê phân từ dựa trên khoảng trắng (POSIX-style whitespace word splitting), tối ưu và phù hợp nhất cho tiếng Việt, tiếng Anh và các ngôn ngữ sử dụng bảng chữ cái Latin.

## 7. Tài liệu cần cập nhật sau khi hoàn thành

- [ ] `docs/development/roadmap.md` (Đánh dấu hoàn thành các checkbox của Phase 1)
- [ ] `docs/development/dev-logs/dev-log-phase-1.md` (Dev log theo template)

## 8. Lệnh xác minh

```powershell
$env:UV_PYTHON = "C:\Users\Admin\AppData\Roaming\uv\python\cpython-3.12.8-windows-x86_64-none\python.exe"
& "C:\Users\Admin\.local\bin\uv.exe" run ruff check .
& "C:\Users\Admin\.local\bin\uv.exe" run ruff format --check .
& "C:\Users\Admin\.local\bin\uv.exe" run pytest
```

