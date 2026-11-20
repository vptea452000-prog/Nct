# Quy trình làm video (định dạng tài liệu – kể chuyện, 16:9)

## 1. Cùng viết kịch bản
- Chủ kênh đưa chủ đề và ý muốn; Claude viết bản nháp → hai bên sửa tới khi chốt.
- Giọng văn: câu đầy đủ, mềm, liền mạch (xem KENH.md); có mốc năm và số liệu khi cần, nhưng kể như một câu chuyện.
- File: `<tap>/KICH_BAN.md` — chỉ một bài đọc liền mạch.

## 2. Claude lập danh sách khung hình và nguồn tư liệu (`<tap>/NGUON.md`)
Mỗi câu hoặc cụm câu = một mã khung hình. Mỗi dòng ghi:

| Mã | Câu kịch bản | Cần gì | Loại | Từ khóa tìm (Anh / Việt) | Nguồn nên tìm | Ghi chú |
|---|---|---|---|---|---|---|
| K01 | "Năm 1942, …" | Ảnh tàu sân bay Yorktown ra khơi | Ảnh | `USS Yorktown CV-5 1942 photo` | Google Hình ảnh, Wikimedia Commons | Chọn bản không hình mờ |
| K02 | … | Bản đồ nền Thái Bình Dương (trống, không chữ) | Bản đồ | `Pacific Ocean blank map svg` | Wikimedia Commons | Claude tự thêm mũi tên, nhãn |
| K03 | … | — | **Tự tạo** | — | — | Chữ, số liệu, dòng thời gian |

**Loại:** Ảnh · Video (đoạn phim tư liệu) · Bản đồ nền · Tranh · **Tự tạo** (Claude làm, chủ kênh không cần tìm).
**Claude tự tạo:** chữ tiêu đề, phụ đề, số liệu, biểu đồ, dòng thời gian, mũi tên/khối quân trên bản đồ, chuyển cảnh, hiệu ứng.

## 3. Chủ kênh tìm và tải tư liệu
- Đặt tên file đúng **mã khung hình**: `K01.jpg`, `K02.svg`, `K05.mp4`… (nhiều lựa chọn: `K01a.jpg`, `K01b.jpg`).
- Gom vào một thư mục, nén thành **một file .zip** rồi gửi (kèm file voice).
- Không tìm được khung nào thì bỏ trống — Claude sẽ thay bằng hình tự tạo hoặc báo lại.

### Mẹo tìm nguồn (chủ kênh tự xử lý bản quyền — tìm nguồn thoải mái)
- Tìm ở bất kỳ đâu: Google Hình ảnh, Wikimedia Commons, các kho lưu trữ (NARA, Library of Congress, IWM…), phim tài liệu, YouTube, Internet Archive, báo chí, sách ảnh.
- Ưu tiên bản **độ phân giải cao, không có hình mờ / logo / chữ chèn** — để hình lên video sạch và lia/zoom không bị vỡ.
- Video: tải đoạn cần dùng là đủ (không cần cả phim); ghi chú thêm mốc giây nếu chỉ dùng một khúc.
- Vẫn nên ghi đường link nguồn vào `nguon.txt` để Claude đối chiếu đúng nội dung (ảnh có đúng người/sự kiện không).

## 4. Thu giọng
- Đọc theo `KICH_BAN.md`, gửi 1 file (hoặc chia theo gợi ý). Nghỉ ~1 giây giữa các đoạn.

## 5. Claude dựng video
- Kiểm tra từng file: đúng nội dung chưa (sai/không chắc → hỏi lại, không đoán), độ phân giải, hình mờ (có thì cắt khung tránh đi).
- Căn câu theo giọng (đếm âm tiết), dựng theo mã khung hình: lia/zoom chậm trên ảnh, bản đồ động có mũi tên và nhãn, chữ và số liệu tự tạo, phụ đề, hiệu ứng tiếng.
- Nhịp máy vừa phải, chỉ nhanh ở cao trào. Xuất 16:9, −14 LUFS.
- Bàn giao: video + bảng ghi công nguồn để dán vào mô tả YouTube.
