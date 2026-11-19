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
- Ảnh đại diện mới (18/11/2026, chủ kênh duyệt): chỉ Bộp, cận mặt, chống cằm suy nghĩ — `brand/avatar_bop_{cam,xanh,dem}.png` (tạo bằng `brand/make_avatar_bopgam.py solo`).

## Cập nhật: hoạt hình thuần (chủ kênh chốt 17/11/2026, từ Onoda v2)

Mốc phong cách cho các tập sau là **Onoda v2** (`onoda/src/scenes.py`, `onoda/src/toon2.py`):

- **Hoạt hình thuần, không dùng ảnh thật** → không vướng quyền sử dụng ảnh. Ảnh chủ kênh gửi dùng để **tham khảo** (trang phục, bối cảnh, sự kiện) khi vẽ, không đưa trực tiếp vào video. Nhân vật người thật vẽ đơn giản, không mô phỏng khuôn mặt.
- **Nhân vật cử động**: đi, nói (nhép miệng), chớp mắt, thở, nhiều tư thế; nhân vật già đi theo thời gian khi câu chuyện kéo dài nhiều năm.
- **Cắt nhanh ~3–4 s/cảnh**, chuyển chương bằng lia máy có nhoè; đoạn nặng dùng mờ dần.
- **Kể bằng hình ảnh** thay vì minh họa chữ: ẩn dụ thị giác (nến thay số người chết, đồng hồ năm, màn hình chia đôi, ngày–đêm luân phiên), chữ lớn bật từng ký tự.
- Linh vật xuất hiện ở đoạn nhẹ; vắng mặt ở đoạn có người chết.
- Giữ: Shorts 9:16, giọng chủ kênh, phụ đề, hiệu ứng tiếng (không nhạc), đối chiếu sự kiện trước khi thu.

## Quy trình rút gọn (chủ kênh chốt 17/11/2026)

Chủ kênh gửi **kịch bản + file MP3 giọng đọc**. Claude làm tất cả phần còn lại: đối chiếu sự kiện, căn mốc, phụ đề, thiết kế cảnh hoạt hình, hiệu ứng tiếng, xuất video và bàn giao. Không cần gửi ảnh.

- Nếu chỉ gửi MP3 mà không kèm kịch bản: Claude dùng kịch bản đã đối chiếu trước đó cho tập ấy; Claude chưa nghe được nội dung MP3 nên **cần bản chữ của lời đọc** để làm phụ đề và căn mốc.
- Chỗ sai sự kiện phát hiện khi đối chiếu: Claude vẫn dựng, chữ trên hình viết trung tính, và báo câu + mốc giây cần thu lại.

## Chuỗi "fact nguyên thủy" (chủ kênh chốt 17/11/2026)

- Video Shorts riêng lẻ, mỗi video một fact về thời tiền sử; chủ kênh viết kịch bản, gửi MP3 + bản chữ.
- Phong cách hoạt hình thuần như Onoda v2; **linh vật kênh vẫn là người dẫn chuyện**.
- Đối chiếu: tách rõ điều đã chắc (có bằng chứng, có niên đại) với giả thuyết; đề xuất cách nói "các nhà khoa học cho rằng…" khi cần. Niên đại ghi đúng đơn vị (năm trước Công nguyên / cách đây … năm).
- Hình vẽ tránh khuôn mẫu sai: người tiền sử cầm gậy gầm gừ, sống cùng khủng long, mặc da thú kiểu hoạt hình cũ khi không có căn cứ.

## Định dạng mới: phim hoạt hình hài không lời (chủ kênh chốt 17/11/2026)

Áp dụng cho chuỗi fact nguyên thủy:
- **Không còn giọng đọc của chủ kênh, không linh vật.** Nhân vật nói ú ớ (giọng tự tổng hợp, mỗi nhân vật một cao độ/nhịp riêng); người xem hiểu qua **bóng thoại truyện tranh** (thường / hét / nghĩ / thì thầm) và chữ tượng thanh.
- Hài, diễn xuất phóng đại; mỗi phim xoay quanh **một fact có thật**, kết bằng **thẻ fact** 1–2 câu.
- Kịch bản do một AI khác viết theo `MAU_KICH_BAN_HAI.md`; chủ kênh gửi kịch bản → Claude đối chiếu fact, dựng hình, tổng hợp giọng ú ớ, hiệu ứng tiếng, xuất video.
- Shorts 9:16, 30–60 giây; không phụ đề lời đọc (chỉ bóng thoại).

### Ghi chú sau Tập 1: Lửa (17/11/2026)
Chủ kênh: "khá hay, khá vui" → định dạng phim hài không lời được giữ. Yêu cầu **tập sau vui hơn nữa**. Phía Claude sẽ tăng: biểu cảm phóng đại (mắt lồi, nhảy dựng, khói bốc đầu), hài hình thể (ngã, va đầu, cháy mông), nhịp cắt nhanh hơn, cận mặt khi phản ứng, rung khung ở cú đánh hài, tiếng hiệu ứng kiểu hoạt hình (boing, trượt, té). Gợi ý cho người viết kịch bản: phần "Để phim vui hơn" trong `MAU_KICH_BAN_HAI.md`.
- **Âm thanh phim hài không lời (sửa sau Tập 1):** giọng ú ớ phải liền mạch, không chèn tiếng phụ âm/tiếng gõ; không đặt chuỗi tiếng lách cách, tích tắc, tí tách dày dưới lời thoại.
- **Giọng ú ớ đã chốt (17/11/2026):** dùng đúng giọng của Tập 1 bản sửa, lưu trong `tools/babble.py` (Bộp cao–nhanh–nhẹ, Gầm trầm–chậm–khàn; cảm xúc theo câu). Nhân vật mới thêm vào bảng `VOICE` cùng kiểu.
- **Bộ khung nhân vật v2 (18/11/2026, chủ kênh khen "linh hoạt vui nhộn hơn", cải thiện dần):** `tools/rig.py` (tỉ lệ chibi, tay chân IK, lấy đà–co giãn–nảy, thở/chớp mắt/đung đưa, nét mặt phong phú, lợn rừng sống động) + `tools/lipsync.py` (nhép miệng theo âm lượng giọng ú ớ, cùng seed/mốc với sfx_events). Mẫu dùng: `giao/demo/demo.py`. Áp dụng từ Tập 3 trở đi (Tập 2 giữ bản v1).

## Định dạng kể chuyện 16:9 (từ 19/11/2026)
- Video ngang 16:9, kể ở ngôi "bạn" (ví dụ: "Nếu bạn là người lính Nhật trong Thế Chiến II"). Claude viết kịch bản, chủ kênh thu giọng đọc, Claude dựng video.
- Viết như **kể chuyện** có nhân vật và cảm xúc, không viết kiểu bài lịch sử nhiều mốc và con số.
- File kịch bản (`KICH_BAN.md`) chỉ có **một bài đọc liền mạch**: không chia phần, không tiêu đề phụ, không ghi chú ngắt nghỉ. Khung hình và đối chiếu dữ kiện để riêng ở `GHI_CHU.md`.
- **Không dùng tên/nhân vật chuỗi nguyên thủy (Bộp, Gầm)**; nhân vật đặt tên hợp bối cảnh (lính Nhật: Kenji…), vẽ **người que** (`tools/stick2.py`) — chủ kênh chốt 19/11/2026 thay cho chibi.
- Nhân vật diễn câm theo lời dẫn, có hiệu ứng tiếng; chuyển động tự nhiên, hoạt bát.
- **Nhịp máy quay (chủ kênh duyệt 19/11/2026):** máy luôn có chuyển động nhưng **vừa phải** — cảnh dài, cẩu/lia/đẩy chậm và êm, không rung tay; **chỉ nhanh ở khoảnh khắc cao trào** (zoom giật, nghiêng khung, chớp sáng, đồ vật đập vào khung). Mẫu: `linh_nhat/src/test_open2.py` (bản v3).
