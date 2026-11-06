---
name: review-change
description: Đánh giá Git diff hiện tại của DocuExtract về tính đúng đắn, bảo mật, tương thích API, chất lượng kiểm thử, và khả năng bảo trì. Sử dụng trước khi chấp nhận hoặc merge các thay đổi.
---

# Đánh Giá Thay Đổi

## Quy trình
1. Đọc `AGENTS.md`, requirements/API contract/ADR liên quan, và Definition of Done.
2. Kiểm tra `git status` và diff đầy đủ, bao gồm các file chưa được theo dõi khi có thể.
3. Truy vết code đã thay đổi qua các caller, schema, parser, và kiểm thử.
4. Tìm kiếm: lỗi đúng đắn, edge case, xử lý file không an toàn, công việc blocking trong async path, rò rỉ tài nguyên, xử lý exception quá rộng, API response không ổn định, và kiểm thử còn thiếu.
5. Kiểm tra thay đổi dependency, giá trị mặc định cấu hình, log, lộ secret, và drift tài liệu.
6. Chỉ chạy xác minh tập trung khi phạm vi đánh giá và môi trường cho phép; phân biệt phát hiện tĩnh với kiểm tra đã thực thi.

## Định dạng đầu ra
Liệt kê các phát hiện trước, theo thứ tự mức độ nghiêm trọng:
- **Critical / High / Medium / Low**
- Tham chiếu file và dòng.
- Tình huống lỗi cụ thể.
- Lý do quan trọng.
- Khuyến nghị sửa chữa.

Sau đó báo cáo bằng chứng kiểm thử/lệnh, nhận xét không cản trở, và các khu vực không thể xác minh. Nếu không xác định được phát hiện nào, hãy nói rõ và nêu những gì đã được đánh giá. Không sửa đổi file trừ khi người dùng yêu cầu rõ ràng.
