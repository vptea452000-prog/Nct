"""Nhịp phim Tập 2: Cây giáo. (id, giây, cảnh, người nói, loại bóng, chữ, cảm xúc giọng)"""
B = [
    # CẢNH 1 — bờ suối, buổi sáng
    ("open",      2.4, 1, None,  None,      None, None),
    ("lunch",     2.6, 1, "gam", "whisper", "Bữa trưa… của… tao…", "smug"),
    ("charge",    1.4, 1, None,  None,      None, None),
    ("bounce",    1.8, 1, "gam", "shout",   "Ối!", "panic"),
    ("turn",      1.8, 1, None,  None,      None, None),
    ("talk",      2.6, 1, "gam", "say",     "…Ơ. Mình nói chuyện tử tế được không?", "worried"),
    ("chase",     3.4, 1, None,  None,      None, None),
    ("skin",      2.0, 1, "bop", "say",     "Da lợn rừng dày lắm.", "calm"),
    ("skin2",     2.4, 1, "bop", "say",     "Đập thì nó chỉ đau, chứ không thủng.", "calm"),
    ("climb",     2.6, 1, "gam", "shout",   "Tao biết! Tao… đang tập leo cây.", "proud"),
    # CẢNH 2 — cửa hang, buổi trưa
    ("hug",       2.6, 2, "gam", "whisper", "Lửa của tao…", "sleepy"),
    ("knap",      1.6, 2, None,  None,      None, None),
    ("ouch",      1.8, 2, "bop", "shout",   "Á! Sắc thật.", "panic"),
    ("haft",      3.2, 2, None,  None,      None, None),
    ("glue",      2.8, 2, "bop", "say",     "Nhựa cây để dính. Gân thú khô lại sẽ co, siết chặt hơn.", "calm"),
    ("done",      2.0, 2, "bop", "shout",   "Xong rồi!", "happy"),
    # CẢNH 3 — Gầm phát hiện
    ("peek",      1.3, 3, None,  None,      None, None),
    ("tooth",     2.0, 3, "gam", "say",     "Cái gì đây? Que xỉa răng à?", "smug"),
    ("ex1",       2.4, 3, "bop", "say",     "Cây giáo. Gậy của anh to nhưng đầu tròn…", "calm"),
    ("ex2",       2.0, 3, "bop", "say",     "…lực đập tỏa ra khắp nơi.", "calm"),
    ("ex3",       2.8, 3, "bop", "say",     "Mũi giáo nhỏ và nhọn: cả sức mạnh dồn vào một điểm.", "calm"),
    ("huh",       2.0, 3, "gam", "think",   "Dồn… vào… điểm?", None),
    ("finger",    2.2, 3, "bop", "say",     "Anh lấy ngón tay ấn vào tay tôi xem.", "calm"),
    ("press1",    1.8, 3, None,  None,      None, None),
    ("thorn",     2.0, 3, "bop", "say",     "Giờ lấy cái gai này, ấn nhẹ thôi.", "calm"),
    ("press2",    1.8, 3, None,  None,      None, None),
    ("same",      2.8, 3, "bop", "say",     "Đó! Cùng một sức, nhưng cái gai nhỏ hơn nên đâm vào được.", "happy"),
    ("strong",    2.4, 3, "gam", "shout",   "Tao không cần dồn điểm gì hết. Tao có sức!", "proud"),
    ("useless",   1.6, 3, "gam", "shout",   "Đồ vô dụng!", "angry"),
    ("snap",      2.2, 3, None,  None,      None, None),
    ("lost",      2.6, 3, "bop", "say",     "…Tôi mất cả buổi sáng đấy.", "sad"),
    # CẢNH 4 — chiều, lợn rừng quay lại
    ("snort",     2.6, 4, None,  None,      None, None),
    ("brother",   2.2, 4, "gam", "shout",   "Nó… đi gọi anh nó tới?!", "panic"),
    ("bonk2",     1.6, 4, None,  None,      None, None),
    ("help",      2.4, 4, "gam", "shout",   "BỘP! Cứu! Cái que xỉa răng đâu rồi?!", "panic"),
    ("rebuild",   2.6, 4, None,  None,      None, None),
    ("catch",     1.4, 4, "bop", "shout",   "Đỡ này!", "angry"),
    ("aim",       1.6, 4, None,  None,      None, None),
    ("brake",     2.6, 4, None,  None,      None, None),
    ("flee",      1.8, 4, None,  None,      None, None),
    ("win",       1.8, 4, "gam", "whisper", "…Tao thắng?", "wonder"),
    ("reach1",    2.4, 4, "bop", "say",     "Giáo dài, nên anh đứng xa mà vẫn với tới nó.", "calm"),
    ("reach2",    2.4, 4, "bop", "say",     "Nó chưa tới được anh thì đã gặp mũi nhọn rồi.", "calm"),
    # CẢNH 5 — hoàng hôn, bờ suối
    ("fish",      2.6, 5, None,  None,      None, None),
    ("fishstick", 2.4, 5, "gam", "shout",   "Hahaha! Gậy cá! Tao phát minh ra gậy cá!", "proud"),
    ("mine",      2.0, 5, "bop", "say",     "Đó là cây giáo. Của tôi.", "sad"),
    ("allmine",   2.8, 5, "gam", "shout",   "Giáo của tao! Cá của tao! Suối cũng của tao!", "proud"),
    ("sing",      2.6, 5, "gam", "say",     "♪ La la laaa ♪", "sing"),
    # CẢNH 6 — đêm
    ("chilly",    2.8, 6, None,  None,      None, None),
    ("idea",      2.2, 6, "bop", "think",   "Ơ… hay là…", None),
    ("useless2",  1.8, 6, "gam", "shout",   "Đồ vô dụng!", "angry"),
    ("black",     0.8, 6, None,  None,      None, None),
    ("card",      6.5, 7, None,  None,      None, None),
]

T = {}
_t = 0.0
for row in B:
    T[row[0]] = (_t, _t + row[1], row)
    _t += row[1]
DUR = round(_t, 3)
