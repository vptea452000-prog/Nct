# Onoda v1 — ghi chú bàn giao

**Tập:** Vì sao một người lính Nhật vẫn chiến đấu 29 năm sau khi chiến tranh kết thúc?
**Phiên bản:** v1 · Shorts 1080 × 1920, 30 fps · dài 2:00,8 (theo MP3) · **phong cách hoạt hình 2D mới, có linh vật**, có hiệu ứng tiếng

## Bộ file

| File | Nội dung |
|---|---|
| `build/Onoda_v1.mp4` | Bản đầy đủ: H.264 CRF 19, AAC 192 kbps, phụ đề in cứng, giọng + 176 hiệu ứng; −14,2 LUFS, đỉnh −1,2 dBTP |
| `build/Onoda_v1.srt` | Phụ đề riêng |
| `build/sfx_stem.wav` | Riêng lớp hiệu ứng |
| `build/contact_sheet.png` | Dải khung hình |
| `src/` | `scenes.py` (bảng dựng), `toon.py` (nhân vật hoạt hình), `sets.py` (bối cảnh), `sfx_events.py`, `subs.py`, `align.py`, `render.py` |

Xuất lại: `python3 src/align.py && python3 src/render.py full && mv build/Onoda_v1.mp4 build/Onoda_v1_nosfx.mp4 && python3 src/sfx_events.py`

## Việc cần chủ kênh xem trước khi đăng

1. **Quyền sử dụng hai ảnh** (đã xác minh đúng người, đúng sự kiện, nhưng quyền chưa rõ):
   - `suzuki_onoda_1974.jpg` (81,7–83,3 s) — ảnh trong hộp thông tin Wikipedia tiếng Anh về Norio Suzuki; trang Wikipedia có thể dùng theo "sử dụng hợp lý", không phải ảnh tự do.
   - `onoda_walkout_1974.jpg` (104,1–107,3 s) — ảnh Onoda rời rừng năm 1974 (historicalphotos.com, blogspot), không ghi tác giả.
2. **Ảnh không dùng vì bản quyền rõ:** Onoda trao kiếm cho Marcos (ghi JIJI PRESS/AFP/Getty Images), ảnh Onoda chào (Getty Images), ảnh trên historyhit.com (Alamy/Granger). Cảnh trao kiếm được vẽ hoạt hình, có nhãn "HOẠT HÌNH MINH HỌA".
3. **Mốc giây là ước lượng.** **Hiệu ứng tiếng:** Claude không nghe được; dấu/cú nhấn ~8 dB dưới giọng, tự hạ ~7 dB khi có lời.

## Bảng xác minh ảnh

| Ảnh chụp màn hình | Nội dung | Căn cứ | Dùng |
|---|---|---|---|
| 1000043865 | Hiroo Onoda thời trẻ | Trang Commons "Hiroo Onoda young.jpg" | ✓ 13,6–15,8 s; 69,2–73,3 s |
| 1000043866 | Hiroo và Shigeo Onoda, 1944 | Trang Commons cùng tên | Dự phòng (chưa dùng) |
| 1000043867 | Quần đảo Lubang nhìn từ trên cao | Tên file "Lubang_Group…" | ✓ 18,9–21,4 s — "chụp sau này" |
| 1000043868 | Bãi biển Lubang | Tên file "Lubang_…" | Dự phòng |
| 1000043871 | Kinshichi Kozuka | Trang Commons "Kozuka kinshichi.jpg" | ✓ 54,5–60,8 s |
| 1000043873 | Suzuki (trái) và Onoda, 2/1974, Lubang | Chú thích hộp thông tin Wikipedia | ✓ 81,7–83,3 s — **quyền chưa rõ** |
| 1000043874 (và 72) | Onoda rời rừng năm 1974 | Tiêu đề trang "Hiroo Onoda… 1974" | ✓ 104,1–107,3 s — **quyền chưa rõ** |
| 1000043869 | Onoda trao kiếm cho Marcos, 11/3/1974 | JIJI PRESS/AFP/Getty Images | **Không dùng — bản quyền** |
| 1000043870 | Onoda khi đầu hàng 1974 | Alamy/Granger | **Không dùng — bản quyền** |
| 1000043875 | Onoda chào | Getty Images | **Không dùng — bản quyền** |

Nhân vật hoạt hình (lính, Suzuki, Taniguchi, Tổng thống Marcos) đều vẽ đơn giản, không mô phỏng khuôn mặt người thật.

## Bảng dựng theo mốc giây

| Mốc | Lời | Hình | Hiệu ứng |
|---|---|---|---|
| 0–8,7 | "Năm 1974… Thế chiến chưa kết thúc" | Rừng lúc hoàng hôn, tiêu đề "1974 / PHILIPPINES", linh vật cầm ống nhòm; lính bước ra; cận mặt chào, bong bóng "THẾ CHIẾN CHƯA KẾT THÚC!" | Tiếng rừng, lá xào xạc |
| 8,7–13,6 | "chỉ huy cũ… bán sách… bay sang" | Hiệu sách, ông chỉ huy cũ, linh vật ngó; máy bay qua biển | Máy bay |
| 13,6–15,8 | "thiếu úy Hiroo Onoda" | Ảnh thật Onoda thời trẻ, thẻ tên | Dấu |
| 15,8–24,5 | "Lubang… không được đầu hàng… rút vào núi" | Bản đồ Manila – Lubang; ảnh đảo; dấu "KHÔNG ĐẦU HÀNG"; 4 người lính đi vào rừng | Bước chân |
| 24,5–38,6 | "Nhật đầu hàng… truyền đơn… đồ giả… loa, thư" | Tiêu đề "8 · 1945"; máy bay rải truyền đơn; dấu "ĐỒ GIẢ!"; loa và thư bật ngược ra | Máy bay, giấy, dấu, vô tuyến |
| 38,6–47,4 | "du kích… đốt lúa… ba mươi người" | Đêm, ruộng lúa cháy, chớp súng; màn tối "khoảng 30 người chết" (không đùa) | Lửa, súng |
| 47,4–62,6 | "từng người rời đi… Kozuka… một mình" | Bốn người lính, một người bỏ đi, một người mờ đi; ảnh Kozuka; Onoda nhỏ giữa rừng "MỘT MÌNH" | Bước chân, súng |
| 62,6–73,3 | "Nhật Bản sững sờ… 1959… còn sống?" | Báo (minh họa), linh vật hoảng; văn bản 1959 dấu "ĐÃ CHẾT"; ảnh Onoda dấu "CÒN SỐNG?" | Giấy, dấu |
| 73,3–87,7 | "Suzuki… bốn ngày… chụp ảnh chung… lệnh cấp trên" | Chàng trai đeo ba lô; đếm ngày; gặp nhau; ảnh thật Suzuki – Onoda kèm chớp đèn; bong bóng "CHỈ ĐI KHI CÓ LỆNH CẤP TRÊN" | Bước chân, màn trập |
| 87,7–104,1 | "mang ảnh về… Taniguchi… 9/3/1974… đọc lệnh" | Máy bay; hiệu sách, thẻ tên Taniguchi; hai người vào rừng; Onoda chào; bong bóng "MIỄN TOÀN BỘ NHIỆM VỤ CHIẾN ĐẤU" | Bước chân, giấy |
| 104,1–120,8 | "trình diện… súng, 500 viên đạn… trao kiếm… ân xá" | Ảnh Onoda rời rừng; súng, bộ đếm 500, lựu đạn; trao kiếm (hoạt hình); dấu "ÂN XÁ", tối dần | Kim loại, dấu |
