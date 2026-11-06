---
name: plan-feature
description: Kiểm tra repository DocuExtract và tạo kế hoạch triển khai cho tính năng mới, endpoint, refactor, dependency, hoặc thay đổi kiến trúc. Sử dụng trước các tác vụ coding ở mức trung bình hoặc lớn.
---

# Lập Kế Hoạch Tính Năng

## Mục tiêu
Tạo kế hoạch triển khai dựa trên bằng chứng mà không thay đổi mã nguồn ứng dụng.

## Quy trình
1. Đọc `AGENTS.md`, các yêu cầu sản phẩm liên quan, kiến trúc, API contract, ADR, và Definition of Done.
2. Kiểm tra cây thư mục repository, Git status/diff hiện tại, cấu hình dependency, các file nguồn liên quan, và kiểm thử.
3. Truy vết luồng request/data hiện có. Tìm kiếm code có thể tái sử dụng trước khi đề xuất module mới.
4. Phân tách các sự kiện đã xác nhận khỏi các giả định. Nếu một chi tiết còn thiếu không cản trở kế hoạch an toàn, hãy nêu một giả định hợp lý thay vì đặt câu hỏi rộng.
5. Xác định kết quả hiển thị với người dùng, công việc trong phạm vi, và các non-goal rõ ràng.
6. Xác định các thay đổi API/schema/cấu hình và tính tương thích ngược.
7. Liệt kê các bước triển khai theo thứ tự với các module/file dự kiến sẽ thay đổi.
8. Xác định các kiểm thử positive, negative, boundary, và regression.
9. Đánh giá các rủi ro bảo mật, tài nguyên, concurrency, và vận hành.
10. Xác định các cập nhật tài liệu và ADR.

## Đầu ra
Viết hoặc trình bày kế hoạch sử dụng `docs/development/implementation-plan-template.md`. Với tác vụ được theo dõi, lưu dưới `docs/development/plans/` với tên file mô tả. Không tạo thư mục trừ khi cần thiết.

Kết thúc bằng:
- Thứ tự triển khai được khuyến nghị.
- Các quyết định quan trọng cần chủ sở hữu phê duyệt.
- Những gì sẽ không được xây dựng.

Không chỉnh sửa mã nguồn ứng dụng trong skill này. Nếu người dùng yêu cầu rõ ràng lập kế hoạch và triển khai trong cùng một tác vụ, hãy trình bày kế hoạch trước trong tương tác và chỉ tiến hành trong phạm vi ủy quyền rõ ràng đó.
