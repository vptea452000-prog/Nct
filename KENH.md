# Hồ sơ kênh

| Hạng mục | Đã chốt |
|---|---|
| Tên hiển thị | **Nct official** (11/2026 từng đổi sang Tuấn Nguyễn rồi quay về Nct official; trước đó là Vox'NCT) |
| Tên, logo trên video | **Không hiện** tên kênh hay logo trong video (chủ kênh dặn 11/2026) |
| Đề tài | Lịch sử, vụ việc có thật lần theo được; mỗi tập trả lời một câu hỏi cụ thể |
| Định dạng | Shorts 9:16, 1080 × 1920, 30 fps; bản dài 16:9 dựng riêng về sau |
| Phong cách hình | Phối ảnh/phim tư liệu thật với đồ họa giấy cắt kiểu Vox; vàng chỉ chi tiết đáng nhìn, đỏ cho đối phương/cảnh báo, navy cho phía Mỹ/đồng minh |
| Âm thanh | Giọng đọc chủ kênh tự thu là chính. **Từ tập sau Midway có hiệu ứng tiếng** (chủ kênh dặn 11/2026), tự tổng hợp bằng `tools/sfx_lib.py`, bám đúng chuyển động trên hình, tự hạ khi có lời, luôn thấp hơn giọng. Không nhạc nền; vẫn tắt tiếng clip tư liệu. Midway v2 giữ nguyên, không hiệu ứng |
| Phong cách dựng mốc | **Midway v2** (chủ kênh chọn 11/11/2026): cắt thẳng theo lời, không thêm chuyển cảnh trượt, chất phim, rung khung hay tô vàng từ khoá trong phụ đề như bản v3 |

Quy trình đầy đủ theo tài liệu "Quy trình sản xuất video" của chủ kênh.

## Quy tắc dùng ảnh (chủ kênh dặn 11/2026, sau lỗi ảnh nhận nhầm là Juan Pujol)

1. **Chỉ dùng ảnh đã xác minh được** người, nơi, thời điểm. Không nhận diện theo kiểu "trông giống".
2. Ảnh nào **chưa chắc chắn thì không đưa vào video**. Claude liệt kê riêng và hỏi chủ kênh trước khi dựng, không tự đoán.
3. Xác minh dựa trên **trang gốc**: cơ quan lưu trữ, bảo tàng (NARA, IWM, Lưu trữ Quốc gia Anh, Bảo tàng Auschwitz, IPN…). Khi gửi ảnh, chủ kênh kèm link trang gốc nếu có. Khi môi trường mở được mạng, Claude tự tra lại.
4. Chú thích trên hình chỉ ghi điều nguồn xác nhận. Không rõ ngày thì không ghi ngày. Ảnh chụp sau sự kiện ghi "chụp sau này". Hiện vật cùng loại (huân chương, vũ khí) ghi rõ là hiện vật cùng loại.
5. Một người không có ảnh xác minh được thì dùng hình bóng trung tính kèm tên, **không mượn ảnh người khác**.
6. Bàn giao luôn có bảng tư liệu: file → nhận diện → nguồn → mức chắc chắn; ảnh bị loại ghi rõ lý do.
