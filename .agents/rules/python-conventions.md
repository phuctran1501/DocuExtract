---
trigger: glob
globs: "**/*.py, **/*_test.py"
description: Quy ước về Python style, typing, cài đặt FastAPI, và khả năng bảo trì.
---

# Quy Ước Python

- Tuân theo phiên bản Python và package manager của repository; không được thay đổi một trong hai một cách thầm lặng.
- Sử dụng type hints cho các hàm public và ranh giới module. Ưu tiên các return type rõ ràng.
- Sử dụng Pydantic models cho structured API input/output; giữ cho parser internals độc lập với FastAPI.
- Chỉ sử dụng `async def` khi await async I/O hoặc async dependencies. Không tự động coi CPU-bound parsing là bất đồng bộ.
- Giữ cho các hàm tập trung và side effects hiển thị. Tránh mutable module globals và import-time work.
- Bắt các exception cụ thể được mong đợi. Không bao giờ nuốt exception hoặc trả về dữ liệu fallback có dạng thành công sau một lần thất bại.
- Ưu tiên các tính năng standard-library và các dependencies hiện có. Giải thích bất kỳ dependency mới nào.
- Giữ cho route handlers gọn nhẹ; đặt document parsing trong `app/parsers/` và processing orchestration trong `app/services/`.
- Tuân theo cấu hình Ruff nếu có. Không reformat các file không liên quan.
