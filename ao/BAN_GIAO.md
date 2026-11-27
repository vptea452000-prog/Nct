# Tập 3: Kim khâu và áo da — ghi chú bàn giao

**Chuỗi:** Bộp và Gầm (fact nguyên thủy) · phim hoạt hình hài không lời
**Phiên bản:** v1 · Shorts 1080 × 1920, 30 fps · dài 2:25,5 · 61 nhịp
**Bộ khung nhân vật:** v2 (`tools/rig.py`) — tập đầu tiên dựng toàn bộ bằng bộ khung mới

| File | Nội dung |
|---|---|
| `build/Ao_v1.mp4` | Bản đầy đủ: hình + giọng ú ớ chuẩn + hiệu ứng |
| `src/beats.py` | Nhịp phim (thoại, loại bóng, cảm xúc giọng) — sửa ở đây |
| `src/scenes.py` | Cảnh; đạo cụ mới: kim xương, tấm da bay, áo khâu, cây mùa đông, tuyết, con chấy dễ thương, khe đá, sợi gân |
| `src/sfx_events.py` | Giọng ú ớ (`tools/babble.py`) + hiệu ứng |

Xuất lại: `python3 src/render.py full && python3 src/sfx_events.py`

## Bổ sung vào bộ khung v2 trong tập này

Trang phục `outfit`: `bare` (cởi trần, đóng khố), `coat` (áo khâu ôm sát có tay áo, đường khâu, cổ lông), `bigcoat` (áo cỡ Gầm); tấm da khoác `cape` (bay phần phật `cape_flap`, tuột `cape_drop`, thủng `cape_hole`); `shiver` (run lẩy bẩy); miệng `chatter` (răng va cầm cập); `prop_r/prop_l` (cầm đồ vật nhỏ như cây kim).

## Đối chiếu khoa học

- Kim xương chim ở hang Denisova: ~50.000 năm, dài ~7 cm, có lỗ — khớp ghi chú kịch bản; thẻ fact **không** ghi "cổ nhất".
- Chấy quần áo tách khỏi chấy đầu ít nhất ~83.000, có thể ~170.000 năm trước (Toups, Reed và cộng sự, 2011) — đúng câu trên thẻ fact.
- Áo ôm sát giữ lớp không khí ấm, chặn gió lùa: minh họa bằng sơ đồ hai hình người (khoác hờ ✗ / ôm sát ✓).

## Đã làm theo gợi ý dựng

- **Các nhịp cười chính:** tấm da bay lên ngọn cây (VÙ! → PHẦN PHẬT, da mắc trên cây suốt cảnh sau); Gầm ra lệnh cho tấm da "đứng yên" (da tuột lần nữa giữa câu); hai người kẹt trong một chiếc áo (KẸT!, tay Gầm thò ra ống tay); áo khâu dính vào tấm da kéo lê như cái đuôi (SỘT… SỘT…, Bộp nhịn cười "PHÌ…"); "Cái áo cắn tao!".
- **Thêm:** mặt Bộp dài ra thật (đầu kéo dài + đám mây mưa nhỏ) ở câu "Tôi mài cả buổi đấy"; tấm da cháy thủng một lỗ to; nước mũi Gầm đóng băng.
- **Màn khâu:** tua nhanh ▶▶ x4 "ĐO · CẮT · KHÂU SƯỜN · TAY ÁO" với tiếng "phập" theo nhịp.
- **Chấy:** vẽ dễ thương (mắt to, má hồng, cười, vẫy tay, khuân đồ dọn vào "NHÀ MỚI").
- **Chiến lợi phẩm của Gầm:** cuối cảnh 5 hiện "LỬA · GIÁO · ÁO", áo thủng treo trên cây giáo.
- **Cài tập sau (Dây thừng):** sợi gân đơn đứt PHỰT, hai sợi xoắn lại "KHÔNG ĐỨT!", bong bóng suy nghĩ hình sợi thừng bện.
- **Âm thanh:** giọng ú ớ chuẩn của kênh; câu thì thầm "Tao… đang kiểm tra áo…" làm nghẹt (lọc thấp); không có chuỗi tiếng gõ dưới lời thoại.
