---
name: implement-feature
description: Triển khai một kế hoạch tính năng DocuExtract đã được phê duyệt với các thay đổi Python tập trung, kiểm thử, cập nhật tài liệu API, và xác minh. Sử dụng khi người dùng yêu cầu xây dựng hoặc sửa đổi một tính năng.
---

# Triển Khai Tính Năng

## Điều kiện tiên quyết
- Đọc `AGENTS.md` và các tài liệu liên quan.
- Xác định kế hoạch đã được phê duyệt hoặc xác nhận rằng người dùng đã yêu cầu rõ ràng triển khai nhiệm vụ được mô tả.
- Kiểm tra Git status/diff và phần triển khai hiện tại. Bảo toàn các thay đổi không liên quan của người dùng.

## Quy trình
1. Nêu lại kết quả và phạm vi được chấp nhận; xác định xung đột với code/tài liệu hiện tại.
2. Triển khai từng phần dọc (vertical slice) một lần. Giữ trách nhiệm của route, schema, service, và parser riêng biệt.
3. Thêm hoặc cập nhật kiểm thử song song với hành vi.
4. Giữ việc thêm dependency ở mức tối thiểu và giải thích lý do cần thiết.
5. Xử lý các lỗi parser/input dự kiến bằng các kiểu lỗi ứng dụng ổn định và ánh xạ API.
6. Cập nhật tài liệu API contract, requirements, setup, hoặc ADR khi hành vi hoặc kiến trúc thay đổi.
7. Chạy kiểm thử có mục tiêu, bộ kiểm thử đầy đủ khi thực tế, và kiểm tra Ruff khi được cấu hình.
8. Kiểm tra diff cuối cùng để phát hiện định dạng không cố ý, chỉnh sửa không liên quan, secrets bị lộ, và kiểm thử còn thiếu.

## Điều kiện dừng
Dừng lại và báo cáo thay vì ứng biến khi:
- Kế hoạch đã phê duyệt mâu thuẫn với cấu trúc hoặc hành vi thực tế của dự án.
- Cần thay đổi API gây phá vỡ tương thích hoặc mở rộng kiến trúc nhưng chưa được phê duyệt.
- Có liên quan đến thao tác phá hoại, credential thực, tài khoản bên ngoài, hoặc môi trường production.
- Xác minh phát hiện lỗi không thể giải thích hoặc sửa chữa an toàn trong phạm vi.

## Bàn giao
Báo cáo các file đã triển khai, các lựa chọn thiết kế quan trọng, lệnh/kết quả kiểm thử thực tế, giới hạn, và cách ngắn nhất để thử tính năng. Không tuyên bố các kiểm tra chưa chạy là đã thành công.
