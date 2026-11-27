# Neanderthal v1 — ghi chú bàn giao

**Tập:** Vì sao trong người bạn có ADN của một loài người đã tuyệt chủng? (chuỗi fact nguyên thủy)
**Phiên bản:** v1 · Shorts 1080 × 1920, 30 fps · dài 1:25,2 · hoạt hình thuần, linh vật dẫn chuyện, có hiệu ứng tiếng

| File | Nội dung |
|---|---|
| `build/Neanderthal_v1.mp4` | Bản đầy đủ, phụ đề in cứng, giọng + 151 hiệu ứng; −14,2 LUFS, đỉnh −1,2 dBTP |
| `build/Neanderthal_v1.srt` | Phụ đề riêng |
| `build/sfx_stem.wav` | Riêng lớp hiệu ứng |
| `src/prehist.py` | Nhân vật tiền sử mới (Neanderthal, người hiện đại thời tiền sử), chuỗi ADN, xương, mảnh ghép |

Xuất lại: `python3 src/align.py && python3 src/render.py full && mv build/Neanderthal_v1.mp4 build/Neanderthal_v1_nosfx.mp4 && python3 src/sfx_events.py`

## Việc cần chủ kênh quyết trước khi đăng

Lời thu giữ nguyên hai câu đã đánh dấu khi đối chiếu (xem `DOI_CHIEU.md`). Phụ đề ghi đúng lời đọc; chữ trên hình viết trung tính.

1. **8,6–10,6 s — "Họ không phải tổ tiên trực tiếp của chúng ta"**: mâu thuẫn với nội dung tập (vì có con chung, một số người Neanderthal là tổ tiên của người ngoài châu Phi). Trên hình chỉ ghi "HAI NHÁNH NGƯỜI". Đề xuất thu lại: *"Họ không phải tổ tiên chính của chúng ta, mà là một nhánh người khác."*
2. **72,8–76,9 s — "người mang hai bản của một biến thể gen…"**: chi tiết "hai bản" chưa xác nhận được. Trên hình ghi "biến thể gen Neanderthal · liên quan: dễ cháy nắng khi còn nhỏ". Đề xuất thu lại: *"…một số biến thể gen Neanderthal có liên quan tới việc dễ bị cháy nắng khi còn nhỏ."*

Thu lại hai câu này thì gửi MP3 mới; Claude căn lại mốc và xuất lại.

## Bảng dựng

| Mốc | Lời | Hình |
|---|---|---|
| 0–4,8 | "ADN của một loài người đã tuyệt chủng" | Chuỗi ADN xoay, vài thanh đổi màu cam, linh vật hoảng |
| 4,8–6,0 | "người Neanderthal" | Người Neanderthal bật lên, chữ bật từng ký tự |
| 6,0–8,6 | "châu Âu và nhiều vùng châu Á" | Bản đồ, vùng phân bố tô cam (gần đúng) |
| 8,6–12,0 | "một nhánh người khác" | Cây hai nhánh: người hiện đại (xanh) / Neanderthal (cam) |
| 12,0–15,7 | "rời châu Phi… gặp nhau… con chung" | Mũi tên rời châu Phi; hai người gặp nhau thời băng hà, trái tim |
| 15,7–21,3 | "đứa trẻ… hàng nghìn thế hệ" | Đứa trẻ có đốm sáng cam; dòng người, bộ đếm thế hệ (minh họa) |
| 21,3–26,8 | "giải mã ADN… so sánh" | Phòng thí nghiệm: xương → ADN; hai chuỗi ADN đặt cạnh nhau |
| 26,8–35,0 | "1,5–2%… cao hơn một chút" | Lưới 100 ô, ô cam tăng dần |
| 35,0–40,9 | "Đông Á cao hơn châu Âu" | Hai cột đo; linh vật thắc mắc |
| 40,9–46,7 | "người châu Phi… 0,3%" | Bản đồ châu Phi: "0%" bị đóng dấu "từng được cho là" → "~0,3%" |
| 46,7–57,0 | "1%… mỗi người giữ mảnh khác nhau… 1/5 bộ gen" | Mảnh ghép cam từ nhiều người bay về, lấp 1/5 khung |
| 57,0–65,9 | "không nằm im… da và tóc… thích nghi" | ADN uốn lượn; biểu tượng da, tóc; tổ tiên trong tuyết (nhãn "giả thuyết") |
| 65,9–69,9 | "tiểu đường, bệnh Crohn" | Giọt máu, ruột |
| 69,9–77,3 | "112.000 người Anh… cháy nắng" | Bộ đếm người; linh vật đỏ ửng dưới nắng (minh họa) |
| 77,3–80,3 | "biến mất… không chữ viết" | Người Neanderthal đi vào sương mù |
| 80,3–85,2 | "vẫn còn trong tế bào hàng tỉ người" | Phóng từ tế bào ra hàng loạt tế bào có đốm cam |
