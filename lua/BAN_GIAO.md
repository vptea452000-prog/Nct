# Tập 1: Lửa — ghi chú bàn giao

**Chuỗi:** fact nguyên thủy · **định dạng:** phim hoạt hình hài không lời (bóng thoại truyện tranh, giọng ú ớ tổng hợp)
**Phiên bản:** v1 · Shorts 1080 × 1920, 30 fps · dài 1:32,1 · kịch bản do AI khác viết, Claude dựng theo các đề xuất đã duyệt

| File | Nội dung |
|---|---|
| `build/Lua_v1.mp4` | Bản đầy đủ: hình + giọng ú ớ + hiệu ứng tiếng; −14,2 LUFS, đỉnh −1,3 dBTP |
| `build/sfx_stem.wav` | Lớp âm thanh riêng (giọng ú ớ + hiệu ứng) |
| `build/contact_sheet.png` | Dải khung hình |
| `src/beats.py` | **Nhịp phim**: 40 nhịp, mỗi nhịp có thời lượng, người nói, loại bóng thoại, chữ, cảm xúc giọng — sửa ở đây là đổi được thoại/nhịp |
| `src/scenes.py` | Từng cảnh; `src/sfx_events.py` giọng ú ớ (formant) + hiệu ứng |

Xuất lại: `python3 src/render.py full && python3 src/sfx_events.py`

## Đã áp dụng theo đề xuất được duyệt

1. **Thẻ fact cuối phim**: "Con người đã dùng lửa từ khoảng 1 triệu năm trước. Nấu chín giúp thức ăn mềm và dễ tiêu hóa hơn." + "Tập sau: cây giáo". Không khẳng định cách xoay que tạo lửa (chưa có bằng chứng khảo cổ trực tiếp).
2. **Bóng thoại dài được tách ngắn** (ví dụ câu của Bộp ở cảnh 1 tách thành 3 bóng).
3. **Nhân vật**: Bộp — người hiện đại thời tiền sử, mảnh, hiền; Gầm — người Neanderthal vạm vỡ, râu rậm, cầm **gậy gỗ thẳng** (không phải dùi cui u bướu).
4. **Giọng ú ớ**: Bộp cao, nhanh, nhẹ; Gầm trầm, chậm, to, khàn. Cảm xúc theo câu: hét (lên giọng, to), thì thầm (chỉ hơi), run lạnh (giọng rung), xấu hổ (nhỏ, chậm), hoảng (cao, nhanh). "Đồ vô dụng!" cuối phim được làm như vọng ra từ trong hang.

## Bóng thoại & tượng thanh

- Bóng **tròn** (nói thường), **răng cưa nền vàng chữ đỏ** (hét), **đám mây** (nghĩ), **viền đứt** (thì thầm).
- Chữ tượng thanh: VÈO VÈO, PHÙ…, BÙNG!, BỤP!, TÁCH TÁCH, BÌNH! BỊCH!, KHỤ KHỤ!, CẬP CẬP, KHỊT KHỊT, ỌC ỌC ỌC, GRỪ…, PHỪNG!, ẲNG ẲNG!, HỪM!

## Cần chủ kênh xem

- Claude **không nghe được âm thanh**: giọng ú ớ và hiệu ứng chỉ đo bằng số. Nghe xem giọng Bộp/Gầm đã đủ vui chưa (cao/thấp, nhanh/chậm), góp ý theo nhịp hoặc mốc giây.
- Độ dài 1:32 (Shorts cho phép tới 3 phút). Muốn gọn hơn có thể bớt vài nhịp ở cảnh 1 và 3 trong `src/beats.py`.

## Sửa (17/11/2026) — bỏ tiếng lách cách khi nhân vật nói

Chủ kênh phản ánh: khi nhân vật nói có nhiều tiếng lách cách, khó chịu. Nguyên nhân và cách sửa:
- **Trong giọng ú ớ**: mỗi âm tiết có chèn tiếng phụ âm (tiếng xì ngắn) và bật/tắt âm tiết gắt → chuỗi lách cách. Giọng mới: nguồn hài âm sạch, cao độ trượt mượt, nguyên âm chuyển dần, âm tiết vào–ra mềm, **không còn tiếng phụ âm**. Đo lại: 0 đột biến cao tần trong giọng (trước đây mỗi âm tiết một đột biến).
- **Tiếng lửa nền**: trước nhiều tiếng tí tách → nay chủ yếu tiếng ù ấm, tí tách rất thưa và nhẹ.
- **Bỏ** tiếng ma sát dạng gõ khi xoay que (thay bằng tiếng cọ êm), tiếng răng va lập cập, các tiếng tích tắc lẻ.
- Áp dụng cho các tập sau: không dùng chuỗi tiếng gõ/tích tắc dưới lời thoại.
