---
name: integrate-aspnet
description: Thiết kế hoặc đánh giá ranh giới giữa DocuExtract và một ứng dụng ASP.NET Core Clean Architecture, bao gồm typed HttpClient, ánh xạ API contract, timeout, cancellation, và xử lý lỗi downstream.
---

# Tích Hợp ASP.NET Core

## Mục tiêu
Giữ DocuExtract độc lập trong khi đảm bảo HTTP contract của nó an toàn và dễ sử dụng cho ứng dụng ASP.NET Core.

## Quy trình
1. Đọc `docs/architecture/api-contract.md` và xác nhận nó khớp với OpenAPI schema đã triển khai.
2. Xác định use case .NET cần extraction và các trường request/response chính xác mà nó sử dụng.
3. Định nghĩa abstraction tầng Application như `IDocumentExtractor`; giữ `HttpClient`, multipart construction, và JSON transport trong tầng Infrastructure.
4. Sử dụng typed `HttpClient` được đăng ký thông qua dependency injection.
5. Truyền `CancellationToken` từ ranh giới API/request đến lời gọi HTTP ra ngoài.
6. Cấu hình timeout rõ ràng và ánh xạ riêng biệt: lỗi mạng, timeout, HTTP response không thành công, JSON không hợp lệ, và mã lỗi DocuExtract đã biết.
7. Bảo toàn hoặc tạo correlation ID và đưa vào log trên cả hai service mà không ghi log nội dung tài liệu.
8. Xem xét kích thước upload, request streaming, kích thước response, retry, và xác thực service. Không giới thiệu retry tự động mà không phân tích hành vi timeout/idempotency.
9. Đề xuất các kiểm thử contract/integration, bao gồm một response lỗi có kiểm soát.

## Ràng buộc kiến trúc
- ASP.NET Core sở hữu validation nghiệp vụ, authorization, workflow, và lưu trữ dữ liệu nghiệp vụ.
- Tầng Application phụ thuộc vào abstraction, không phụ thuộc vào FastAPI hoặc chi tiết transport.
- Tầng Infrastructure sở hữu chi tiết triển khai HTTP.
- Không thêm code .NET vào repository DocuExtract trừ khi được yêu cầu rõ ràng.
- Không chia sẻ database giữa hai service.

## Đầu ra
Cung cấp ánh xạ request/response, phác thảo C# interface/DTO/client-registration, ánh xạ lỗi, yêu cầu cấu hình, và các trường hợp kiểm thử integration. Giải thích các lựa chọn .NET không rõ ràng bằng tiếng Việt cho developer biết C# nhưng đang học Python.
