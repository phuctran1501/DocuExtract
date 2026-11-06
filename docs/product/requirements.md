# DocuExtract — Yêu Cầu

**Trạng thái:** Baseline đề xuất cho MVP đầu tiên. Cập nhật tài liệu này khi phạm vi sản phẩm thay đổi.

## 1. Các tác nhân

- **API Consumer:** một ASP.NET Core API hoặc dịch vụ nội bộ đáng tin cậy khác gửi tài liệu để trích xuất.
- **Operator/Developer:** chạy, cấu hình, quan sát và kiểm thử DocuExtract.

Không có tài khoản người dùng cuối hay giao diện tự phục vụ công khai trong MVP.

## 2. Yêu cầu chức năng

| ID    | Yêu cầu                                                                                                              | Mức độ ưu tiên |
| ----- | -------------------------------------------------------------------------------------------------------------------- | -------------- |
| FR-01 | Service cung cấp một health endpoint.                                                                                | Must           |
| FR-02 | Service chấp nhận file PDF và trích xuất văn bản.                                                                    | Must           |
| FR-03 | Service chấp nhận file DOCX và trích xuất văn bản.                                                                   | Must           |
| FR-04 | Service trả về metadata tên file, loại media được phát hiện, kích thước byte, văn bản trích xuất, số ký tự và số từ. | Must           |
| FR-05 | Service từ chối các loại file không được hỗ trợ với một mã lỗi ổn định.                                              | Must           |
| FR-06 | Service từ chối các file vượt quá giới hạn kích thước có thể cấu hình.                                               | Must           |
| FR-07 | Service xử lý các tài liệu bị lỗi, rỗng và được mã hóa mà không bị crash.                                            | Must           |
| FR-08 | Service chuẩn hóa văn bản trích xuất theo các quy tắc xác định được tài liệu hóa.                                    | Should         |
| FR-09 | Service báo cáo khi tài liệu không có văn bản có thể trích xuất; không giả vờ thực hiện OCR.                         | Must           |
| FR-10 | Service cung cấp một endpoint tùy chọn cho thống kê văn bản cơ bản.                                                  | Could          |

## 3. Yêu cầu phi chức năng

### NFR-01 — Bảo mật

- Các byte được tải lên và nội dung tài liệu là input không đáng tin cậy.
- Thực thi kích thước tối đa và các định dạng được hỗ trợ.
- Không tin tưởng MIME type hoặc tên file do client cung cấp là bằng chứng về loại file.
- Không bao giờ ghi log văn bản trích xuất hoặc secret.
- Không trả về stack trace hoặc đường dẫn nội bộ.

### NFR-02 — Độ tin cậy

- Một tài liệu lỗi phải thất bại dưới dạng lỗi ở cấp độ request, không làm crash tiến trình service.
- Mọi lỗi mong đợi đều phải được ánh xạ tới một mã lỗi được tài liệu hóa.
- Dọn dẹp tài nguyên tạm thời khi thành công và thất bại nếu file tạm thời được sử dụng.

### NFR-03 — Hiệu năng

- MVP nhắm tới các tài liệu nhỏ trong giới hạn upload đã cấu hình.
- Thiết lập baseline trước khi thêm concurrency, queue hoặc hệ thống worker.
- Tránh đọc không giới hạn và kích thước response không giới hạn.

### NFR-04 — Khả năng bảo trì

- Tách biệt HTTP route, schema, service và parser theo định dạng cụ thể.
- Sử dụng type hint và schema rõ ràng.
- Test parser độc lập với HTTP route.

### NFR-05 — Khả năng tương tác

- Sử dụng REST endpoint có phiên bản và response JSON.
- Giữ ổn định tên trường API và mã lỗi.
- Tài liệu hóa tên trường multipart, content type, giới hạn kích thước và status code.

### NFR-06 — Khả năng vận hành

- Cấu hình đến từ biến môi trường/settings.
- Cung cấp health visibility và structured log.
- Cung cấp hướng dẫn cài đặt cục bộ có thể tái tạo và hướng dẫn Docker khi containerization được triển khai.

## 4. Giới hạn và chính sách ban đầu

| Cài đặt         | Chính sách ban đầu                                                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Giới hạn upload | Mặc định 10 MiB; có thể cấu hình                                                                                                     |
| Định dạng       | Chỉ `.pdf`, `.docx`                                                                                                                  |
| OCR             | Không được hỗ trợ trong MVP                                                                                                          |
| Lưu trữ         | Không có lưu trữ upload lâu dài                                                                                                      |
| Phiên bản API   | `/api/v1`                                                                                                                            |
| Health          | `/health`                                                                                                                            |
| Xác thực        | Mạng nội bộ đáng tin cậy cho MVP cục bộ; xác thực service-to-service cho production phải được thiết kế trước khi expose ra bên ngoài |

Các giá trị này là mặc định cho việc lập kế hoạch triển khai. Bất kỳ triển khai production nào cũng phải xem xét lại giới hạn upload, kiểm soát truy cập, rate limit, timeout và giới hạn tài nguyên.

## 5. Tiêu chí chấp nhận cho extraction slice đầu tiên

- Một PDF có văn bản hợp lệ trả về văn bản trích xuất không rỗng và metadata đúng.
- Một DOCX hợp lệ trả về văn bản đoạn văn/bảng theo các quy tắc trích xuất được tài liệu hóa.
- Một file bị đổi tên hoặc không được hỗ trợ bị từ chối khi nội dung thực tế của nó không khớp với định dạng được phép.
- Một upload quá kích thước bị từ chối mà không đọc payload không giới hạn vào bộ nhớ.
- Một tài liệu bị lỗi, được mã hóa hoặc rỗng trả về lỗi/cảnh báo có thể dự đoán được.
- Test bao phủ cả trường hợp thành công và thất bại.
- Tài liệu API mô tả response thực tế và contract lỗi.
