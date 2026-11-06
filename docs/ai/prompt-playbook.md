# Gemini + Antigravity Prompt Playbook

Dùng một nhiệm vụ giới hạn rõ ràng cho mỗi prompt. Để các instruction trong repository và các skill chứa các quy tắc lặp lại; prompt chỉ cần mô tả kết quả mong muốn và các ràng buộc.

## 1. Cuộc hội thoại đầu tiên trong workspace mới

```text
Đọc AGENTS.md và bản đồ tài liệu trong README.md. Kiểm tra toàn bộ cây thư mục repository, trạng thái Git hiện tại, cấu hình project Python, và các test hiện có. Chưa sửa đổi bất kỳ file nào. Báo cáo:
1. Những gì đã có và những gì còn thiếu.
2. Liệu implementation có khớp với tài liệu product và architecture không.
3. Milestone đầu tiên nhỏ nhất và hữu ích nhất.
4. Các rủi ro hoặc giả định mâu thuẫn.
Không tự bịa code hoặc khẳng định đã chạy lệnh nào đó nếu chưa thực sự chạy.
```

## 2. Lên kế hoạch cho một feature

```text
Dùng skill plan-feature. Tôi muốn implement: [mô tả một kết quả cụ thể].
Kiểm tra implementation hiện tại trước. Đọc các requirements và API contract liên quan. Tạo một plan với scope/non-goals, files, API changes, các bước theo thứ tự, tests, security risks, và documentation updates. Chưa thay đổi source code.
```

## 3. Implement một plan đã được phê duyệt

```text
Dùng skill implement-feature. Implement plan đã phê duyệt: [đường dẫn đến plan hoặc dán nội dung plan].
Giữ diff tập trung, thêm tests cho cả trường hợp thành công và thất bại, cập nhật API contract nếu hành vi thay đổi, và chạy các kiểm tra liên quan. Dừng lại và báo cáo nếu plan mâu thuẫn với repository hoặc yêu cầu một quyết định kiến trúc quan trọng.
```

## 4. Debug một lỗi

```text
Tái hiện và chẩn đoán lỗi này trước khi thay đổi code: [error, command, steps].
Truy vết luồng request/data, xác định nguyên nhân gốc rễ có khả năng nhất, và phân biệt bằng chứng với giả thuyết. Đề xuất bản fix nhỏ nhất và an toàn nhất cùng regression test. Không được suppress exception hoặc làm yếu tests chỉ để lệnh chạy xanh.
```

## 5. Review trước khi chấp nhận một thay đổi

```text
Dùng skill review-change. Review Git diff hiện tại với vai trò senior Python backend reviewer. Ưu tiên correctness, API compatibility, upload security, async/blocking behavior, error handling, tests, và phạm vi ngoài ý muốn. Báo cáo kết quả theo mức độ nghiêm trọng kèm tham chiếu file/dòng. Không sửa file trừ khi tôi yêu cầu sửa các phát hiện đó.
```

## 6. Chuẩn bị tích hợp ASP.NET Core

```text
Dùng skill integrate-aspnet. Dựa trên docs/architecture/api-contract.md, thiết kế .NET integration boundary cho một ứng dụng ASP.NET Core Clean Architecture. Giữ Application layer độc lập với HTTP transport và đặt typed HttpClient adapter trong Infrastructure. Bao gồm timeout, CancellationToken, correlation ID, response mapping, và xử lý downstream failure. Không thêm .NET source files vào repository này trừ khi tôi yêu cầu rõ ràng.
```

## 7. Yêu cầu giải thích để học

```text
Giải thích implementation bằng tiếng Việt như thể tôi biết C#/.NET nhưng còn mới với Python. So sánh các khái niệm Python/FastAPI liên quan với các khái niệm C#/.NET quen thuộc. Giải thích luồng request, các trade-off quan trọng, và những gì tôi nên tự kiểm tra hoặc test. Không viết lại code chỉ để minh họa một style khác.
```

## 8. Quy trình vận hành hữu ích

1. Yêu cầu reconnaissance repository.
2. Yêu cầu plan cho công việc medium/large.
3. Phê duyệt hoặc sửa đổi plan.
4. Implement một vertical slice.
5. Review diff và kết quả test.
6. Cập nhật docs/dev log.
7. Commit chỉ sau khi owner chấp nhận kết quả.
