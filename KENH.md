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

## Phong cách hình từ tập Onoda (chủ kênh chốt 16/11/2026)

Thay phong cách giấy cắt (Midway v2) bằng **hoạt hình 2D**, theo bản thử `onoda/proto/` và bộ vẽ `onoda/proto/src/toon.py`:

- **Linh vật kênh**: nhân vật tròn màu vàng, kính tròn, khăn đỏ (xem `brand/`). Đóng vai người dẫn chuyện phản ứng với câu chuyện (tò mò, hoảng hốt, chỉ tay…). Hài nhẹ, dồn vào linh vật; đề tài có người chết thì tiết chế.
- **Nhân vật lịch sử vẽ hoạt hình đơn giản**, nét viền dày, tô phẳng có đổ bóng; không vẽ mô phỏng khuôn mặt người thật theo ảnh. Nhãn "HOẠT HÌNH MINH HỌA" khi cần.
- **Bối cảnh có chiều sâu**: tiền cảnh mờ, máy quay đẩy vào, lia, cận mặt khi phản ứng; ánh sáng ấm, góc tối.
- **Chữ lớn viền đậm** trên dải tối (dòng trắng lớn + dòng vàng nhỏ), bong bóng thoại, thẻ tên.
- **Ảnh tư liệu thật** lồng vào cảnh như tranh, ảnh, tài liệu trong tay nhân vật — vẫn theo đúng quy tắc dùng ảnh ở trên.
- Giữ nguyên: Shorts dọc 9:16, **giọng chủ kênh tự thu**, phụ đề tiếng Việt, hiệu ứng tiếng (không nhạc nền), đối chiếu sự kiện trước khi thu, không hiện tên kênh/logo trong video.
- Ảnh đại diện và ảnh bìa kênh: `brand/avatar_*.png`, `brand/banner_*.png`.

## Cập nhật: hoạt hình thuần (chủ kênh chốt 17/11/2026, từ Onoda v2)

Mốc phong cách cho các tập sau là **Onoda v2** (`onoda/src/scenes.py`, `onoda/src/toon2.py`):

- **Hoạt hình thuần, không dùng ảnh thật** → không vướng quyền sử dụng ảnh. Ảnh chủ kênh gửi dùng để **tham khảo** (trang phục, bối cảnh, sự kiện) khi vẽ, không đưa trực tiếp vào video. Nhân vật người thật vẽ đơn giản, không mô phỏng khuôn mặt.
- **Nhân vật cử động**: đi, nói (nhép miệng), chớp mắt, thở, nhiều tư thế; nhân vật già đi theo thời gian khi câu chuyện kéo dài nhiều năm.
- **Cắt nhanh ~3–4 s/cảnh**, chuyển chương bằng lia máy có nhoè; đoạn nặng dùng mờ dần.
- **Kể bằng hình ảnh** thay vì minh họa chữ: ẩn dụ thị giác (nến thay số người chết, đồng hồ năm, màn hình chia đôi, ngày–đêm luân phiên), chữ lớn bật từng ký tự.
- Linh vật xuất hiện ở đoạn nhẹ; vắng mặt ở đoạn có người chết.
- Giữ: Shorts 9:16, giọng chủ kênh, phụ đề, hiệu ứng tiếng (không nhạc), đối chiếu sự kiện trước khi thu.
