"""Nhịp phim Tập 1: Lửa — dựng từ kịch bản (bóng thoại tách ngắn để đọc kịp trên điện thoại).

Mỗi nhịp: (id, thời lượng, cảnh, người nói, loại bóng, chữ, cảm xúc giọng)
loại bóng: say / shout / think / whisper / None ; người nói: bop / gam / None
"""
B = [
    # CẢNH 1 — trước cửa hang, chiều tối
    ("open",      2.6, 1, None,  None,      None, None),
    ("drill",     2.8, 1, "bop", "say",     "Thêm chút nữa… thêm chút nữa…", "calm"),
    ("spark",     2.6, 1, None,  None,      None, None),
    ("warm",      2.4, 1, "bop", "say",     "Được rồi! Ấm quá…", "happy"),
    ("jump",      2.2, 1, "gam", "shout",   "Con gì đây?!", "angry"),
    ("bite",      2.2, 1, "gam", "shout",   "Nó cắn tay mày kìa!", "angry"),
    ("no",        2.0, 1, "bop", "say",     "Không, không! Nó không cắn.", "worried"),
    ("name",      2.0, 1, "bop", "say",     "Cái này gọi là LỬA.", "calm"),
    ("warm2",     1.8, 1, "bop", "say",     "Nó làm mình ấm…", "calm"),
    ("what",      1.6, 1, "gam", "shout",   "Ấm cái gì!", "angry"),
    ("red",       2.6, 1, "gam", "say",     "Nó đỏ, nó nhảy, nó kêu tách tách.", "angry"),
    ("useless",   1.8, 1, "gam", "shout",   "Đồ vô dụng!", "angry"),
    ("stomp",     2.8, 1, None,  None,      None, None),
    ("smoke",     2.6, 1, "gam", "shout",   "Thấy chưa! Nó phun khói vào mặt tao!", "angry"),
    ("danger",    1.6, 1, "gam", "shout",   "Đồ nguy hiểm!", "angry"),
    ("sigh",      2.8, 1, "bop", "think",   "Haizz…", "sad"),
    # CẢNH 2 — đêm, mưa lạnh
    ("cold",      2.8, 2, "gam", "say",     "L-l-lạnh… lạnh quá…", "cold"),
    ("glow",      2.8, 2, None,  None,      None, None),
    ("raise",     2.6, 2, "gam", "say",     "Mày… lại nuôi con vật đỏ đó à?", "grumpy"),
    ("tasty",     2.4, 2, "bop", "say",     "Ừ. Nó làm thịt thơm và mềm hơn.", "happy"),
    ("try",       1.6, 2, "bop", "say",     "Ăn thử không?", "happy"),
    ("nope",      1.6, 2, "gam", "shout",   "Không thèm!", "grumpy"),
    ("growl",     2.4, 2, None,  None,      None, None),
    ("onebite",   2.0, 2, "gam", "whisper", "…Một miếng thôi.", "shy"),
    # CẢNH 3 — nửa đêm
    ("wolves",    2.6, 3, None,  None,      None, None),
    ("wolf",      1.6, 3, "bop", "whisper", "Sói…", "scared"),
    ("letme",     1.4, 3, "gam", "shout",   "Để tao!", "angry"),
    ("hot",       2.4, 3, "gam", "shout",   "Á! NÓNG! NÓNG!", "panic"),
    ("flee",      2.2, 3, None,  None,      None, None),
    ("afraid",    2.2, 3, "gam", "say",     "…Chúng nó sợ.", "wonder"),
    ("fact",      2.2, 3, "bop", "say",     "Đúng rồi. Thú dữ sợ lửa.", "calm"),
    ("invent",    2.6, 3, "gam", "shout",   "Gậy lửa! Tao phát minh ra gậy lửa!", "proud"),
    ("mine",      2.0, 3, "bop", "say",     "Nhưng lửa là của tôi mà…", "worried"),
    ("allmine",   2.8, 3, "gam", "shout",   "Lửa của tao! Gậy của tao! Hang cũng của tao!", "proud"),
    ("hog",       2.2, 3, None,  None,      None, None),
    # CẢNH 4 — sáng hôm sau
    ("stone",     2.4, 4, None,  None,      None, None),
    ("idea",      2.8, 4, "bop", "think",   "Ơ… hay là… gắn cái này lên đầu gậy?", "wonder"),
    ("useless2",  1.8, 4, "gam", "shout",   "Đồ vô dụng!", "angry"),
    ("black",     0.8, 4, None,  None,      None, None),
    ("card",      5.5, 5, None,  None,      None, None),
]

T = {}
_t = 0.0
for row in B:
    T[row[0]] = (_t, _t + row[1], row)
    _t += row[1]
DUR = round(_t, 3)
