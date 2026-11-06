# ADR-001: Giữ bản phát hành đầu tiên của DocuExtract không có trạng thái (stateless)

- **Trạng thái:** Đã chấp thuận cho MVP
- **Ngày:** 2026-11-05
- **Người ra quyết định:** Chủ dự án

## Bối cảnh

Mục tiêu đầu tiên là học Python/FastAPI và chứng minh một ranh giới xử lý tài liệu hữu ích cho ASP.NET Core. Việc thêm storage, queue, hoặc database sẽ làm tăng khối lượng thiết lập và vận hành trước khi hành vi trích xuất được xác thực.

## Quyết định

MVP xử lý một upload trong vòng đời request và trả về văn bản đã trích xuất cùng metadata. Nó không lưu trữ file đã upload hoặc văn bản đã trích xuất. Service không sở hữu các business entity, tài khoản người dùng, hoặc dữ liệu ứng dụng.

## Hệ quả

**Tích cực**
- Ít thành phần hơn và thiết lập cục bộ đơn giản hơn.
- Kiểm thử dễ dàng hơn và hành vi có thể tái tạo.
- Quyền sở hữu rõ ràng: ứng dụng ASP.NET Core lưu trữ dữ liệu nghiệp vụ khi thích hợp.

**Tiêu cực / hạn chế**
- Các tài liệu lớn hoặc xử lý chậm có thể giữ một HTTP request mở lâu.
- Kết quả không thể phục hồi từ DocuExtract sau khi response bị mất.
- Giới hạn bộ nhớ/CPU và timeout request phải được xem xét.

## Xem xét lại khi

- Các tài liệu thường xuyên vượt quá ngân sách xử lý đồng bộ.
- Kết quả phải tồn tại khi caller ngắt kết nối hoặc cần được poll sau.
- Nhiều consumer cần trạng thái xử lý chung.
- Thông lượng yêu cầu mô hình worker/queue chuyên dụng.

Bất kỳ thay đổi nào cũng nên so sánh xử lý đồng bộ, FastAPI background tasks, và kiến trúc queue/worker chuyên dụng dựa trên nhu cầu đã được đo lường.
