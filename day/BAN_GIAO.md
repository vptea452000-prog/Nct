# Tập 4: Dây thừng — ghi chú bàn giao

**Chuỗi:** Bộp và Gầm (fact nguyên thủy) · phim hoạt hình hài không lời
**Phiên bản:** v1 · Shorts 1080 × 1920, 30 fps · dài 2:34,7 · 66 nhịp · bộ khung nhân vật v2

| File | Nội dung |
|---|---|
| `build/Day_v1.mp4` | Bản đầy đủ: hình + giọng ú ớ chuẩn + hiệu ứng |
| `src/beats.py` | Nhịp phim — sửa ở đây |
| `src/common.py` | Bộ công cụ cảnh dùng chung (tách từ Tập 3): camera, bóng thoại tự trỏ vào đầu, nhép miệng, kim, tấm da, tuyết, chấy, hang… |
| `src/scenes.py` | Cảnh; đạo cụ mới: dây thừng có vân xoắn, cuộn dây, bó củi, thân cây lột vỏ, bó sợi xoắn + mũi tên chiều xoắn, kén dây, thỏ, khe núi có mỏm đá, cành cây uốn |
| `src/sfx_events.py` | Giọng ú ớ (`tools/babble.py`) + hiệu ứng |

Xuất lại: `python3 src/render.py full && python3 src/sfx_events.py`

## Đối chiếu khoa học

- Abri du Maras: mẩu dây ~6 mm, ba bó sợi vỏ trong của cây xoắn vào nhau, dính trên dụng cụ đá dài 60 mm, 41.000–52.000 năm (Hardy và cộng sự, 2020) — khớp.
- Hohle Fels: mảnh ngà voi ma mút dài 20,4 cm, bốn lỗ có rãnh xoắn, ~40.000 năm, dùng bện dây (Conard và cộng sự, 2020) — khớp; thẻ ghi "~40.000 năm".
- Màn bện dây: từng bó xoắn ↺ (vân chéo một chiều, mũi tên vàng), ba bó bện ↻ (vân chéo ngược lại, mũi tên xanh), khung tổng kết "1 bó: ↺ / 3 bó: ↻" — đúng mô tả trong nguồn.
- "Nhiều sợi cùng chịu sức kéo" (sơ đồ 1 sợi ✗ / 6 sợi chia lực ✓), "bám chặt vào nhau" và dây quấn gốc cây "bám chặt, không trượt" — vật lý cơ bản, diễn đạt không dùng thuật ngữ.

## Đã làm theo gợi ý dựng

- **Nhịp cười chính:** bó củi rơi từng khúc rồi đổ ào (CỘP… ÀO!); củi đổ trúng chân Gầm (CỐP!, nhảy lò cò, rơm rớm nước mắt); Gầm tự quấn thành cái kén chỉ còn đầu (VÒNG… VÒNG… → "…"); hai chân chạy trên không trước khi rơi (ỰC…); sợi dây nằm ngay cạnh chân trên mỏm đá (được cài từ cảnh dây rơi xuống vực); ném dây hụt, rơi trúng đầu (BỘP!), lần ba Bộp chộp được; "ĐỪNG GÃI!" (Gầm tuột tay vì chấy); Gầm buộc luôn Bộp vào gốc cây.
- **Nối tập:** Gầm mặc áo to, vác cây giáo, chấy vẫn bò quanh; áo thủng treo trên giáo; chiến lợi phẩm "LỬA · GIÁO · ÁO · DÂY".
- **Cài tập sau (Cung tên):** cành cây uốn cong buộc dây, TƯNG! que gỗ bay vút; bong bóng suy nghĩ hiện hình cây cung; "Đồ vô dụng!" vọng ra từ hang tối (chỉ thấy hai mắt).
- **Âm thanh:** giọng ú ớ chuẩn; "…Con giun." nói lí nhí (lọc thấp); không có chuỗi tiếng gõ dưới lời thoại.
