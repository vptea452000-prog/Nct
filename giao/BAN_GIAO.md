# Tập 2: Cây giáo — ghi chú bàn giao

**Chuỗi:** Bộp và Gầm (fact nguyên thủy) · phim hoạt hình hài không lời
**Phiên bản:** v1 · Shorts 1080 × 1920, 30 fps · dài 2:00,8 · 53 nhịp

| File | Nội dung |
|---|---|
| `build/Giao_v1.mp4` | Bản đầy đủ: hình + giọng ú ớ chuẩn của kênh + hiệu ứng; −13,7 LUFS, đỉnh −2,6 dBTP |
| `build/contact_sheet.png` | Dải khung hình |
| `src/beats.py` | Nhịp phim (thoại, loại bóng, cảm xúc giọng) — sửa ở đây |
| `src/kit.py` | Bộ công cụ dùng chung cho chuỗi (bóng thoại, tượng thanh, hang, lửa, nhân vật) |
| `src/scenes.py` | Cảnh; nhân vật/đạo cụ mới: lợn rừng (con anh to, có sẹo), cây, suối, cá, giáo mũi đá, gai, tấm da, con bọ |

Xuất lại: `python3 src/render.py full && python3 src/sfx_events.py`

## Đối chiếu khoa học

Khớp với ghi chú nguồn của kịch bản: Kathu Pan ~500.000 năm (Wilkins và cộng sự 2012); thí nghiệm gắn mũi đá bằng nhựa keo + gân; giáo mũi đá phổ biến sau ~300.000 năm; giáo gỗ Schöningen được tính lại ~200.000 năm (2025); nguyên lý áp lực = lực / diện tích. Thẻ fact cuối phim dùng đúng hai câu kịch bản đề xuất.

## Đã làm theo gợi ý dựng của kịch bản

- **Ba nhịp cười chính có ngừng**: gậy bật vào trán (BỐP! → CỐP! + sao quay quanh đầu), "Nó… đi gọi anh nó tới?!" (máy lia lộ con lợn anh to gấp rưỡi, có sẹo; rồi "…"), lợn phanh gấp trước mũi giáo (KÉÉÉT!, lợn **lé mắt** nhìn mũi đá, "…").
- **Gọi lại tập 1**: Gầm nằm ôm đống lửa ngủ (z z z); đống lửa nằm góc hang ở các cảnh sau; cuối phim nhãn "chiến lợi phẩm: lửa · giáo".
- **Màn "ngón tay và cái gai"**: cận cảnh, chậm; mũi tên lực tỏa rộng (ngón tay, Bộp mặt tỉnh bơ "…") so với dồn vào một điểm (cái gai, Bộp nhảy dựng "ÚI!!!"); tiếp theo là biểu đồ "cùng 1 sức → áp lực" hai cột.
- **Làm vui hơn tập 1**: đường tốc độ khi lao tới, Gầm chạy vòng quanh cây bị lợn đuổi, rung khung ở mỗi cú hài, hai cảnh dựng nhanh "1/5 → 5/5" và "MÒ ĐÁ! NHÉT! TRÉT! QUẤN!", Gầm hát lạc giọng với nốt nhạc nhảy.
- **Âm thanh**: giọng ú ớ dùng `tools/babble.py` (đúng giọng đã chốt), không có chuỗi tiếng gõ dưới lời thoại; thêm boing, cốp, khịt, ụt ịt, phanh gấp, tõm, phập, ngáy.
