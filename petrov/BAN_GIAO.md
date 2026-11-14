# Petrov v1 — ghi chú bàn giao

**Tập:** Năm 1983, vì sao một sĩ quan Liên Xô không báo động khi máy tính báo Mỹ phóng tên lửa?
**Phiên bản:** v1 · Shorts 1080 × 1920, 30 fps · dài 1:44,1 (theo MP3) · phong cách Midway v2, **có hiệu ứng tiếng**

## Bộ file

| File | Nội dung |
|---|---|
| `build/Petrov_v1.mp4` | Bản đầy đủ: H.264 CRF 19, AAC 192 kbps, phụ đề in cứng, giọng + 149 hiệu ứng; −14,1 LUFS, đỉnh −1,3 dBTP |
| `build/Petrov_v1.srt` | Phụ đề riêng |
| `build/sfx_stem.wav` | Riêng lớp hiệu ứng |
| `build/contact_sheet.png` | Dải khung hình |
| `assets/screenshots/` | 29 ảnh chụp màn hình gốc |
| `assets/photos/` | Ảnh đã cắt, chỉ gồm ảnh dùng được |

Xuất lại: `python3 src/align.py && python3 src/render.py full && mv build/Petrov_v1.mp4 build/Petrov_v1_nosfx.mp4 && python3 src/sfx_events.py`

## Việc cần chủ kênh xem

1. **Không có ảnh Petrov năm 1983 dùng được.** Ảnh thời trẻ trong quân phục và các ảnh Petrov ở nhà đều là ảnh Alamy có dấu nước (bản quyền), ảnh mặc quân phục ở brightstarsound.com ghi "© Juliet Butler / Alamy". Video dùng ảnh Commons những năm cuối đời, chú thích rõ. Nếu chủ kênh có ảnh thời trẻ với quyền sử dụng rõ, Claude thay vào.
2. **Phòng chỉ huy Serpukhov-15:** không có ảnh xác minh (ảnh phòng điều khiển trên vitalcapacities.com không rõ nguồn), nên màn hình báo động là đồ họa có nhãn DIỄN Ý / MINH HỌA.
3. **Mốc giây là ước lượng.** **Hiệu ứng tiếng:** Claude không nghe được; còi báo động ~10 dB dưới giọng, cú nhấn ~8 dB, tự hạ ~7 dB khi có lời.

## Bảng xác minh ảnh

| Ảnh chụp màn hình | Nội dung | Căn cứ | Dùng |
|---|---|---|---|
| 1000043835 | Petrov những năm cuối đời (áo sọc, lịch tháng 6) | Wikimedia (tên file "Stanislaw-jewgr…") | ✓ 9,9–14 s; 88,6–94 s |
| 1000043833 | Petrov được vinh danh trên sân khấu, màn hình ghi Semperoper Dresden | Trang Commons "Petrow semperoper1.JPG" | ✓ 81,6–85,1 s (không ghi năm) |
| 1000043832 | Đá tưởng niệm "Stanisławowi Jefgrafowiczowi Pietrowowi (1939–2017)" | Wikimedia; đọc được chữ khắc | ✓ 100,8–104,1 s |
| 1000043831 / 34 | Tướng Yury Votintsev | Wikipedia tiếng Nga (hộp thông tin) | ✓ 77,9–81,6 s |
| 1000043820 | Bản đồ đường bay KAL 007 | Trang Commons "KAL007.svg" | ✓ 26,9–32,6 s |
| 1000043822 | Tên lửa Minuteman III đang phóng | Tên file "Minuteman_III_l…" | ✓ 4,2–5,6 s — chú thích "ảnh minh họa, một lần phóng thử" |
| 1000043824 / 25 | Radar Daryal ở Pechora | Tên file "Pechora_radar…"; danh mục "Daryal radar" | ✓ 46,3–50,8 s — "radar mặt đất của Liên Xô, chụp sau này" |
| 1000043814 | Ảnh vệ tinh, toạ độ 55,068°B 37,041°Đ | Toạ độ trùng Serpukhov-15 | ✓ 14–16,5 s — "chụp sau này" |
| 1000043829 | Sơ đồ vệt quỹ đạo kiểu Molniya | Trang Commons "Molniya.jpg" | ✓ 16,5–22,6 s — "loại quỹ đạo vệ tinh Oko dùng" |
| 1000043838 | Fryazino | Trang Commons "Fryazino 2010-05-19.jpg" | ✓ 85,1–88,6 s |
| 1000043811, 12, 15, 16 | Petrov mặc quân phục (People 1999), các ảnh khác trên brightstarsound.com | Chú thích ghi © Juliet Butler / Alamy, Association of World Citizens | **Không dùng — bản quyền** |
| 1000043813, 36, 37 | Petrov thời trẻ; Petrov ở nhà | Ảnh Alamy có dấu nước | **Không dùng — bản quyền** |
| 1000043817 | Trung tâm điều khiển vệ tinh (TWZ) | Báo TWZ, không rõ quyền | Không dùng |
| 1000043818 | Phòng điều khiển (vitalcapacities.com) | Không rõ nguồn, không chắc là Serpukhov-15 | Không dùng |
| 1000043819 | Boeing 747 Korean Air | Tên file "747-2B5" — KAL 007 là 747-230B (HL7442), không phải chiếc này | Không dùng |
| 1000043828 | Vệ tinh Molniya-1 trong bảo tàng | Vệ tinh thông tin, không phải Oko | Không dùng |
| 1000043823, 26, 27, 30 | Sơ đồ Minuteman; Minuteman trong hầm 1989; bản đồ radar Daryal; bản đồ địa cầu | Không cần cho nội dung | Không dùng |
| 1000043839 | Bài cáo phó trên The Guardian | Ảnh báo, bản quyền | Không dùng (dùng để đối chiếu) |
| — | Karl Schumacher, Dmitry | Không có ảnh xác minh | Thẻ tên chữ |

## Bảng dựng theo mốc giây

| Mốc | Lời | Hình | Hiệu ứng |
|---|---|---|---|
| 0–5,6 | "Hơn nửa đêm 26/9/1983… Mỹ vừa phóng tên lửa" | Màn hình 00:15 (minh họa); ảnh Minuteman phóng | Ù máy, tiếng nổ trầm |
| 5,6–9,9 | "báo lên cấp trên hay không" | Điện thoại quay số, "CÓ / KHÔNG" | — |
| 9,9–14 | "trung tá Stanislav Petrov…" | Chân dung + thẻ tên | Giấy |
| 14–22,6 | "Serpukhov-15… vệ tinh cảnh báo sớm… căn cứ Mỹ" | Ảnh vệ tinh khu boong-ke; sơ đồ quỹ đạo, hai vệ tinh, sóng trên nước Mỹ | Bíp |
| 22,6–26,9 | "không phải bấm nút đánh trả… báo lên trên" | Hai thẻ, dấu "KHÔNG PHẢI" / "NHIỆM VỤ" | Dấu |
| 26,9–32,6 | "rất căng… máy bay Hàn Quốc" | Bản đồ KAL 007, chip 1.9.1983 | Nổ xa |
| 32,6–40,6 | "còi… СТАРТ… năm tên lửa… cao nhất" | Màn hình đỏ nhấp nháy "СТАРТ", 1 → 5 tên lửa, "ĐỘ TIN CẬY: CAO NHẤT" (diễn ý) | Còi báo động, bíp, cú nhấn |
| 40,6–46,3 | "không tin… không chỉ năm quả" | So sánh: đánh thật (hàng chục tên lửa) / báo động (5) | Tim đập |
| 46,3–50,8 | "radar mặt đất… chưa thể xác nhận" | Ảnh radar Daryal | — |
| 50,8–53 | "lỗi hệ thống" | Màn hình gõ "LỖI HỆ THỐNG" | Máy chữ |
| 53–60,9 | "ông chờ… 23 phút… ông đã đúng" | Đồng hồ đếm 0 → 23 phút, dấu "ÔNG ĐÃ ĐÚNG" | Tích tắc, tim đập, dấu |
| 60,9–67,5 | "ánh nắng phản chiếu trên mây cao" | Đồ họa Mặt Trời → mây → vệ tinh (minh họa) | Ngân |
| 67,5–74 | "không được khen thưởng… khiển trách… rời quân đội" | Sổ trực, dấu "KHIỂN TRÁCH", chip 1984 | Dấu |
| 74–81,6 | "giữ kín 15 năm… tướng Votintsev… hồi ký 1998" | 1983 → 1998; chân dung Votintsev | Tích tắc |
| 81,6–85,1 | "người đã cứu thế giới" | Ảnh Petrov ở Semperoper Dresden | Ngân |
| 85,1–88,6 | "Fryazino" | Ảnh Fryazino 2010 | — |
| 88,6–94 | "19/5/2017… gần bốn tháng" | Chân dung, chip ngày | — |
| 94–100,8 | "7/9… Karl Schumacher… Dmitry" | Điện thoại rung chuông, nhấc máy | Chuông điện thoại |
| 100,8–104,1 | "đã mất từ tháng 5" | Đá tưởng niệm, tối dần | — |

## Phiên bản đã chốt

**Chủ kênh chốt v1 (14/11/2026)**, giữ ảnh Petrov những năm cuối đời ở đoạn giới thiệu.
