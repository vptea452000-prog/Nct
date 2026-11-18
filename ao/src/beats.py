"""Nhịp phim Tập 3: Kim khâu và áo da. (id, giây, cảnh, người nói, loại bóng, chữ, cảm xúc giọng)"""
B = [
    # CẢNH 1 — cửa hang, sáng sớm, gió rét
    ("open",      2.8, 1, None,  None,      None, None),
    ("inside",    1.6, 1, None,  None,      None, None),
    ("warm1",     2.6, 1, "gam", "say",     "Thấy chưa? Tao ấm. Mày lạnh.", "smug"),
    ("warm2",     1.8, 1, "gam", "shout",   "Vì tao giỏi.", "proud"),
    ("gust",      2.8, 1, None,  None,      None, None),
    ("naked",     1.6, 1, None,  None,      None, None),
    ("better",    2.8, 1, "gam", "say",     "…Gió hôm nay hơi giỏi hơn tao.", "cold"),
    # CẢNH 2 — Bộp làm kim
    ("grind",     2.4, 2, None,  None,      None, None),
    ("sharp1",    2.4, 2, "bop", "say",     "Xương cứng, mài được rất nhọn.", "calm"),
    ("sharp2",    2.2, 2, "bop", "say",     "Nhưng chỉ nhọn thôi chưa đủ…", "calm"),
    ("drill",     1.8, 2, None,  None,      None, None),
    ("hole",      2.2, 2, "bop", "say",     "…phải có cái lỗ để xỏ sợi.", "calm"),
    ("thread",    2.2, 2, None,  None,      None, None),
    ("stitch",    2.6, 2, None,  None,      None, None),
    ("lead1",     2.4, 2, "bop", "say",     "Kim đi trước, sợi chạy theo sau.", "happy"),
    ("lead2",     3.0, 2, "bop", "say",     "Không cần chọc lỗ rồi mới luồn từng chút như trước nữa.", "calm"),
    # CẢNH 3 — chiếc áo đầu tiên
    ("montage",   3.2, 3, None,  None,      None, None),
    ("wear",      1.6, 3, None,  None,      None, None),
    ("nofly",     2.4, 3, None,  None,      None, None),
    ("fit1",      2.6, 3, "bop", "say",     "Áo ôm sát người thì giữ được lớp hơi ấm bên trong,", "calm"),
    ("fit2",      2.0, 3, "bop", "say",     "gió không lùa vào được.", "calm"),
    ("sack",      2.6, 3, "gam", "shout",   "Cái gì đây? Mày chui vào bao tải à?", "smug"),
    ("sleeve1",   2.0, 3, "bop", "say",     "Đây là áo. Có tay áo nữa.", "calm"),
    ("sleeve2",   2.0, 3, "bop", "say",     "Anh giơ tay lên vẫn ấm.", "happy"),
    ("fight",     2.6, 3, "gam", "shout",   "Tao không cần tay áo! Tay tao để đánh nhau!", "angry"),
    ("grab",      2.0, 3, "gam", "say",     "Còn cái que này…", "smug"),
    ("broken",    2.4, 3, "gam", "shout",   "…Cái que có lỗ thủng! Đồ hỏng!", "angry"),
    ("useless",   1.6, 3, "gam", "shout",   "Đồ vô dụng!", "angry"),
    ("flick",     2.0, 3, None,  None,      None, None),
    ("long",      2.6, 3, "bop", "say",     "…Tôi mài cả buổi đấy.", "sad"),
    # CẢNH 4 — đêm, bão tuyết
    ("storm",     2.6, 4, None,  None,      None, None),
    ("slip",      2.2, 4, None,  None,      None, None),
    ("stay",      2.6, 4, "gam", "shout",   "Đứng yên! Tao ra lệnh cho mày đứng yên!", "angry"),
    ("burn",      2.6, 4, None,  None,      None, None),
    ("snore",     2.0, 4, None,  None,      None, None),
    ("sneak",     2.2, 4, None,  None,      None, None),
    ("stuck",     2.8, 4, None,  None,      None, None),
    ("wake",      1.8, 4, "bop", "shout",   "Anh làm gì vậy?!", "panic"),
    ("check",     3.0, 4, "gam", "whisper", "Tao… đang kiểm tra áo của mày có an toàn không.", "shy"),
    # CẢNH 5 — Gầm tự khâu
    ("find",      2.0, 5, None,  None,      None, None),
    ("sew",       2.6, 5, None,  None,      None, None),
    ("done",      1.8, 5, "gam", "shout",   "Xong! Áo của tao!", "proud"),
    ("tail",      3.0, 5, None,  None,      None, None),
    ("fix",       2.8, 5, None,  None,      None, None),
    ("snow",      2.2, 5, None,  None,      None, None),
    ("sack2",     2.6, 5, "gam", "shout",   "Ấm! ẤM! Tao phát minh ra cái bao tải ấm!", "proud"),
    ("mine",      2.2, 5, "bop", "say",     "Áo. Và kim là của tôi.", "sad"),
    ("allmine",   2.8, 5, "gam", "shout",   "Áo của tao! Kim của tao! Tuyết cũng của tao!", "proud"),
    ("trophy",    2.4, 5, None,  None,      None, None),
    # CẢNH 6 — mấy ngày sau
    ("itch",      2.4, 6, None,  None,      None, None),
    ("bite",      1.8, 6, "gam", "shout",   "Bộp! Cái áo cắn tao!", "panic"),
    ("lice1",     2.2, 6, "bop", "say",     "Không phải áo. Chấy đấy.", "calm"),
    ("lice2",     2.4, 6, "bop", "say",     "Trước giờ chấy chỉ sống trên tóc.", "calm"),
    ("lice3",     2.6, 6, "bop", "say",     "Giờ có áo, chúng có thêm chỗ ở mới.", "calm"),
    ("home",      2.6, 6, "gam", "shout",   "Áo của tao! Không phải nhà của chúng mày!", "angry"),
    ("snap",      2.0, 6, None,  None,      None, None),
    ("twist",     2.0, 6, None,  None,      None, None),
    ("idea",      2.4, 6, "bop", "think",   "Ơ… hay là… bện nhiều sợi lại?", None),
    ("useless2",  1.8, 6, "gam", "shout",   "Đồ vô dụng!", "angry"),
    ("black",     0.8, 6, None,  None,      None, None),
    ("card",      7.5, 7, None,  None,      None, None),
]

T = {}
_t = 0.0
for row in B:
    T[row[0]] = (_t, _t + row[1], row)
    _t += row[1]
DUR = round(_t, 3)
