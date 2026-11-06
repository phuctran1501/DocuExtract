---
trigger: model_decision
description: Áp dụng khi thêm hoặc thay đổi tests, hành vi parser, API endpoints, error handling, hoặc CI verification.
---

# Quy Tắc Testing

- Test hành vi pure normalization và parser độc lập với HTTP routes khi có thể.
- Đối với các endpoint, bao gồm: thành công, input không hợp lệ, định dạng không được hỗ trợ, upload quá kích thước, input bị lỗi/mã hóa, và ánh xạ lỗi không mong đợi khi liên quan.
- Sử dụng các fixture nhỏ, xác định; không commit các tài liệu private hoặc người dùng thực.
- Kiểm tra response schema, status code, và stable error code — không chỉ kiểm tra rằng request không bị crash.
- Chạy test liên quan nhất trước, sau đó chạy bộ test rộng hơn khi có thể.
- Chạy Ruff lint và format checks khi được cấu hình.
- Báo cáo các lệnh và kết quả chính xác. Nêu rõ khi nào một lần kiểm tra không được chạy.
- Không bao giờ xóa/bỏ qua/nới lỏng một test chỉ để có được một build xanh.
