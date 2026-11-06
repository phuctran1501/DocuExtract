# Hướng Dẫn Cài Đặt Môi Trường Phát Triển

> File này ghi lại baseline cài đặt dự kiến. Hãy điều chỉnh các lệnh phù hợp với package manager và các file project thực tế sau khi repository được khởi tạo.

## 1. Yêu cầu tiên quyết

- Git
- Python 3.12 trở lên
- `uv` để quản lý Python project/dependency (được khuyến nghị cho dự án này)
- Antigravity với workspace được mở tại thư mục gốc của repository

## 2. Khởi tạo Python project (chỉ lần cài đặt đầu tiên)

Nếu repository chưa có `pyproject.toml`:

```bash
uv init --python 3.12
```

Nếu `pyproject.toml` đã tồn tại, không chạy lại `uv init`. Hãy kiểm tra file đó và giữ nguyên cài đặt package manager hiện tại.

## 3. Thêm các dependency ban đầu

```bash
uv add fastapi "uvicorn[standard]" pydantic-settings python-multipart pypdf python-docx
uv add --dev pytest httpx ruff
uv sync
```

Chỉ thêm các dependency mà milestone hiện tại thực sự cần. Ví dụ, `python-multipart` cần thiết cho FastAPI multipart uploads; các parser tài liệu cần thiết khi triển khai phân tích PDF/DOCX.

## 4. Chạy API

Sau khi điểm vào ứng dụng tồn tại:

```bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Mở tài liệu API được tạo tự động tại `http://127.0.0.1:8000/docs` và health endpoint tại `http://127.0.0.1:8000/health` khi đã được triển khai.

## 5. Chạy các kiểm tra

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Để format file một cách có chủ đích:

```bash
uv run ruff format .
```

Hãy xem lại diff sau khi format; không format các file không liên quan.

## 6. Biến môi trường

Chỉ tạo file `.env` cục bộ khi các cài đặt yêu cầu. Commit file `.env.example` với các giá trị placeholder và thêm `.env` vào `.gitignore`. Không bao giờ đặt API key, mật khẩu, JWT secret hay URL riêng tư vào các file Markdown được theo dõi bởi Git.

## 7. Docker (milestone sau)

Các lệnh Docker nên được thêm vào sau khi Dockerfile và cấu hình compose tồn tại. Không hướng dẫn cộng tác viên chạy các lệnh không có trong repository. Tránh các lệnh reset volume mang tính phá hủy dữ liệu trừ khi người dùng có chủ ý xóa dữ liệu cục bộ.
