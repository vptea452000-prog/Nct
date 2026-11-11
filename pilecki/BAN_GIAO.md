# Pilecki v1 — ghi chú bàn giao

**Tập:** Vì sao một sĩ quan Ba Lan tự nộp mình vào Auschwitz?
**Phiên bản:** v1 · Shorts 1080 × 1920, 30 fps · dài 1:42,4 (theo MP3) · phong cách Midway v2, **có hiệu ứng tiếng**

## Bộ file

| File | Nội dung |
|---|---|
| `build/Pilecki_v1.mp4` | Bản đầy đủ: H.264 CRF 19, AAC 192 kbps, phụ đề in cứng, giọng + hiệu ứng; −14,1 LUFS, đỉnh −1,1 dBTP |
| `build/Pilecki_v1.srt` | Phụ đề riêng |
| `build/sfx_stem.wav` | Riêng lớp hiệu ứng (để chỉnh trong CapCut) |
| `build/contact_sheet.png` | Dải khung hình, 1 khung mỗi 1,5 s |
| `src/` | `scenes.py` (bảng dựng), `sfx_events.py` (hiệu ứng), `lib.py`, `subs.py`, `align.py`, `render.py` |

Xuất lại: `python3 src/align.py && python3 src/render.py full && mv build/Pilecki_v1.mp4 build/Pilecki_v1_nosfx.mp4 && python3 src/sfx_events.py`

## Việc cần xử lý trước khi đăng

1. **"945 ngày" (66,0–67,0 s)** — phép tính cho 946–947 ngày (tài liệu thường ghi 947). Chữ trên hình đã để trung tính: chỉ ghi "22.9.1940 → 27.4.1943", không ghi số ngày. Chủ kênh quyết thu lại hay giữ.
2. **Mốc giây là ước lượng** (căn theo khoảng lặng + số âm tiết; các ranh giới câu khớp khoảng lặng rất tốt). Đoạn 64,6–67,0 s đã đối chiếu thêm bằng đỉnh âm lượng.
3. **Xác minh chú thích ảnh** (bảng dưới), nhất là ảnh vây bắt ở Warsaw và ảnh mộ tượng trưng.
4. **Hiệu ứng tiếng:** Claude không nghe được âm thanh; mức đã đo (cú nhấn ~10–15 dB dưới giọng, tự hạ ~7 dB khi có lời). Cần chủ kênh nghe duyệt.

## Bảng dựng theo mốc giây

| Mốc | Lời (cụm kích hoạt) | Hình | Nguồn | Hiệu ứng |
|---|---|---|---|---|
| 0,0–4,5 | "Tháng 9 năm 1940… phố Warsaw" | Ảnh vây bắt, đẩy chậm; chip ngày; nhãn WARSAW | Ảnh thật | Tiếng động cơ xe trầm |
| 4,5–8,05 | "không tìm cách trốn… cố ý để mình bị bắt" | Người giấy: đám đông bỏ chạy, một người đứng yên (khoanh vàng), rồi bước về phía xe tải | Đồ họa | Bước chân |
| 8,05–9,67 | "đưa vào Auschwitz" | Bản đồ Warsaw → Auschwitz | Đồ họa | Bút vẽ, gõ nhẹ |
| 9,67–13,27 | "Witold Pilecki…" | Chân dung, thẻ tên | Ảnh thật (bản tô màu, đã đưa về đen trắng) | Giấy |
| 13,27–15,6 | "trại tập trung mới mở" | Cổng Auschwitz I (chụp sau này) | Ảnh thật | Gió |
| 15,6–24,2 | "không ai biết… nhiệm vụ…" | Hàng rào: bên ngoài / bên trong; 3 bước nhiệm vụ; chấm vàng vào trong, nối nhóm, tin ra ngoài | Đồ họa | Gõ nhẹ theo từng bước |
| 24,2–25,3 | "giấy tờ giả" | Giấy tờ che tên, dấu "GIẤY TỜ GIẢ" | Đồ họa | Giấy, dấu |
| 25,3–28,7 | "hai ngày bị giam… doanh trại cũ" | Lịch 19–21/9/1940, chip "HAI NGÀY BỊ GIAM" (không minh họa đánh đập) | Đồ họa | Tích tắc |
| 28,7–30,3 | "đưa tới Auschwitz" | Bản đồ, chip 22.9.1940 | Đồ họa | Tiếng tàu trầm |
| 30,3–36,3 | "tù nhân số 4859… Tomasz Serafiński… không phải của ông" | Ảnh hồ sơ tù, khoanh số 4859; tên đánh máy rồi gạch đỏ; "tên thật: WITOLD PILECKI" | Ảnh thật | Màn trập máy ảnh, máy chữ |
| 36,3–44,5 | "người tin được… vị trí quan trọng… chuyển ra ngoài" | Ảnh trinh sát 1944, chấm vàng nối thành mạng, tin đi ra ngoài | Ảnh thật + đồ họa | Gõ nhẹ |
| 44,5–49,75 | "1943, Gestapo truy lùng… nhiều người bị giết" | Sơ đồ mạng; vòng quét đỏ; 4 nút tắt màu, gạch chéo | Đồ họa | Tiếng trầm kéo dài |
| 49,75–52,2 | "tự mình ra ngoài" | Ảnh chính diện số 4859 | Ảnh thật | — |
| 52,2–64,6 | "lò bánh mì… đêm 26/4/1943… cắt dây… lính gác bắn" | Cảnh đêm giấy cắt: hàng rào, tháp canh, lò bánh mì, dây điện thoại đứt, ba người chạy, chớp súng; nhãn "theo lời Pilecki kể lại" | Đồ họa | Gió đêm, cắt dây, cửa kẽo kẹt, bước chạy, súng vọng xa |
| 64,6–67,4 | "945 ngày" | 22.9.1940 → 27.4.1943 trên nền khu nhà trại | Ảnh thật (chụp sau này) | — |
| 67,4–72,3 | "báo cáo… London… không mấy tin" | Trang "RAPORT" (minh họa), bay tới London, mờ đi kèm dấu "?" | Đồ họa | Máy chữ |
| 72,3–80,2 | "chính quyền cộng sản… lưu vong ở London… trở về" | Bản đồ châu Âu, Ba Lan tô đỏ, London; mũi tên trở về | Đồ họa | Tiếng trầm |
| 80,2–85,9 | "tháng 5/1947 bị bắt… xét xử… gián điệp" | Ảnh hồ sơ MBP 1947; ảnh Pilecki tại phiên tòa 1948 | Ảnh thật | Màn trập, búa tòa |
| 85,9–91,0 | "25/5/1948… nhà tù Mokotów" | Biên bản thi hành án (tô dòng ngày); nhà tù Mokotów (chụp sau này) | Ảnh thật | Cửa sắt |
| 91,0–92,5 | "chôn bí mật" | Các lớp đất, viền đứt mờ dần | Đồ họa | Tiếng trầm |
| 92,5–96,5 | "1990… vô tội" | Chân dung + dấu "VÔ TỘI" (xanh navy) | Ảnh thật | Dấu |
| 96,5–98,8 | "báo cáo vẫn còn" | Trang báo cáo (minh họa) | Đồ họa | Giấy |
| 98,8–102,4 | "nơi chôn… chưa ai tìm thấy" | Mộ tượng trưng (chụp sau này), tối dần | Ảnh thật | Gió |

## Tư liệu đã dùng

Ảnh do chủ kênh gửi; chú thích là nhận diện của Claude, **cần đối chiếu trang gốc** (Bảo tàng Auschwitz-Birkenau, IPN, Viện Pilecki, NARA).

| File | Nhận diện |
|---|---|
| `roundup_warsaw.jpg` | Một cuộc vây bắt ở Warsaw thời Đức chiếm đóng — không rõ ngày, không phải ảnh ngày 19/9/1940 (chú thích trên hình đã ghi chung) |
| `pilecki_color.jpg` | Chân dung Pilecki trong quân phục (bản tô màu, dựng về đen trắng) |
| `pilecki_portrait.jpg` | Chân dung Pilecki (đen trắng) |
| `gate_modern.jpg`, `gate_building_modern.jpg` | Cổng và khu nhà Auschwitz I, chụp sau này |
| `mugshot_4859.jpg` | Ảnh hồ sơ tù Auschwitz số 4859 (Bảo tàng Auschwitz-Birkenau) |
| `aerial_1944.jpg` | Ảnh trinh sát của Đồng minh, 25/8/1944, chú thích tiếng Anh thêm sau chiến tranh |
| `mugshot_mbp_1947.jpg` | Ảnh hồ sơ MBP Warszawa 1947 (IPN) |
| `trial_1948.jpg` | Pilecki tại phiên tòa 3/1948 |
| `execution_protocol.jpg` | Biên bản thi hành án tử hình, 25/5/1948 |
| `mokotow_modern.jpg` | Nhà tù Mokotów, phố Rakowiecka, chụp sau này |
| `grave_symbolic.jpg` | Bia mộ tượng trưng của Pilecki (hài cốt chưa tìm thấy), chụp sau này |
| Không dùng | `aerial_1944_crop.jpg`, `courtroom_1948*.jpg` (trùng nội dung), `cell_modern.jpg` (không rõ có phải phòng giam Pilecki) |

Bản đồ: Natural Earth (phạm vi công cộng), **không vẽ biên giới** vì biên giới hiện đại khác năm 1940; riêng Ba Lan tô màu ở đoạn sau 1945 (biên giới gần với ngày nay).
