# Garbo v1 — ghi chú bàn giao

**Tập:** Vì sao một điệp viên được cả Hitler lẫn nước Anh trao huân chương?
**Phiên bản:** v1 · Shorts 1080 × 1920, 30 fps · dài 1:50,0 (theo MP3) · phong cách Midway v2, **có hiệu ứng tiếng**

## Bộ file

| File | Nội dung |
|---|---|
| `build/Garbo_v1.mp4` | Bản đầy đủ: H.264 CRF 19, AAC 192 kbps, phụ đề in cứng, giọng + 266 hiệu ứng; −14,1 LUFS, đỉnh −1,3 dBTP |
| `build/Garbo_v1.srt` | Phụ đề riêng |
| `build/sfx_stem.wav` | Riêng lớp hiệu ứng |
| `build/contact_sheet.png` | Dải khung hình |
| `src/` | `scenes.py` (bảng dựng), `sfx_events.py` (hiệu ứng), `lib.py`, `subs.py`, `align.py`, `render.py` |

Xuất lại: `python3 src/align.py && python3 src/render.py full && mv build/Garbo_v1.mp4 build/Garbo_v1_nosfx.mp4 && python3 src/sfx_events.py`

## Việc cần xử lý trước khi đăng

1. **Mốc giây là ước lượng** (khoảng lặng + số âm tiết); ranh giới câu khớp khoảng lặng tốt. Cần nghe duyệt các điểm: "Thập tự Sắt" (2,4 s), "huân chương" (5,0 s), "từ chối" (14,9 s), "Garbo" (46,9 s), "Pas-de-Calais" (77,2 s), "Hitler" (78,5 s).
2. **Hiệu ứng tiếng:** Claude không nghe được; mức đã đo (dấu/cú nhấn ~8 dB dưới giọng, tự hạ ~7 dB khi có lời).
3. **Xác minh ảnh** theo bảng dưới; hai ảnh chưa nhận diện được nên chưa dùng.
4. **Chi tiết thêm trên hình (không có trong lời đọc):** báo cáo gửi tới trạm tình báo Đức ở *Madrid* (đúng theo nguồn: Abwehr điều khiển Pujol từ Madrid); giờ gửi điện sáng 6/6 khoảng 3 giờ, đổ bộ khoảng 6 giờ 30, tin tới khoảng 8 giờ (theo các nguồn); tên nhà sử học **Nigel West**. Chủ kênh có thể yêu cầu bỏ nếu muốn hình chỉ theo lời.

## Bảng dựng theo mốc giây

| Mốc | Lời (cụm kích hoạt) | Hình | Nguồn | Hiệu ứng |
|---|---|---|---|---|
| 0–8,15 | "Thập tự Sắt… huân chương… cùng một chuỗi bức điện" | Thập tự Sắt (ĐỨC, đỏ) và MBE (ANH, navy) đặt xuống; dải băng điện báo nối hai bên | Ảnh hiện vật | Tiếng ngân huân chương, bíp điện báo |
| 8,15–11,1 | "Juan Pujol… ghét Hitler" | Chân dung, thẻ tên | Ảnh thật | Giấy |
| 11,1–18,5 | "1941… bị từ chối… đổi cách… tình báo Đức" | Bàn "NGƯỜI ANH" bị dấu TỪ CHỐI; ảnh Pujol nhảy sang bàn "TÌNH BÁO ĐỨC" | Đồ họa + ảnh thật | Dấu, lướt |
| 18,5–26,2 | "hứa sang Anh… không sang Anh… Lisbon… như thể ở London" | Bản đồ Madrid → London (gạch X), ghim Lisbon, phong bì đóng dấu bưu điện "LONDON" giả | Đồ họa | Bút, dấu |
| 26,2–30,6 | "sách du lịch, bản đồ, bảng giờ tàu, phim thời sự" | Bốn món tư liệu bật ra theo từng chữ | Đồ họa | Giấy |
| 30,6–37,9 | "một lít rượu vang… không dùng lít… vẫn tin" | Báo cáo đánh máy (diễn ý), khoanh đỏ "LÍT", dấu "ĐỨC VẪN TIN" | Đồ họa | Máy chữ, dấu |
| 37,9–41,4 | "tình báo Anh nhận ra… tìm tới ông" | Điện Đức bị giải mã (minh họa) + kính lúp; mũi tên tới ảnh Pujol | Đồ họa + ảnh | Lướt |
| 41,4–47,75 | "1942… hai mang… MI5… Garbo" | Ảnh Pujol, dấu "GARBO" (navy) | Ảnh thật | Dấu |
| 47,75–53,0 | "27 điệp viên… Đức gửi tiền" | Sơ đồ mạng lưới Garbo (hồ sơ MI5); tiền bay vào | Ảnh tài liệu + đồ họa | Tiền rơi |
| 53,0–59,8 | "1944… Normandy… Pas-de-Calais" | Bản đồ Overlord TOP SECRET; bản đồ eo biển: Normandy (thật) / Pas-de-Calais (điều Đức phải tin) | Tài liệu + đồ họa | — |
| 59,8–62,9 | "hơn năm trăm bức điện" | Bộ đếm 0 → 500+, chồng điện cao dần | Đồ họa | Bíp điện báo |
| 62,9–71,4 | "Sáng 6/6… báo trước… quá muộn… càng tin" | Ảnh Omaha "Into the Jaws of Death"; trục giờ: gửi → đổ bộ → tin tới; dấu "ĐỨC CÀNG TIN" | Ảnh thật + đồ họa | Sóng, pháo trầm, tích tắc |
| 71,4–79,9 | "bức điện quan trọng nhất… lên tới tận Hitler" | Điện 9/6 đánh máy (diễn ý), tô vàng PAS-DE-CALAIS; "LÊN TỚI HITLER" | Đồ họa | Máy chữ, cú nhấn |
| 79,9–84,0 | "các đơn vị Đức… dừng lại… không bao giờ đến" | Xe tăng đỏ đi về Normandy, gặp biển DỪNG, quay lại; mũi tên từ Dover mờ dần | Đồ họa | Xích xe tăng, dấu |
| 84,0–90,2 | "29/7… Thập tự Sắt… MBE" | Thập tự Sắt + sóng vô tuyến; MBE vào cạnh | Ảnh hiện vật | Vô tuyến, ngân |
| 90,2–96,6 | "loan tin… chết vì sốt rét… 1949" | Cáo phó giả, dấu "TIN GIẢ" | Đồ họa | Dấu, máy chữ |
| 96,6–99,5 | "Venezuela… cửa hàng nhỏ" | Hộ chiếu Venezuela của Pujol | Ảnh thật | — |
| 99,5–102,2 | "35 năm sau… nhà sử học Anh" | Bộ đếm 1949 → 1984 | Đồ họa | Tích tắc |
| 102,2–110,0 | "tháng 6/1984… bãi biển Normandy… 40 năm" | Bãi biển giấy cắt + ảnh Pujol; tối dần | Đồ họa + ảnh | Sóng biển |

## Tư liệu

Ảnh do chủ kênh gửi; chú thích là nhận diện của Claude, **cần đối chiếu trang gốc**.

| File | Nhận diện | Ghi chú |
|---|---|---|
| `iron_cross.jpg` | Thập tự Sắt hạng Hai (1939), ảnh hiện vật | Hiện vật cùng loại, không phải chiếc của Pujol |
| `mbe.jpg` | Huân chương MBE (hai mặt) | Hiện vật cùng loại |
| `pujol_beard.jpg` | Juan Pujol (ảnh thường dùng) | Chưa rõ năm chụp |
| `pujol_young.jpg` | Ảnh Pujol thời trẻ (độ phân giải thấp, chỉ dùng cỡ nhỏ) | Cần xác nhận đúng là Pujol |
| `garbo_network.jpg` | Sơ đồ "THE GARBO NETWORK" trong hồ sơ MI5 | |
| `overlord_map.jpg` | Bản đồ khu C, kế hoạch Overlord, TOP SECRET, 5/1944 | |
| `omaha_jaws.jpg` | "Into the Jaws of Death", Omaha, 6/6/1944 (Robert F. Sargent, NARA) | |
| `venezuela_passport.jpg` | Hộ chiếu Venezuela mang tên Juan Pujol García | |
| Chưa dùng | `bodyguard_map.jpg` (bản đồ hiện đại các chiến dịch nghi binh), `bigot_document.jpg`, `eisenhower_order.jpg` (có thể dùng ở bản sau); `unidentified_portrait.jpg`, `unidentified_coast_aerial.jpg` (chưa nhận diện được) | |
