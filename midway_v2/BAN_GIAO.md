# Midway v2 — ghi chú bàn giao

**Tập:** Bức điện báo thiếu nước ở Midway đã khiến quân Nhật để lộ điều gì?
**Phiên bản:** v2 · Shorts 1080 × 1920, 30 fps · dài 1:39,8 (theo MP3)

## Bộ file

| File | Nội dung |
|---|---|
| `build/Midway_v2.mp4` | Bản đầy đủ: H.264 CRF 19, yuv420p, AAC 192 kbps, phụ đề in cứng |
| `build/Midway_v2.srt` | Phụ đề riêng (UTF-8) |
| `build/contact_sheet.png` | Dải khung hình toàn tập, 1 khung mỗi 1,5 s |
| `src/` | Mã dựng: `scenes.py` (bảng dựng), `lib.py` (đồ họa), `subs.py` (phụ đề), `align.py` (căn mốc), `render.py` (xuất) |
| `src/script.txt` | Kịch bản đúng bản chủ kênh gửi |
| `build/words.json` | Mốc giây từng chữ (ước lượng) |
| `assets/photos/` | Ảnh chủ kênh gửi, đã đặt tên theo nội dung |
| `audio/voice.mp3` | Giọng đọc gốc |

Xuất lại: `python3 src/align.py && python3 src/render.py full` (cần skia-python, pyshp, ffmpeg).

## Việc cần xử lý trước khi đăng

1. **Câu "gửi về Tokyo" (giây 73,1–75,4)** vẫn nằm trong bản thu. Chủ kênh cần quyết: thu lại câu này, hoặc giữ nguyên và ghi chú. Chữ trên hình đã để trung tính: chỉ ghi "BẢN DỊCH ĐIỆN NHẬT", không vẽ mũi tên về Tokyo.
2. **Mốc thời gian là ước lượng.** Chưa có SRT từ CapCut và chưa có công cụ chuyển giọng nói thành chữ, nên mốc được căn theo khoảng lặng và số âm tiết. Riêng đoạn 75,8–79,4 s được đối chiếu thêm bằng đỉnh âm lượng. Cần nghe duyệt lại các điểm: "AF" (29,26 s và 87,36 s), "hai tuần" (5,85 s và 83,03 s), tên Rochefort (15,8 s), Nimitz (38,5 s). Có SRT CapCut thì gửi để căn chính xác.
3. **Xác minh chú thích ảnh** theo bảng tư liệu bên dưới, nhất là ảnh tàu Enterprise và Hornet.
4. **Chưa dùng được phim John Ford** *The Battle of Midway* (môi trường chưa tải được). Bản này chỉ dùng ảnh tĩnh.

## Bảng dựng theo mốc giây

| Mốc | Lời (cụm kích hoạt) | Hình | Nguồn | Nối cảnh |
|---|---|---|---|---|
| 0,00–2,65 | "Ngày 20 tháng 5 năm 1942" | Ảnh không ảnh Midway, đẩy chậm; chip ngày; nhãn "ĐẢO MIDWAY" | Ảnh thật (atoll) | Cắt |
| 2,65–10,0 | "báo về Hawaii… hai tuần… tiếp tế ngay" | Bản đồ Midway→Hawaii, mũi tên vẽ theo "báo về"; điện cầu cứu đánh máy dần, tô vàng "HAI TUẦN" ở 5,85 s; nhãn DIỄN Ý | Đồ họa | Kéo bản đồ |
| 9,35 | "nghĩ ra" | Dấu đỏ "MỒI NHỬ" đóng xuống | Đồ họa | — |
| 10,0–12,45 | "phát tin ấy để quân Nhật nghe được" | Thẻ điện bay về Midway, sóng vô tuyến lan ra, ăng-ten đỏ "QUÂN NHẬT" | Đồ họa | Cắt |
| 12,45–18,28 | "Trân Châu Cảng… Joseph Rochefort" | Ảnh Rochefort đặt xuống; chip "TRÂN CHÂU CẢNG"; thẻ tên ở 15,4 s | Ảnh thật | Cắt |
| 18,28–25,0 | "đọc được một phần… chiến dịch lớn vào tháng Sáu" | Điện mật: một số nhóm mã lật thành chữ, số còn lại xám; tô vàng "CHIẾN DỊCH LỚN", "THÁNG 6"; nhãn MINH HỌA | Đồ họa | Phóng nhẹ |
| 25,0–29,96 | "tên mục tiêu… hai chữ cái: AF" | Ô "MỤC TIÊU" trống nhấp nháy; "AF" đập vào đúng 29,26 s, giữ hết khoảng nghỉ | Đồ họa | Cắt |
| 29,96–34,69 | "AF là Midway… giữa Thái Bình Dương" | Chip "AF = ?" bay vào Midway ở 32,0 s; bản đồ lùi ra, chữ "THÁI BÌNH DƯƠNG" | Đồ họa | Cắt |
| 34,69–37,69 | "nơi khác, kể cả Hawaii" | Ảnh Trân Châu Cảng; "AF = nơi khác?" rồi "AF = HAWAII?" ở 36,9 s | Ảnh thật + nhãn | Cắt |
| 37,69–40,66 | "Đô đốc Chester Nimitz… Hạm đội Thái Bình Dương" | Chân dung Nimitz, nhịp vào rồi đứng yên; thẻ tên | Ảnh thật | Cắt |
| 40,66–46,36 | "đoán nhầm… phục kích ở một nơi… đánh vào nơi khác" | Chip đỏ "NẾU ĐOÁN NHẦM"; ba tàu sân bay đi phục kích sai chỗ; máy bay Nhật đánh vào Midway | Đồ họa (giả định) | Cắt |
| 46,36–51,26 | "kiểm tra… Midway là AF hay không" | Thẻ "AF = MIDWAY ?", kính lúp "KIỂM TRA" | Đồ họa | Cắt |
| 51,26–53,56 | "một hòn đảo giữa biển" | Ảnh Midway, đẩy vào đảo Sand | Ảnh thật | Cắt |
| 53,56–55,28 | "máy chưng cất nước ngọt bị hỏng" | Máy rung, khói bốc, kim tụt, mực nước hạ, dấu "HỎNG" ở 54,64 s | Đồ họa (minh họa) | Cắt |
| 55,28–61,4 | "hai đường liên lạc… đường cáp từ Hawaii tới Midway" | Chú giải 2 đường; cáp vẽ dọc chuỗi đảo, thẻ "LỆNH MẬT" chạy theo cáp | Đồ họa | Kéo bản đồ |
| 61,4–67,6 | "phát qua vô tuyến… lời thông thường… ai bắt đúng sóng" | Thẻ "MÁY CHƯNG CẤT HỎNG / THIẾU NƯỚC", "KHÔNG MÃ HOÁ", sóng đỏ lan tới phía Nhật | Đồ họa | Cắt |
| 67,6–69,86 | "phía Mỹ quay sang nghe điện" | Ảnh Rochefort (lần 2), sóng đỏ từ mép trái đi vào | Ảnh thật + đồ họa | Cắt |
| 69,86–75,8 | "22 tháng 5… Melbourne, Úc… bản dịch" | Bản đồ có Melbourne; bản dịch bay ra từ Melbourne | Đồ họa | Phóng tài liệu |
| 75,8–83,6 | "đơn vị không quân ở AF… hai tuần" | Bản dịch đánh máy, tô vàng "AF" (78,0 s); thẻ điện Midway trượt vào, nối hai chữ "HAI TUẦN" (83,05 s) | Đồ họa (diễn ý) | Cắt |
| 83,6–87,97 | "chính Midway đã phát… AF" | Ảnh Midway nguyên khung; chip "AF" đập lên đảo ở 87,36 s | Ảnh thật + nhãn | Cắt |
| 87,97–90,43 | "Sáng ngày 4 tháng 6… tàu sân bay Nhật" | Ảnh tàu Hiryu bị ném bom; chip ngày | Ảnh thật | Cắt |
| 90,43–91,37 | "đến đánh Midway" | Ảnh kho dầu Midway bốc cháy | Ảnh thật | Cắt |
| 91,37–94,95 | "ba tàu sân bay Mỹ" | Ba dải ảnh lần lượt: Enterprise, Hornet, Yorktown | Ảnh thật | Cắt |
| 94,95–99,8 | "Từ lúc… mới mười lăm ngày" | Nền Midway cháy làm tối; lịch 20/5→4/6 chạy; chip "MỚI 15 NGÀY" ở 98,0 s | Ảnh thật + đồ họa | Hết |

Đoạn dài nhất chỉ có đồ họa là 18,3–34,7 s (khoảng 16 s), nhỉnh hơn mức "khoảng 15 s". Nguyên nhân là chưa có tư liệu thật cho đoạn giải mã. Nếu có ảnh văn phòng HYPO hoặc ảnh máy mã, có thể chèn vào khoảng 20–22 s.

## Danh sách tư liệu và quyền sử dụng

Tất cả ảnh dưới đây do chủ kênh gửi. Chú thích là nhận diện của Claude theo nội dung ảnh, **cần đối chiếu với trang gốc** (NHHC/NARA) trước khi đăng. Ảnh của Hải quân và chính phủ liên bang Mỹ thường thuộc phạm vi công cộng tại Mỹ, nhưng vẫn cần ghi nguồn.

| File | Dùng ở | Nhận diện | Độ chắc chắn |
|---|---|---|---|
| `atoll.jpg` | 0–2,6 s; 51,3–53,6 s; 83,6–88 s | Midway nhìn từ trên không, đảo Eastern phía trước, đảo Sand phía sau, khoảng 11/1941 (trên hình ghi "chụp 11/1941") | Địa điểm chắc chắn; ngày cần xác minh |
| `rochefort.jpg` | 12,5–18,3 s; 67,6–69,9 s | Joseph Rochefort tại bàn làm việc (quân hàm đại tá, chụp sau trận) | Cao |
| `yorktown.jpg` | 34,7–37,7 s; 91,4–95 s | USS Yorktown (CV-5) trong ụ khô Trân Châu Cảng, cuối 5/1942 (thấy số 5 ở mũi tàu) | Cao; ngày 29/5 cần xác minh |
| `nimitz.jpg` | 37,7–40,7 s | Đô đốc Chester Nimitz, khoanh tay | Cao; chưa rõ ngày chụp |
| `hiryu.jpg` | 88–90,4 s | Tàu sân bay Nhật (thường chú thích là Hiryu) né bom B-17, 4/6/1942 | Khá; tên tàu cần xác minh |
| `burning.jpg` | 90,4–91,4 s; 95–99,8 s | Kho dầu cháy trên đảo Sand, Midway, 4/6/1942 (có chim hải âu) | Cao |
| `enterprise.jpg` | 91,8–95 s | Tàu sân bay Mỹ có radar CXAM, trong cảng; Claude nhận là USS Enterprise | **Cần xác minh** |
| `hornet.jpg` | 92–95 s | Tàu sân bay Mỹ sơn ngụy trang loang; Claude nhận là USS Hornet (CV-8) | **Cần xác minh** |
| `nimitz_bunker.jpg` | Không dùng | Nimitz bước ra khỏi hầm cát | Chưa rõ địa điểm, ngày; không dùng để tránh gán sai |
| `planes_unverified.jpg` | Không dùng | Ảnh/tranh đội hình máy bay, nhiều khả năng đã chỉnh sửa hoặc dàn dựng | Không rõ nguồn; dễ bị hiểu là bằng chứng nên không dùng |

Bản đồ: Natural Earth (110m, phạm vi công cộng). Font: Inter (OFL), Liberation Mono (OFL).

## Nguồn sự kiện cần đối chiếu

- NSA Center for Cryptologic History, về vai trò của Rochefort, HYPO và mẹo "AF".
- Naval History and Heritage Command, *Battle of Midway*: mốc 20/5 (tin thiếu nước), bản dịch của FRUMEL Melbourne, 4/6/1942.
- Mốc "mười lăm ngày": từ 20/5 đến 4/6/1942, đã đếm trên lịch.

## Phần chưa nghe duyệt được

Claude không nghe được nội dung MP3, nên chưa xác nhận được lời thu khớp từng chữ với `script.txt`. Năm lượt duyệt đã chạy được: lượt 1 (lời và sự kiện, theo kịch bản), lượt 3 (dải khung hình), lượt 4 (bố cục vùng an toàn, cỡ chữ ≥ 26 px, dấu tiếng Việt) và lượt 5 (file xuất). **Lượt 2 (khớp lời với hình) mới đối chiếu theo mốc ước lượng**, cần chủ kênh xem trên điện thoại và góp ý theo mốc giây.

## Thay đổi so với v1

- Phối ảnh tư liệu thật, khoảng 40% thời lượng, thay cho bản toàn đồ họa.
- Font tài liệu đổi sang Liberation Mono để đủ dấu viết hoa (DejaVu Sans Mono mất dấu ở Ở, Ỉ, Ầ, Ế).
- Chữ trên hình về bức điện Nhật để trung tính (không ghi "gửi về Tokyo").
- Không còn khung trống khi đang có lời.

## Phiên bản đã chốt

**Chủ kênh chọn v2 (11/11/2026).** Bản v3 (thêm chuyển cảnh trượt, chất phim, rung khung, tô vàng từ khoá trong phụ đề) không được chọn; mã v3 vẫn còn trong lịch sử git (commit 74aee71) để tham khảo. Các tập sau giữ phong cách v2 làm mốc.

## Bản có hiệu ứng âm thanh (thử nghiệm, chờ chủ kênh chọn)

`build/Midway_v2_sfx.mp4`: hình giữ nguyên v2, thêm 248 hiệu ứng **tự tổng hợp bằng code** (`src/sfx.py`, không dùng file ngoài nên không vướng bản quyền), mỗi hiệu ứng bám đúng mốc chuyển động trên hình.

- Máy chữ theo từng chữ điện văn; dấu "MỒI NHỬ", "HỎNG", "4/6" đóng xuống; giấy trượt, ảnh đặt xuống; ghim/nhãn bật; bút dạ quang
- Nhiễu vô tuyến + bíp điện báo khi phát tin và khi nghe điện Nhật; tiếng điện chạy dọc đường cáp
- Nhóm mã nhảy số khi giải mã; cú nhấn trầm khi "AF" xuất hiện (29,24 s và 87,33 s)
- Máy bay lướt qua và tiếng nổ đục ở cảnh "nếu đoán nhầm" và khi Midway bị đánh (90,43 s); đồng hồ tích tắc khi lịch chạy
- Hiệu ứng tự hạ ~7 dB khi đang có lời; cú nhấn mạnh nhất vẫn thấp hơn giọng ~8 dB
- Âm lượng tổng −14,3 LUFS, đỉnh −1,2 dBTP (bản v2 gốc: −14,1 LUFS, đỉnh +1,0 dBTP do MP3 giọng có đỉnh vượt 0 dB)
- `build/sfx_stem.wav`: riêng lớp hiệu ứng, để chỉnh trong CapCut nếu cần

Claude không nghe được âm thanh: mức và mốc được đo bằng số, còn độ hay/dở phải do chủ kênh nghe duyệt.
