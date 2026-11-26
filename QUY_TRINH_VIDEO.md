# Quy trình làm video (định dạng tài liệu – kể chuyện, 16:9) — chốt 20/11/2026

1. **Cùng viết kịch bản** — chủ kênh đưa chủ đề (có thể kèm kịch bản tham khảo); Claude viết, hai bên sửa tới khi chốt.
   Giọng văn mềm, liền mạch, đủ từ nối; khoảng 6 phút ≈ 1.600–1.700 chữ. File `<tap>/KICH_BAN.md`.
   Claude lập `<tap>/NGUON.md`: mã khung hình, hình cần tìm, từ khóa, nguồn gợi ý (chữ/số liệu/bản đồ động thì tự tạo).
2. **Chủ kênh gửi file ảnh** (tải bản gốc, nén zip; tên file tùy ý). Claude tự nhận diện, gán vào mã khung hình,
   báo lại khung còn thiếu / ảnh nghi sai — không đoán khi chưa chắc.
3. **Chủ kênh gửi file voice** (1 file).
4. **Claude dựng toàn bộ, tập trung tối đa cho hấp dẫn, bắt mắt**: căn câu theo giọng; tranh lia/zoom có chiều sâu (tách lớp,
   ánh sáng, hạt phim); bản đồ động (đường hành quân, vùng tô màu, nhãn tiếng Việt); thẻ chữ, trích dẫn, số liệu; chuyển cảnh;
   hiệu ứng tiếng; nhịp vừa phải, nhanh và mạnh ở cao trào; xuất 16:9 −14 LUFS. Bàn giao video + tiêu đề, mô tả, mốc thời gian.

Không dùng cảnh phim — dựng bằng tranh, ảnh và bản đồ. Chủ kênh tự xử lý bản quyền; hình phải đúng người/sự kiện.

## Phong cách hình ảnh (chủ kênh dặn 20/11/2026)
- **Intro cuốn hút ngay từ những giây đầu:** mở bằng hình mạnh nhất + câu móc (hook), vào thẳng xung đột/câu hỏi, không dạo đầu dài; tiêu đề hiện sớm, gọn.
- **Hiệu ứng đơn giản nhưng sang, không rối:** lia/zoom chậm và êm, chuyển cảnh mờ/đẩy nhẹ, chữ ít và đẹp (một kiểu chữ, căn đều, nhiều khoảng trống),
  tông màu thống nhất, ánh sáng tinh tế; không dồn nhiều hiệu ứng cùng lúc, không chữ nhảy loạn, không màu chói.

## Quy tắc dựng đã chốt (từ góp ý Alexander v2)
- Bản đồ: dùng bản đồ thật có nguồn (ảnh vệ tinh NASA Blue Marble / Wikimedia Commons), ghi nguồn trong mô tả.
- Bản đồ không kẻ đường nối/tuyến hành quân, chỉ hiện tên địa danh đúng lúc giọng đọc nhắc tới.
- Chữ to giữa màn hình khi có từ quan trọng: năm, tên riêng, địa điểm, con số (canh theo thời điểm từng chữ trong voice).
- Camera: mỗi ảnh chỉ zoom dứt khoát một hướng (vào hoặc ra), tốc độ đều, không lia qua lại; các ảnh liền nhau đổi chiều xen kẽ.
- Kịch bản tiếp theo giữ phong cách như kịch bản Alexander (kể liền mạch, câu trọn vẹn, có từ nối).

## Căn giọng đọc (từ tập Hitler)
- Dùng Whisper (`tools/asr.py <tập>`, chạy với `HF_HUB_DISABLE_XET=1`) để lấy thời điểm từng chữ, rồi `tools/align_asr.py <tập>` ghép với kịch bản. Không dùng cách đếm âm tiết cũ nữa.
- Luôn kiểm tra thứ tự câu trong file giọng so với kịch bản. **Không cắt ghép giọng của chủ kênh.** Nếu giọng đọc lệch thứ tự, giữ nguyên giọng và cho hình chạy theo câu đang đọc (`audio/segments.json`), đồng thời báo chủ kênh để xuất lại giọng nếu muốn đúng mạch.
