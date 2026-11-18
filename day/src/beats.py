"""Nhịp phim Tập 4: Dây thừng. (id, giây, cảnh, người nói, loại bóng, chữ, cảm xúc giọng)"""
B = [
    # CẢNH 1 — bìa rừng, buổi sáng
    ("open",      2.8, 1, None,  None,      None, None),
    ("drop",      3.0, 1, None,  None,      None, None),
    ("sigh",      2.6, 1, "bop", "say",     "Giá mà có thứ gì giữ chúng lại với nhau…", "sad"),
    ("pass",      2.0, 1, None,  None,      None, None),
    ("weak",      2.0, 1, "gam", "shout",   "Yếu thế! Nhìn tao này!", "proud"),
    ("double",    2.6, 1, None,  None,      None, None),
    ("slippery",  2.4, 1, "gam", "say",     "…Củi hôm nay trơn.", "grumpy"),
    # CẢNH 2 — Bộp làm dây
    ("bark",      2.4, 2, None,  None,      None, None),
    ("bark1",     2.0, 2, "bop", "say",     "Lớp vỏ ngoài thì giòn.", "calm"),
    ("bark2",     2.6, 2, "bop", "say",     "Lớp vỏ trong mới có sợi dài và dai.", "calm"),
    ("one",       1.8, 2, None,  None,      None, None),
    ("weak1",     2.0, 2, "bop", "say",     "Một sợi thì yếu…", "sad"),
    ("twist1",    2.6, 2, None,  None,      None, None),
    ("twist2",    2.6, 2, None,  None,      None, None),
    ("twist3",    3.2, 2, "bop", "say",     "Mỗi bó xoắn một chiều, ba bó bện lại theo chiều ngược lại.", "calm"),
    ("grip",      2.4, 2, "bop", "say",     "Chúng siết lấy nhau, không bung ra được.", "calm"),
    ("pull",      2.0, 2, None,  None,      None, None),
    ("share1",    2.4, 2, "bop", "say",     "Nhiều sợi cùng chịu sức kéo.", "calm"),
    ("share2",    2.6, 2, "bop", "say",     "Lại còn bám chặt vào nhau. Nên khỏe hơn nhiều.", "happy"),
    ("tie",       2.6, 2, None,  None,      None, None),
    # CẢNH 3 — Gầm phát hiện
    ("worm",      2.2, 3, "gam", "shout",   "Con gì đây? Con giun khô à?", "smug"),
    ("rope",      2.6, 3, "bop", "say",     "Dây thừng. Để buộc, để kéo, để treo đồ…", "calm"),
    ("stomp",     2.2, 3, "gam", "shout",   "Giun thì để giẫm! Đưa đây!", "angry"),
    ("tug",       2.6, 3, None,  None,      None, None),
    ("wrap",      3.0, 3, None,  None,      None, None),
    ("cocoon",    2.0, 3, None,  None,      None, None),
    ("kidnap",    2.6, 3, "gam", "say",     "…Con giun này bắt cóc tao.", "worried"),
    ("free",      1.6, 3, None,  None,      None, None),
    ("throw",     1.8, 3, None,  None,      None, None),
    ("useless",   1.6, 3, "gam", "shout",   "Đồ vô dụng!", "angry"),
    ("fall",      2.0, 3, None,  None,      None, None),
    ("lost",      2.6, 3, "bop", "say",     "…Tôi bện cả buổi đấy.", "sad"),
    # CẢNH 4 — chiều, khe núi
    ("rabbit",    2.0, 4, None,  None,      None, None),
    ("dinner",    2.0, 4, "gam", "shout",   "Bữa tối! Đứng lại!", "happy"),
    ("leap",      1.6, 4, None,  None,      None, None),
    ("air",       2.2, 4, None,  None,      None, None),
    ("aaa",       1.8, 4, "gam", "shout",   "Áááá!", "panic"),
    ("ledge",     2.2, 4, None,  None,      None, None),
    ("help",      2.0, 4, "gam", "shout",   "BỘP! Cứu tao!", "panic"),
    ("look",      2.6, 4, "bop", "say",     "Anh có thấy cái gì quanh đó không?", "calm"),
    ("spot",      2.0, 4, None,  None,      None, None),
    ("worm2",     1.8, 4, "gam", "whisper", "…Con giun.", "shy"),
    ("toss",      2.0, 4, "bop", "shout",   "Ném một đầu lên đây!", "calm"),
    ("miss",      3.4, 4, None,  None,      None, None),
    ("anchor",    2.4, 4, None,  None,      None, None),
    ("fric",      3.0, 4, "bop", "say",     "Dây quấn quanh gốc cây thì bám chặt, không trượt.", "calm"),
    ("climb1",    2.2, 4, "bop", "shout",   "Giờ anh bám vào mà leo lên!", "happy"),
    ("climb",     2.4, 4, None,  None,      None, None),
    ("itchy",     1.8, 4, None,  None,      None, None),
    ("dont",      1.6, 4, "bop", "shout",   "ĐỪNG GÃI!", "panic"),
    ("grit",      2.6, 4, None,  None,      None, None),
    # CẢNH 5 — hoàng hôn, trước hang
    ("coil",      2.0, 5, None,  None,      None, None),
    ("lifeline",  2.6, 5, "gam", "shout",   "Dây cứu mạng! Tao phát minh ra dây cứu mạng!", "proud"),
    ("mine",      2.0, 5, "bop", "say",     "Dây thừng. Của tôi.", "sad"),
    ("allmine",   2.8, 5, "gam", "shout",   "Dây của tao! Cây của tao! Vực cũng của tao!", "proud"),
    ("tieall",    3.0, 5, None,  None,      None, None),
    ("tiebop",    1.8, 5, None,  None,      None, None),
    ("hey",       1.4, 5, "bop", "shout",   "Này!", "angry"),
    ("keep",      2.8, 5, "gam", "say",     "Buộc lại cho khỏi mất. Mày cũng là của tao.", "smug"),
    ("trophy",    2.4, 5, None,  None,      None, None),
    # CẢNH 6 — đêm
    ("bend",      2.6, 6, None,  None,      None, None),
    ("twang",     2.2, 6, None,  None,      None, None),
    ("idea",      2.0, 6, "bop", "think",   "Ơ… hay là…", None),
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
