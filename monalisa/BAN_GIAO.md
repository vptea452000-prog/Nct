# Mona Lisa v1 — ghi chú bàn giao

**Tập:** Vì sao Mona Lisa biến mất hơn một ngày mới có người nhận ra?
**Phiên bản:** v1 · Shorts 1080 × 1920, 30 fps · dài 1:51,3 (theo MP3) · phong cách Midway v2, **có hiệu ứng tiếng**

## Bộ file

| File | Nội dung |
|---|---|
| `build/MonaLisa_v1.mp4` | Bản đầy đủ: H.264 CRF 19, AAC 192 kbps, phụ đề in cứng, giọng + 130 hiệu ứng; −14,1 LUFS, đỉnh −1,0 dBTP |
| `build/MonaLisa_v1.srt` | Phụ đề riêng |
| `build/sfx_stem.wav` | Riêng lớp hiệu ứng |
| `build/contact_sheet.png` | Dải khung hình |
| `assets/screenshots/` | 21 ảnh chụp màn hình gốc (để truy nguồn) |
| `assets/photos/` | Ảnh đã cắt, chỉ gồm ảnh đã xác minh |

Xuất lại: `python3 src/align.py && python3 src/render.py full && mv build/MonaLisa_v1.mp4 build/MonaLisa_v1_nosfx.mp4 && python3 src/sfx_events.py`

## Việc cần chủ kênh xem

1. **Ảnh bức Mona Lisa** chỉ có bản thu nhỏ ~240 px (từ trang danh mục Commons) nên chỉ dùng cỡ nhỏ (thước 77 cm, rương đáy giả). Nếu gửi thêm ảnh chụp màn hình bản lớn (ví dụ trang Commons "Mona Lisa, by Leonardo da Vinci, from C2RMF retouched.jpg"), Claude sẽ thay vào.
2. **Mốc giây là ước lượng**; ranh giới câu khớp khoảng lặng rất tốt.
3. **Hiệu ứng tiếng:** Claude không nghe được; dấu/búa tòa ~8 dB dưới giọng, tự hạ ~7 dB khi có lời.

## Bảng xác minh ảnh

| Ảnh chụp màn hình | Nội dung | Căn cứ | Dùng |
|---|---|---|---|
| 1000043767 | Chỗ treo Mona Lisa trống, bốn móc sắt | Trang Commons "Mona Lisa stolen-1911.jpg" | ✓ 14,3–16,3 s; 68,5–71,3 s |
| 1000043770 / 71 | Tranh "Mona Lisa au Louvre" của Louis Béroud, 1911 | Trang Commons "Louis Beroud - Mona Lisa au Louvre 1911.jpg" | ✓ 0–6,8 s; 10,1–14,3 s |
| 1000043776 | Thẻ hồ sơ cảnh sát (Bertillon) của Peruggia, ảnh hai góc + vân tay tay phải, ghi "Peruggia 25.1.09" | Trang Commons "Vincenzo Perugia.jpg" | ✓ 25,2–31,8 s (cắt mặt); 44,6–47,9 s (cả thẻ) |
| 1000043775 | Tranh minh họa báo chí tái hiện vụ trộm, có chân dung Peruggia | Trang Commons "Vincenzio Peruggia stealing Mona Lisa.jpg" | ✓ 31,8–39,3 s (lướt từng khung); 95,7–104,7 s (chân dung) — chú thích "tranh minh họa, không phải ảnh chụp" |
| 1000043777 | Guillaume Apollinaire, tháng 9/1911 | Trang Commons "Guillaume Apollinaire - Septembre 1911.jpg" | ✓ 51,5–54,4 s |
| 1000043778 | Pablo Picasso trong xưởng vẽ ở Montmartre, 1908 | Trang Commons cùng tên | ✓ 54,4–57,1 s |
| 1000043783 (và 81) | Mona Lisa ở Uffizi, Florence, 1913 | Trang Commons "Monalisa uffizi 1913.jpg"; chú thích trên Modern Met | ✓ 91,1–93,8 s — không gắn tên những người trong ảnh |
| 1000043784 / 85 | Le Petit Parisien số 13559, 13/12/1913, "La Joconde est retrouvée" | Trang Commons cùng tên | ✓ 93,8–95,7 s |
| 1000043786 | Mona Lisa trở về Louvre, 1914 | Trang Commons "After photo for the return of Gioconda at the Louvre Museum 1914.jpg" | ✓ 104,7–111,3 s |
| 1000043768 | Ảnh Mona Lisa (bản thu nhỏ trong danh mục Commons) | Danh mục "Mona Lisa in the Louvre" | ✓ chỉ cỡ nhỏ |
| 1000043787 | Hàng người xếp hàng biển "MONA LISA", thùng khiêng lên bậc thềm | Không có chú thích; rào "Police Line", xe hơi hiện đại — nhiều khả năng chuyến triển lãm ở Mỹ năm 1963 | **Không dùng** (không phải năm 1911) |
| 1000043782 | Kết quả tìm ảnh (trở về Louvre, ảnh nhóm với tranh) | Không có chú thích | Không dùng (đã có bản có trang Commons) |
| 1000043779 | Apollinaire băng đầu | Ảnh thời Thế chiến I, khác giai đoạn | Không dùng |
| 1000043780 | Picasso 500px | Đã có ảnh có trang Commons | Không dùng |
| 1000043772, 73 | Tranh nhà hát Opéra và Hội chợ Thế giới của Béroud | Không liên quan nội dung | Không dùng |
| 1000043769 | Danh mục Commons (ảnh nhỏ) | — | Không dùng |
| — | Alfredo Geri, Giovanni Poggi, Louis Béroud (chân dung) | Không có ảnh xác minh | Thẻ tên chữ, không mượn ảnh người khác |

Đồ họa minh họa có nhãn MINH HỌA / DIỄN Ý: tít báo năm 1911 (tiếng Việt), lá thư "Leonardo", mặt sau tranh có dấu Louvre.

## Bảng dựng theo mốc giây

| Mốc | Lời | Hình | Hiệu ứng |
|---|---|---|---|
| 0–6,8 | "Thứ Hai 21/8/1911… Louvre ở Paris" | Tranh của Béroud vẽ Mona Lisa trên tường Louvre, khung vàng quanh Mona Lisa | Bật, bút dạ |
| 6,8–10,1 | "hơn một ngày sau…" | Đồng hồ quay từ sáng thứ Hai sang sáng thứ Ba | Tích tắc |
| 10,1–16,3 | "Louis Béroud… bốn cái móc sắt" | Tranh của Béroud + thẻ tên; ảnh bức tường trống, khoanh 4 móc | Gõ nhẹ |
| 16,3–25,2 | "lính gác… chụp ảnh… giục mấy lần… không hề giữ" | Lính gác, Béroud, thẻ "BÊN CHỤP ẢNH", ba dấu "!", dấu "KHÔNG GIỮ" | Màn trập, dấu |
| 25,2–31,8 | "Vincenzo Peruggia… đóng cửa" | Ảnh mặt từ thẻ hồ sơ, dấu "ĐÓNG CỬA" | Dấu |
| 31,8–41,4 | "áo khoác trắng… gỡ… cầu thang… tháo khung… giấu… 80 phân" | Lướt từng khung tranh minh họa báo chí; thước 77 cm cạnh Mona Lisa | Bước chân, kẽo kẹt |
| 41,4–51,5 | "khung tranh, vân tay… hồ sơ… sắp theo cách khác" | Khung + kính có vân tay; thẻ hồ sơ (khoanh vân tay); tủ hồ sơ xếp theo số đo | Ngăn kéo |
| 51,5–59,1 | "Apollinaire… Picasso… không liên quan" | Hai chân dung, dấu "KHÔNG LIÊN QUAN" | Dấu |
| 59,1–66,6 | "phòng trọ… đáy giả" | Cảnh sát hỏi chuyện; rương cắt ngang thấy tranh dưới đáy giả | Kẽo kẹt |
| 66,6–71,3 | "báo chí… xếp hàng nhìn tường trống" | Tít báo (minh họa); ảnh bức tường trống | Giấy, xì xào |
| 71,3–81,1 | "hai năm… Florence… thư ký tên Leonardo" | 1911 → 1913; bản đồ Paris – Florence; lá thư (diễn ý) | Tích tắc, bút |
| 81,1–91,1 | "Geri… Poggi… khách sạn… đáy giả… dấu Louvre" | Thẻ tên; rương mở, đáy giả nhấc lên, tranh lộ ra; mặt sau tranh có dấu (minh họa) | Kẽo kẹt, dấu |
| 91,1–95,7 | "giữ tranh kiểm tra… bị bắt tại khách sạn" | Ảnh Mona Lisa ở Uffizi 1913; Le Petit Parisien 13/12/1913 | Giấy |
| 95,7–104,7 | "ra tòa… quê hương Leonardo… 7 tháng" | Chân dung Peruggia (tranh minh họa); "hơn 1 năm tù" gạch → "còn 7 tháng" | Búa tòa |
| 104,7–111,3 | "4/1/1914… 28 tháng" | Ảnh tranh trở về Louvre 1914, tối dần | Xì xào, chuông |
