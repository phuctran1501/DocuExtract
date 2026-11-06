# DocuExtract — Tầm nhìn sản phẩm (Product Vision)

## 1. Vấn đề

Các hệ thống ASP.NET Core đôi khi cần khả năng xử lý tài liệu chuyên biệt—ví dụ như đọc CV của ứng viên hoặc trích xuất văn bản từ file PDF do người dùng tải lên. Việc triển khai mọi parser và thư viện xử lý văn bản ngay bên trong backend chính có thể làm tăng độ phụ thuộc lẫn nhau (coupling) và khiến việc phát triển độc lập các xử lý chuyên biệt này trở nên khó khăn hơn.

## 2. Tầm nhìn sản phẩm

DocuExtract là một dịch vụ Python nhỏ gọn, có thể deploy độc lập, tiếp nhận các tài liệu được hỗ trợ và trả về văn bản đã được trích xuất, chuẩn hóa cùng các siêu dữ liệu (metadata) cơ bản thông qua một HTTP API ổn định.

## 3. Đối tượng sử dụng mục tiêu

- Các Web API ASP.NET Core áp dụng kiến trúc Clean Architecture.
- Các dịch vụ nội bộ cần trích xuất văn bản từ tài liệu một cách xác định (deterministic).
- Các dự án học tập cần một ranh giới dịch vụ thực tế bằng Python/FastAPI.

## 4. Giá trị cốt lõi

- Trách nhiệm duy nhất: trích xuất tài liệu và xử lý văn bản nhẹ nhàng.
- API contract ổn định, có phân phiên bản.
- Xử lý an toàn các file tải lên không đáng tin cậy.
- Dễ dàng chạy cục bộ và đóng gói bằng Docker.
- Kiểm thử và triển khai độc lập.

## 5. Phạm vi MVP

**Trong phạm vi**
- Trích xuất văn bản từ PDF.
- Trích xuất văn bản từ DOCX.
- Chuẩn hóa văn bản và thống kê cơ bản.
- Xác thực file và phản hồi lỗi nhất quán.
- Health endpoint, kiểm thử tự động, và tài liệu OpenAPI.
- Hướng dẫn tích hợp HTTP cho ASP.NET Core.

**Ngoài phạm vi cho đến khi được phê duyệt rõ ràng**
- OCR cho tài liệu scan/chỉ có hình ảnh.
- Đọc hiểu CV, tóm tắt hoặc chấm điểm dựa trên LLM.
- Tài khoản người dùng, cấp phát JWT, vai trò và phân quyền.
- Lưu trữ tài liệu bền vững hoặc database ứng dụng.
- Cơ sở hạ tầng hàng đợi/worker và điều phối phân tán.
- Giao diện người dùng (Frontend/UI).

## 6. Các nguyên tắc sản phẩm

1. Giữ dịch vụ không trạng thái (stateless) cho đến khi việc lưu trữ dữ liệu thực sự cần thiết.
2. Đảm bảo việc trích xuất mang tính xác định (deterministic) và có thể kiểm thử được.
3. Coi mọi tài liệu tải lên là dữ liệu đầu vào không đáng tin cậy (untrusted input).
4. Trả về mã lỗi có thể đọc bằng máy, không trả về stack trace.
5. Giữ quyền sở hữu nghiệp vụ tại hệ thống ASP.NET Core gọi đến.
6. Ưu tiên một lát cắt chức năng hoàn chỉnh (vertical slice) hoạt động được và quan sát được thay vì cơ sở hạ tầng suy đoán.
7. Đưa ra các lựa chọn kỹ thuật dễ hiểu cho người mới bắt đầu học Python.

## 7. Tiêu chí thành công

MVP thành công khi bên gọi có thể gửi một file PDF hoặc DOCX hợp lệ, nhận về văn bản trích xuất cùng metadata, nhận mã lỗi rõ ràng khi đầu vào không hợp lệ hoặc không được hỗ trợ, và có thể kiểm thử hành vi mà không cần kết nối với database hay nhà cung cấp AI bên ngoài nào.
