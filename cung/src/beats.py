"""Nhịp phim Tập 5: Cung tên. (id, giây, cảnh, người nói, loại bóng, chữ, cảm xúc giọng)"""
B = [
    # CẢNH 1 — bờ suối, buổi sáng
    ("open",      2.8, 1, None,  None,      None, None),
    ("stab",      1.8, 1, None,  None,      None, None),
    ("show",      2.2, 1, "gam", "shout",   "Cá của tao! Đẹp nhất suối!", "proud"),
    ("eagle",     2.4, 1, None,  None,      None, None),
    ("empty",     1.6, 1, None,  None,      None, None),
    ("hey",       1.8, 1, "gam", "shout",   "…Ê! Trả đây!", "angry"),
    ("throwsp",   2.6, 1, None,  None,      None, None),
    ("eat",       2.0, 1, None,  None,      None, None),
    ("unfair",    2.8, 1, "gam", "shout",   "Cây cao quá! Tay tao ngắn quá! Trời bất công!", "angry"),
    # CẢNH 2 — Bộp nhớ lại
    ("think",     2.0, 2, None,  None,      None, None),
    ("heavy1",    2.4, 2, "bop", "say",     "Giáo nặng, lại chỉ có sức tay đẩy đi.", "calm"),
    ("heavy2",    1.8, 2, "bop", "say",     "Nên không bay xa được.", "calm"),
    ("draw",      2.4, 2, None,  None,      None, None),
    ("store1",    2.6, 2, "bop", "say",     "Khi kéo dây, mình uốn cong cái cành.", "calm"),
    ("store2",    2.8, 2, "bop", "say",     "Cành bị uốn sẽ giữ lại sức mình vừa kéo. Buông tay ra…", "calm"),
    ("release",   1.4, 2, None,  None,      None, None),
    ("push1",     2.8, 2, "bop", "say",     "…cành duỗi thẳng ra, đẩy hết sức đó vào một que gỗ nhỏ.", "calm"),
    ("push2",     2.4, 2, "bop", "say",     "Que nhẹ, nên bay rất nhanh và rất xa.", "happy"),
    ("whittle",   2.4, 2, None,  None,      None, None),
    ("light",     2.8, 2, "bop", "say",     "Mũi tên phải nhỏ, phải nhẹ. Nặng quá là không bay nổi.", "calm"),
    # CẢNH 3 — Gầm phát hiện
    ("hunch",     2.2, 3, "gam", "shout",   "Cái gì đây? Cái cành bị gù à?", "smug"),
    ("bow",       2.6, 3, "bop", "say",     "Cái cung. Với mũi tên. Đứng xa vẫn bắn tới được.", "calm"),
    ("far",       1.6, 3, "gam", "shout",   "Xa? Đưa đây!", "smug"),
    ("fiddle",    2.4, 3, None,  None,      None, None),
    ("scratch",   2.6, 3, "gam", "say",     "Ơ… sướng… Gãi lưng! Cái này để gãi lưng!", "happy"),
    ("twangs",    2.0, 3, None,  None,      None, None),
    ("notfor",    1.8, 3, "bop", "shout",   "Không phải để gãi lưng!", "panic"),
    ("useA",      2.6, 3, "gam", "shout",   "Gãi lưng thì tốt. Còn bắn thì vô dụng!", "smug"),
    ("useB",      2.4, 3, "gam", "shout",   "Que thì làm sao bay được? Đồ vô dụng!", "angry"),
    ("snap",      2.4, 3, None,  None,      None, None),
    ("lost",      2.6, 3, "bop", "say",     "…Tôi vót cả buổi đấy.", "sad"),
    # CẢNH 4 — chiều, đại bàng quay lại
    ("bigfish",   2.2, 4, None,  None,      None, None),
    ("nobody",    2.2, 4, "gam", "say",     "Lần này không ai lấy được.", "smug"),
    ("grab",      2.4, 4, None,  None,      None, None),
    ("hair",      1.8, 4, "gam", "shout",   "TÓC CỦA TAO!", "panic"),
    ("miss",      2.8, 4, None,  None,      None, None),
    ("stick",     1.8, 4, "gam", "say",     "…Que đâu?", "shy"),
    ("quick",     2.0, 4, None,  None,      None, None),
    ("shoot1",    2.8, 4, None,  None,      None, None),
    ("drunk",     1.8, 4, "gam", "shout",   "Que này say rượu!", "angry"),
    ("wait",      1.4, 4, "bop", "shout",   "Đợi đã!", "panic"),
    ("feather",   2.6, 4, None,  None,      None, None),
    ("fletch1",   2.8, 4, "bop", "say",     "Lông ở đuôi giữ cho tên bay thẳng, không lật lung tung.", "calm"),
    ("fletch2",   1.8, 4, "bop", "say",     "Giống như đuôi chim vậy.", "happy"),
    ("aim",       2.4, 4, None,  None,      None, None),
    ("shoot2",    2.4, 4, None,  None,      None, None),
    ("fall",      2.2, 4, None,  None,      None, None),
    ("won",       2.2, 4, "gam", "whisper", "…Tao thắng.", "proud"),
    # CẢNH 5 — hoàng hôn, trước hang
    ("king",      2.2, 5, None,  None,      None, None),
    ("inv",       2.6, 5, "gam", "shout",   "Cành bắn xa! Tao phát minh ra cành bắn xa!", "proud"),
    ("mine",      2.0, 5, "bop", "say",     "Cung tên. Của tôi.", "sad"),
    ("allmine",   2.8, 5, "gam", "shout",   "Cung của tao! Tên của tao! Đại bàng cũng của tao!", "proud"),
    ("keek",      1.8, 5, None,  None,      None, None),
    ("trophy",    2.6, 5, None,  None,      None, None),
    # CẢNH 6 — đêm mưa, sáng hôm sau
    ("rain",      2.8, 6, None,  None,      None, None),
    ("morning",   2.4, 6, None,  None,      None, None),
    ("idea",      2.0, 6, "bop", "think",   "Ơ… hay là…", None),
    ("useless2",  1.8, 6, "gam", "shout",   "Đồ vô dụng!", "sleepy"),
    ("black",     0.8, 6, None,  None,      None, None),
    ("card",      7.5, 7, None,  None,      None, None),
]

T = {}
_t = 0.0
for row in B:
    T[row[0]] = (_t, _t + row[1], row)
    _t += row[1]
DUR = round(_t, 3)
