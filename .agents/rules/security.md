---
trigger: model_decision
description: Áp dụng khi xử lý các file tải lên, nội dung tài liệu, secrets, logging, cấu hình, network exposure, hoặc các error paths nhạy cảm về bảo mật.
---

# Quy Tắc Bảo Mật

- Coi uploaded bytes, filenames, MIME types, và document contents là không đáng tin cậy.
- Thực thi giới hạn kích thước file có thể cấu hình trước khi đọc không giới hạn. Xác thực extension và nội dung/signature thực tế; không tin tưởng client headers một mình.
- Không bao giờ sử dụng uploaded filename làm filesystem path. Sử dụng server-generated temporary names và đảm bảo cleanup nếu cần dùng đến disk.
- Không log document text, file bytes, credentials, tokens, hoặc raw multipart bodies.
- Trả về các error message an toàn, ổn định; giữ các chi tiết chẩn đoán trong protected server logs.
- Tránh các loại file không bị giới hạn, decompression bombs, unbounded parsing, và uncontrolled response sizes.
- Không tuyên bố hỗ trợ OCR cho scanned documents trừ khi có OCR implementation và tests tồn tại.
- Không bao giờ commit secrets hoặc các giá trị `.env` thực. Việc tiếp xúc production yêu cầu service-to-service authentication và network controls.
