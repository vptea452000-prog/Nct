# Mincemeat v1 — ghi chú bàn giao

**Tập:** Vì sao tình báo Anh thả xác một người lạ xuống biển Tây Ban Nha?
**Phiên bản:** v1 · Shorts 1080 × 1920, 30 fps · dài 1:44,6 (theo MP3) · phong cách Midway v2, **có hiệu ứng tiếng**

## Bộ file

| File | Nội dung |
|---|---|
| `build/Mincemeat_v1.mp4` | Bản đầy đủ: H.264 CRF 19, AAC 192 kbps, phụ đề in cứng, giọng + 168 hiệu ứng; −14,2 LUFS, đỉnh −1,1 dBTP |
| `build/Mincemeat_v1.srt` | Phụ đề riêng |
| `build/sfx_stem.wav` | Riêng lớp hiệu ứng |
| `build/contact_sheet.png` | Dải khung hình |
| `assets/screenshots/` | 16 ảnh chụp màn hình gốc chủ kênh gửi (để truy nguồn) |
| `assets/photos/` | Ảnh đã cắt từ ảnh chụp màn hình, chỉ gồm ảnh đã xác minh |

Xuất lại: `python3 src/align.py && python3 src/render.py full && mv build/Mincemeat_v1.mp4 build/Mincemeat_v1_nosfx.mp4 && python3 src/sfx_events.py`

## Việc cần chủ kênh quyết

1. **Ảnh chưa xác minh (chưa đưa vào video)** — xem bảng dưới. Nếu chủ kênh xác nhận, Claude thay vào:
   - ảnh đổ bộ ("The_Invasion_of…") cho đoạn 87,6–91,5 s (hiện là bản đồ);
   - ảnh hai sĩ quan cạnh xe ("Charles_Cholmo…") cho đoạn 13,7–16,1 s ("cái bẫy do tình báo Anh dựng lên").
2. **Mốc giây là ước lượng**; ranh giới câu khớp khoảng lặng tốt.
3. **Hiệu ứng tiếng:** Claude không nghe được; dấu/cú nhấn ~7 dB dưới giọng, tự hạ ~7 dB khi có lời.
4. **Đoạn 70–91 s toàn đồ họa (~21 s)** vì chưa có ảnh xác minh cho các sự kiện tháng 5–7/1943; ảnh đổ bộ Sicily (nếu xác nhận) sẽ chia nhỏ đoạn này.

## Bảng xác minh ảnh (theo quy tắc dùng ảnh của kênh)

| Ảnh chụp màn hình | Nội dung | Căn cứ xác minh | Dùng |
|---|---|---|---|
| 1000043745 | Thẻ quân nhân "William Martin" | Chữ trên thẻ: MARTIN William, Captain RM (Acting Major), Cardiff 1907, 2/2/1943 | ✓ 11,6–16,1 s; ô nhỏ 40 s — chú thích: ảnh trên thẻ là một sĩ quan MI5 |
| 1000043746 | Ảnh "Pam" | Trang Commons "UK National Archives – WO 106/5921" (hồ sơ Mincemeat) | ✓ 40,9 s (ô nhỏ), 48,2–50,8 s |
| 1000043747 | Tướng Archibald Nye | Tên file "Archibaldnye" (chưa thấy trang mô tả) | ✓ 52,9–55,5 s — mức chắc chắn: theo tên file |
| 1000043748 | Tướng Harold Alexander (chân dung màu) | Tên file "Harold_Alexand…" | ✓ 54,2–55,5 s — theo tên file |
| 1000043749 | HMS Seraph, thủy thủ đoàn trên tháp | Chữ "SERAPH" trên tháp tàu | ✓ 66,9–70,4 s |
| 1000043750 | Tàu ngầm số hiệu P219 | P219 là số hiệu của HMS Seraph | Dự phòng (chưa dùng) |
| 1000043755, 56 | Bia mộ ở Huelva | Đọc được dòng "GLYNDWR MICHAEL SERVED AS MAJOR WILLIAM MARTIN, RM" | ✓ 91,5–104,6 s (chụp sau này) |
| 1000043757 | Trang Commons "William Martin Lapida-2011-08-12" | Cùng bia mộ, ảnh 2011 | Trùng, không dùng |
| 1000043741, 42 | Hai sĩ quan cạnh xe tải | Tên file "Charles_Cholmo…" bị cắt; không thấy chú thích ai là ai | **Chưa xác minh — hỏi chủ kênh** |
| 1000043744 | Bản đồ Sicily 1943 | Ảnh 250px, quá nhỏ | Không dùng (tự vẽ bản đồ) |
| 1000043751 | "The_officers_of_…" — sĩ quan hải quân cầm mô hình tàu | Tên file bị cắt, không rõ tàu nào | **Chưa xác minh** |
| 1000043752 | "The_Royal_Navy…" — tàu đổ bộ, lính lên bờ | Tên file bị cắt, không rõ địa điểm | **Chưa xác minh** |
| 1000043753, 54 | "The_Invasion_of…" — lính lội nước / hành quân | Tên file bị cắt ("of …"), chưa chắc là Sicily | **Chưa xác minh** |
| — | Glyndwr Michael | Không có ảnh được xác nhận | Hình bóng trung tính + ghi chú "Không có ảnh nào được xác nhận là của ông" |

## Bảng dựng theo mốc giây

| Mốc | Lời | Hình | Hiệu ứng |
|---|---|---|---|
| 0–6,65 | "30/4/1943… ngư dân… Huelva" | Bản đồ Iberia, thuyền đánh cá, ghim Huelva | Sóng biển |
| 6,65–11,6 | "chiếc cặp… thư mật" | Cặp có xích, mở ra, hai lá thư, dấu "MẬT" | Xích, khóa bật, dấu |
| 11,6–16,1 | "chưa từng là sĩ quan… cái bẫy" | Thẻ quân nhân giả, dấu "GIẢ" | Dấu |
| 16,1–26,2 | "Sicily… ai nhìn bản đồ cũng đoán… Hy Lạp, Sardinia" | Bản đồ Địa Trung Hải: Bắc Phi → Sicily, rồi Hy Lạp, Sardinia (đỏ) | Bút vẽ |
| 26,2–31,8 | "Glyndwr Michael…" | Hình bóng trung tính + thẻ tên | — |
| 31,8–35,9 | "Thiếu tá William Martin…" | Hình bóng đội mũ sĩ quan, thẻ tên mới | Giấy |
| 35,9–48,2 | các món trong túi | Lưới 6 món, bật ra theo từng chữ (thẻ và ảnh Pam là ảnh thật) | Giấy |
| 48,2–50,8 | "nhân viên MI5" | Ảnh "Pam" = Jean Leslie | — |
| 50,8–58,7 | "thư Nye gửi Alexander… bản nháp… tự viết" | Hai chân dung, phong bì bay; giấy nháp vo tròn; lá thư viết tay hiện dần | Giấy, bút |
| 58,7–64,8 | nội dung thư | Thư đánh máy (diễn ý), tô vàng "SICILY: CHỈ ĐỂ ĐÁNH LẠC HƯỚNG" | Máy chữ |
| 64,8–70,4 | "hộp thép băng khô… tàu ngầm… Huelva" | Hộp thép + hơi lạnh; ảnh HMS Seraph | Hơi xì, tàu ngầm trầm |
| 70,4–74,6 | "trung lập nhưng thân Đức… lọt tới tình báo Đức" | Tây Ban Nha tô xám rồi đỏ; tài liệu đi từ Huelva tới "tình báo Đức" | Lướt |
| 74,6–76,9 | "cặp trả về cho Anh" | Cặp trượt về, nhãn navy | Lướt |
| 76,9–82,2 | "14/5… bức điện Đức… Hy Lạp" | Điện giải mã (diễn ý), kính lúp, dấu "ĐỨC ĐÃ TIN" | Bíp điện báo, máy chữ, dấu |
| 82,2–87,6 | "điều thêm quân… sư đoàn thiết giáp từ Pháp" | Bản đồ: mũi tên đỏ tới Sardinia, Hy Lạp; xe tăng Pháp → Hy Lạp | Xích xe tăng |
| 87,6–91,5 | "tháng 7/1943 đổ bộ Sicily" | Bản đồ: mũi tên navy từ phía nam lên Sicily | Sóng |
| 91,5–96,4 | "chôn ở Huelva… dưới tên William Martin" | Ảnh mộ (chụp sau này), khung vàng dòng "WILLIAM MARTIN" | Gió |
| 96,4–104,6 | "1998… khắc thêm một dòng" | Cận dòng khắc 1998, bản dịch, tối dần | Gió |
