# Định Nghĩa Hoàn Thành (Definition of Done)

Một tính năng được coi là hoàn thành chỉ khi tất cả các mục áp dụng dưới đây được thỏa mãn.

## Yêu cầu
- [ ] User story/vấn đề và tiêu chí chấp nhận đã rõ ràng.
- [ ] Phạm vi và những gì nằm ngoài phạm vi đã được xác định rõ.
- [ ] Hành vi hiện tại và code liên quan đã được kiểm tra.

## Triển khai
- [ ] Thay đổi tuân theo kế hoạch đã được phê duyệt.
- [ ] Route handler giữ ở mức mỏng; logic phân tích cú pháp nằm ngoài HTTP route.
- [ ] Type và Pydantic schema được sử dụng tại ranh giới service/API.
- [ ] Không thêm dependency suy đoán hoặc refactor không liên quan.
- [ ] Các trường hợp lỗi có chủ đích và có thể đọc được bởi máy.

## Bảo mật
- [ ] Kích thước upload và nội dung được hỗ trợ đã được xác thực.
- [ ] Tên file/MIME type do client cung cấp không được tin tưởng mù quáng.
- [ ] Không có secret hoặc nội dung tài liệu được ghi vào log.
- [ ] Không để lộ stack trace/đường dẫn nội bộ ra phía client.
- [ ] File/resource tạm thời được dọn sạch nếu có sử dụng.

## Kiểm thử và xác minh
- [ ] Unit test bao phủ logic xử lý đã thay đổi.
- [ ] API test bao phủ các status code và response schema liên quan.
- [ ] Các trường hợp biên và trường hợp lỗi được bao phủ.
- [ ] Lệnh pytest liên quan chạy thành công.
- [ ] Kiểm tra lint/format của Ruff thành công khi đã cấu hình.
- [ ] Bất kỳ test nào không chạy phải được công bố rõ ràng.

## Tài liệu
- [ ] API contract và hành vi OpenAPI nhất quán với nhau.
- [ ] Tài liệu setup/cấu hình được cập nhật khi cần.
- [ ] Roadmap/requirements/ADR được cập nhật nếu phạm vi hoặc kiến trúc thay đổi.
- [ ] Thêm learning/dev log khi thay đổi giới thiệu một khái niệm quan trọng.

## Bàn giao cuối cùng
- [ ] Tóm tắt nêu rõ các file đã thay đổi và hành vi mới.
- [ ] Lệnh kiểm thử và kết quả thực tế được báo cáo.
- [ ] Các hạn chế và rủi ro còn lại được công bố.
- [ ] Người dùng có thể chạy hoặc xác minh tính năng bằng hướng dẫn được cung cấp.
