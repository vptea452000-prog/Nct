"""Các cảnh theo mốc câu (giây tuyệt đối trong voice)."""
from scenes import *  # noqa

ADULT = 0.95


# ================================================================ A. Quê nhà Ireland (0 – 48,7)
def a_field(c, t):                     # 0–8,5  năm 1912, 20 tuổi · đào khoai từ lúc trời chưa sáng
    q = ease_shot(t, 0, 8.5)
    K = Cam(lerp(1100, 900, q), lerp(520, 560, q), lerp(1.25, 1.1, q), t=t)
    cottage_field(c, K, t, dawn=clamp(t / 6))
    K.layer(c, 1.0)
    dig = math.sin(t * 2.4)
    YOU(c, 1050, GROUND, ADULT, t, face=1, hand_f=(120, lerp(-40, 120, max(0, dig))), hand_b=(80, lerp(-20, 140, max(0, dig))), lean=10 + 8 * dig,
        eyes="dot", mouth="flat")
    sx = 1050 + ADULT * (120 + 26 + 20)
    c.drawLine(sx, GROUND - ADULT * (366 - lerp(-40, 120, max(0, dig))), sx + 40, GROUND + 10, P(INK, stroke=10))
    for k in range(4):
        c.drawOval(skia.Rect.MakeXYWH(1240 + k * 40, GROUND + 20 + (k % 2) * 10, 30, 22), P("#B89A6A"))
    K.end(c)
    if t < 4.0:
        label(c, "Ireland · 1912", W / 2, 160, 70, "#FFFFFF", a=255 * clamp(t / 0.5) * clamp((4.0 - t) / 0.5))


def a_hearth(c, t):                    # 8,5–14  tối quây quần bên bếp lửa than bùn
    q = ease_shot(t, 8.5, 14.0)
    K = Cam(960, lerp(600, 580, q), lerp(1.3, 1.45, q), t=t)
    cottage_in(c, K, t)
    K.layer(c, 1.0)
    ST(c, "ir_mom", 700, GROUND, ADULT, t, face=1, sit=1.0, hand_f=(80, 100), eyes="dot", look=(1, 0.3), mouth="smile", shawl="#6A5A6A")
    NORA(c, 1220, GROUND, 0.85, t, face=-1, sit=1.0, hand_f=(70, 90), eyes="happy", mouth="smile")
    YOU(c, 1420, GROUND, ADULT, t, face=-1, sit=1.0, hand_f=(90, 60), eyes="dot", look=(-1, 0.4), mouth="smile", cap="")
    K.end(c)


def a_letters(c, t):                   # 14–19,75  chẳng có gì nhiều, ngoài những lá thư từ người đi xa
    q = ease_shot(t, 14.0, 19.75)
    K = Cam(lerp(1360, 1420, q), lerp(470, 440, q), lerp(1.7, 1.9, q), t=t)
    cottage_in(c, K, t, fire=0.6)
    K.layer(c, 1.0)
    YOU(c, 1380, GROUND, ADULT, t, face=1, hand_f=(80, -60), hand_b=(60, -40), eyes="dot", look=(0.4, 0.8), mouth="flat", cap="")
    letter(c, 1380 + ADULT * 120, GROUND - ADULT * 420, 0.55, rot=-8)
    K.end(c)


def a_america(c, t):                   # 19,75–27,7  kể về nước Mỹ · chịu khó làm việc thì ai cũng đổi đời
    lt = t - 19.75
    q = ease_shot(t, 19.75, 27.68)
    grad(c, skia.Rect.MakeWH(W, H), lerp_col("#C8D8E8", "#F2D2A8", q), "#FBF2E2")
    sea = P("#8AB0C8"); c.drawRect(skia.Rect.MakeXYWH(0, 760, W, 400), sea)
    skyline(c, 1220, 760, lerp(0.9, 1.05, q), a=255 * clamp(lt / 1.2))
    liberty(c, 560, 780, lerp(0.95, 1.08, q), a=255 * clamp(lt / 0.8))
    if lt > 0.4:
        label(c, "NƯỚC MỸ", W / 2, 180, int(96 * back_out(clamp((lt - 0.4) / 0.4))), "#FFFFFF")
    for k in range(3):   # khung giấy thư mờ quanh
        letter(c, 160 + k * 800, 980 - (k % 2) * 40, 0.5, rot=-10 + k * 8, a=120)


def a_tickets(c, t):                   # 27,7–37,5  dành dụm từng đồng, mua hai tấm vé: cho bạn và em gái Nora
    lt = t - 27.68
    q = ease_shot(t, 27.68, 37.53)
    K = Cam(lerp(960, 1000, q), lerp(560, 520, q), lerp(1.4, 1.6, q), t=t)
    cottage_in(c, K, t, fire=0.8)
    K.layer(c, 1.0)
    fo(c, rect(700, 700, 560, 40), "#6A4A30", ow=6)
    c.drawLine(740, 740, 740, GROUND, P(INK, stroke=10)); c.drawLine(1220, 740, 1220, GROUND, P(INK, stroke=10))
    ST(c, "ir_mom", 640, GROUND, ADULT, t, face=1, hand_f=(140, 20), eyes="dot", look=(1, 0.8), mouth="flat", shawl="#6A5A6A")
    for k in range(min(9, int(lt * 2.2))):
        c.drawOval(skia.Rect.MakeXYWH(820 + (k % 5) * 34, 680 - (k // 5) * 12, 30, 14), P("#C8A040"))
    if lt > 4.4:
        p = back_out(clamp((lt - 4.4) / 0.5))
        c.save(); c.translate(1000, 650); c.scale(p, p)
        ticket(c, -60, 0, 0.42, rot=-8); ticket(c, 60, 10, 0.42, rot=6)
        c.restore()
    YOU(c, 1360, GROUND, ADULT, t, face=-1, hand_f=(90, 30), eyes="wide" if lt > 4.4 else "dot", look=(-1, 0.6), mouth="o" if lt > 4.4 else "flat", cap="")
    NORA(c, 1560, GROUND, 0.85, t, face=-1, eyes="happy" if lt > 7 else "dot", mouth="grin" if lt > 7 else "smile", look=(-1, 0.4))
    if lt > 7.2:
        hx, hy = head_xy(1560, GROUND, 0.85, "nora")
        label(c, "Nora", hx, hy - 110, 46, "#F4C430", a=255 * clamp((lt - 7.2) / 0.4))
    K.end(c)


def a_poster(c, t):                    # 37,5–48,7  vé hạng ba · con tàu ai cũng bàn tán · "Titanic"
    lt = t - 37.53
    grad(c, skia.Rect.MakeWH(W, H), "#3A3028", "#1E1814")
    if lt < 4.0:
        q = ease_shot(t, 37.53, 41.5)
        ticket(c, W / 2, H / 2 - 30, lerp(1.6, 1.8, q), rot=-4 + q * 2)
        return
    q = ease_shot(t, 41.6, 48.66)
    c.save(); c.translate(W / 2, H / 2 - 20); c.rotate(-2); c.scale(lerp(0.95, 1.05, q), lerp(0.95, 1.05, q))
    fo(c, rect(-760, -420, 1520, 820), "#EDE2C6", ow=10)
    c.drawRect(skia.Rect.MakeXYWH(-740, -400, 1480, 120), P("#7A2A22"))
    text(c, "WHITE STAR LINE", 0, -320, "xbold", 52, "#F2EAD6", align="center")
    c.save(); c.translate(0, 160); c.scale(0.4, 0.4)
    titanic(c, 0, 0, 1.0, t, smoke=True)
    c.restore()
    c.drawRect(skia.Rect.MakeXYWH(-740, 190, 1480, 190), P("#2E4A6A"))
    if t > 46.0:
        p = back_out(clamp((t - 46.0) / 0.45))
        c.save(); c.translate(0, 330); c.scale(p, p)
        text(c, "TITANIC", 0, 0, "xbold", 150, "#F4D88A", align="center", stroke=12, stroke_color="#1A120A")
        c.restore()
    c.restore()


# ================================================================ B. Bến cảng Queenstown (48,7 – 92,1)
def harbor_bg(c, K, t):
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#9AA8B4", "#DDE2E0")
    K.end(c)
    K.layer(c, 0.4)
    for k in range(-2, 7):
        hx = k * 330 + 60
        fo(c, rect(hx, 460, 260, 260), ["#C8B898", "#B8A888", "#D0C4A8"][k % 3], ow=5)
        roof = skia.Path(); roof.moveTo(hx - 20, 470); roof.lineTo(hx + 130, 380); roof.lineTo(hx + 280, 470); roof.close()
        fo(c, roof, "#5A5050", ow=5)
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND, W + 6000, 900), P("#8A8278"))
    c.drawLine(-3000, GROUND, W + 3000, GROUND, P(INK, stroke=6))
    K.end(c)


def b_goodbye(c, t):                   # 48,7–63,8  mẹ tiễn ra bến · tràng hạt cho Nora · "Con là anh…" · gật đầu
    lt = t - 48.66
    if t < 53.36:
        q = ease_shot(t, 48.66, 53.36)
        K = Cam(lerp(800, 960, q), 540, 1.1, t=t)
        harbor_bg(c, K, t)
        K.layer(c, 1.0)
        for i, (who, x, s) in enumerate([("ir_mom", 600, ADULT), ("nora", 780, 0.85), ("ir_you", 960, ADULT)]):
            ST(c, who, x + lt * 60, GROUND, s, t + i, face=1, walk=lt * 4.2 + i, eyes="dot", mouth="flat", shawl="#6A5A6A" if who == "ir_mom" else None)
        K.end(c)
        if lt < 2.5:
            label(c, "Queenstown · 11/4/1912", W / 2, 160, 60, "#FFFFFF", a=255 * clamp(lt / 0.4) * clamp((2.5 - lt) / 0.4))
        return
    if t < 59.95:
        q = ease_shot(t, 53.36, 59.95)
        give = ease_out(clamp((t - 53.6) / 1.0))
        hold = t > 56.0
        K = Cam(lerp(940, 1000, q), lerp(500, 470, q), lerp(1.6, 1.8, q), t=t)
        harbor_bg(c, K, t)
        K.layer(c, 1.0)
        ST(c, "ir_mom", 900, GROUND, ADULT, t, face=1, shawl="#6A5A6A", eyes="dot", mouth="flat",
           hand_f=(lerp(60, 140, give), lerp(150, 60, give)) if not hold else (230, 40), look=(1, 0.3) if not hold else (1, -0.2))
        NORA(c, 1080, GROUND, 0.85, t, face=-1, hand_f=(90, 70), eyes="dot", look=(-1, 0.4), mouth="flat")
        YOU(c, 1280, GROUND, ADULT, t, face=-1, hand_f=(lerp(30, 120, ease_out(clamp((t - 56) / 0.6))), 60), eyes="dot", look=(-1, 0), mouth="flat")
        rx, ry = 900 + ADULT * (88 + lerp(60, 140, give) - 20), GROUND - ADULT * (366 - lerp(150, 60, give))
        if not hold:
            for k in range(7):
                c.drawCircle(rx + 6 + 5 * math.cos(k), ry + k * 9, 4, P("#5A3A2A"))
        K.end(c)
        return
    q = ease_shot(t, 59.95, 63.8)
    K = Cam(1290, lerp(400, 390, q), lerp(2.5, 2.8, q), t=t)
    harbor_bg(c, K, t)
    K.layer(c, 1.0)
    nod = math.sin(clamp((t - 60.1) / 0.9) * math.pi * 2) * 14 if t < 61.2 else 0
    YOU(c, 1280, GROUND, ADULT, t, face=-1, eyes="dot", look=(-1, 0), mouth="flat", head_tilt=nod, brow=0.4)
    K.end(c)


def b_tender(c, t):                    # 63,8–69,8  tàu quá lớn không cập bờ · thuyền nhỏ ra vịnh
    q = ease_shot(t, 63.8, 69.82)
    K = Cam(lerp(800, 1100, q), 540, 1.05, t=t)
    sea_bg(c, K, t)
    K.layer(c, 1.0)
    bx = 600 + (t - 63.8) * 90
    c.save(); c.translate(bx, 860 + 6 * math.sin(t * 1.6)); c.rotate(1.5 * math.sin(t * 1.3))
    hull = skia.Path(); hull.moveTo(-420, -60); hull.lineTo(420, -60); hull.quadTo(380, 70, 0, 80); hull.quadTo(-380, 70, -420, -60); hull.close()
    fo(c, hull, "#3A3A40", ow=7)
    fo(c, rect(-120, -200, 160, 140), "#5A5A60", ow=5)
    c.drawLine(-40, -200, -40, -320, P(INK, stroke=14))
    c.restore()
    for i, who in enumerate(["pax0", "paxw1", "ir_you", "nora", "pax2", "paxw3"]):
        ST(c, who, bx - 330 + i * 120, 860 - 60, 0.55, t + i, face=1, idle=0.5)
    K.end(c)
    sea_front(c, K, t)


def b_reveal(c, t):                    # 69,8–79,6  Titanic hiện ra · cao như tòa nhà nhiều tầng, bốn ống khói
    q = ease_shot(t, 69.82, 79.56)
    K = Cam(lerp(1000, 960, q), lerp(820, 420, q), lerp(2.0, 0.85, q), t=t)
    sea_bg(c, K, t)
    K.layer(c, 1.0)
    titanic(c, 980, 760, 0.62, t)
    K.end(c)
    sea_front(c, K, t, y=880)
    K.layer(c, 1.6)
    c.save(); c.translate(400, 1060)      # thuyền nhỏ tiền cảnh, bạn ngước nhìn
    hull = skia.Path(); hull.moveTo(-500, -40); hull.lineTo(500, -40); hull.lineTo(460, 120); hull.lineTo(-460, 120); hull.close()
    fo(c, hull, "#2E2E34", ow=8)
    c.restore()
    YOU(c, 420, 1020, 0.9, t, face=1, eyes="wide", look=(0.5, -1), mouth="o")
    NORA(c, 260, 1020, 0.8, t, face=1, eyes="wide", look=(0.6, -1), mouth="o")
    K.end(c)


def b_inspect(c, t):                   # 79,6–92,1  xếp hàng kiểm tra sức khỏe · lật mí mắt · xem tóc · qua được
    lt = t - 79.56
    if t < 83.81:
        q = ease_shot(t, 79.56, 83.81)
        K = Cam(lerp(800, 1000, q), 540, 1.1, t=t)
        harbor_bg(c, K, t)
        K.layer(c, 1.0)
        fo(c, rect(380, 700, 260, 160), "#7A6A50", ow=6)
        ST(c, "doctor", 460, GROUND, ADULT, t, face=1, hand_f=(120, 40), eyes="dot", mouth="flat")
        for i, who in enumerate(["paxw0", "pax1", "ir_you", "nora", "paxw2", "pax3", "pax4"]):
            ST(c, who, 760 + i * 190, GROUND, 0.88, t + i * 0.3, face=-1, eyes="dot", mouth="flat", idle=0.7)
        K.end(c)
        return
    if t < 89.64:
        q = ease_shot(t, 83.81, 89.64)
        K = Cam(lerp(740, 820, q), 430, lerp(2.3, 2.5, q), t=t)
        harbor_bg(c, K, t)
        K.layer(c, 1.0)
        eye = t < 86.6
        ST(c, "doctor", 560, GROUND, ADULT, t, face=1, hand_f=(190, -150) if eye else (200, -190), hand_b=(150, -120), eyes="squint", mouth="flat")
        if eye:
            YOU(c, 860, GROUND, ADULT, t, face=-1, eyes="wide", look=(-1, -0.6), mouth="flat")
        else:
            NORA(c, 840, GROUND, 0.85, t, face=-1, eyes="dot", look=(0, 0.6), mouth="flat", head_tilt=14)
        K.end(c)
        return
    K = Cam(960, 520, 1.6, t=t)
    harbor_bg(c, K, t)
    K.layer(c, 1.0)
    YOU(c, 880, GROUND, ADULT, t, face=1, eyes="happy", mouth="grin")
    NORA(c, 1060, GROUND, 0.85, t, face=-1, eyes="happy", mouth="grin", hand_f=(60, -200))
    K.end(c)
    p = back_out(clamp((t - 89.9) / 0.35))
    c.save(); c.translate(1500, 300); c.rotate(-12); c.scale(p, p)
    fo(c, rrect(-220, -70, 440, 140, 20), "#FFFFFF", ow=0, a=0)
    c.drawRoundRect(skia.Rect.MakeXYWH(-220, -70, 440, 140), 20, 20, P("#2E8B57", stroke=12))
    text(c, "ĐẠT", 0, 30, "xbold", 90, "#2E8B57", align="center")
    c.restore()


# ================================================================ C. Trên tàu (92,1 – 166,9)
def cabin(c, K, t, light=1.0, night=False):
    K.layer(c, 0.8)
    grad(c, skia.Rect.MakeXYWH(-2000, -2000, W + 4000, H + 4000), "#D8CCB0" if light > 0.5 else "#2A2620", "#B8AC90" if light > 0.5 else "#1A1612")
    c.drawCircle(1500, 400, 70, P("#3A3A3A")); c.drawCircle(1500, 400, 56, P("#1E2A40" if night else "#9AC0D8"))
    c.drawCircle(1500, 400, 70, P(INK, stroke=10))
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-2000, GROUND, W + 4000, 900), P("#7A6A52" if light > 0.5 else "#2A241E"))
    c.drawLine(-2000, GROUND, W + 2000, GROUND, P(INK, stroke=6))
    fo(c, rect(300, 560, 520, 50), "#8A6A44", ow=5); fo(c, rect(300, 760, 520, 50), "#8A6A44", ow=5)      # giường tầng
    fo(c, rect(320, 530, 480, 34), "#F2EEE4", ow=4); fo(c, rect(320, 730, 480, 34), "#F2EEE4", ow=4)
    c.drawLine(300, 300, 300, GROUND, P(INK, stroke=12)); c.drawLine(820, 300, 820, GROUND, P(INK, stroke=12))
    c.drawLine(1000, 120, 1000, 260, P(INK, stroke=5))
    c.drawCircle(1000, 280, 26, P("#FFF2B0" if light > 0.5 else "#5A5040"))
    if light > 0.5:
        c.drawCircle(1000, 280, 120, blur("#FFF2B0", 120 * light, 40))
    c.drawCircle(1000, 280, 26, P(INK, stroke=5))
    K.end(c)


def c_bulb(c, t):                      # 92,1–98,45  những ngày đầu như giấc mơ · phòng có đèn điện
    lt = t - 92.11
    q = ease_shot(t, 92.11, 98.45)
    flick = 1.0 if (lt < 2.5 or lt > 4.0 or int(lt * 4) % 2 == 0) else 0.0
    K = Cam(lerp(1000, 1060, q), lerp(520, 480, q), lerp(1.3, 1.5, q), t=t)
    cabin(c, K, t, light=flick)
    K.layer(c, 1.0)
    pull = 2.5 < lt < 4.0
    YOU(c, 1080, GROUND, ADULT, t, face=-1, hand_f=(90, -220 + (30 if pull and int(lt * 4) % 2 else 0)), eyes="wide", look=(-0.4, -1), mouth="grin", cap="")
    c.drawLine(1010, 300, 1010, 430, P(INK, stroke=3))
    K.end(c)


def c_meal(c, t):                      # 98,45–105,67  ba bữa no nê: bánh mì trắng, súp nóng, thịt hầm
    q = ease_shot(t, 98.45, 105.67)
    K = Cam(lerp(860, 1000, q), lerp(560, 540, q), lerp(1.35, 1.45, q), t=t)
    K.layer(c, 0.8)
    grad(c, skia.Rect.MakeXYWH(-2000, -2000, W + 4000, H + 4000), "#F2EEE4", "#D8D2C2")
    for k in range(-2, 8):
        c.drawLine(k * 300, 120, k * 300, GROUND, P("#C8C0AC", stroke=12))
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-2000, GROUND, W + 4000, 900), P("#9A8A6A"))
    fo(c, rect(380, 700, 1200, 40), "#8A6A44", ow=6)
    for i, (who, x) in enumerate([("pax0", 440), ("ir_you", 760), ("nora", 1000), ("paxw2", 1260), ("pax3", 1500)]):
        chew = math.sin(t * 9 + i)
        ST(c, who, x, GROUND, 0.85 if who == "nora" else 0.9, t + i, face=1 if i % 2 == 0 else -1, sit=1.0,
           hand_f=(110, -40 + 30 * max(0, chew)) if who == "ir_you" else (100, 40), eyes="happy" if who in ("ir_you", "nora") else "dot",
           mouth="grin" if chew > 0 else "o", cap="" if who == "ir_you" else None)
    for k in range(5):
        px = 470 + k * 260
        c.drawOval(skia.Rect.MakeXYWH(px - 60, 680, 120, 26), P("#FFFFFF")); c.drawOval(skia.Rect.MakeXYWH(px - 60, 680, 120, 26), P(INK, stroke=4))
        c.drawOval(skia.Rect.MakeXYWH(px - 30, 668, 60, 22), P("#C8843A"))
        fo(c, rrect(px + 50, 660, 60, 34, 12), "#F2E2B8", ow=3)
    K.end(c)


def c_dance(c, t):                     # 105,67–112,82  buổi tối: kèn túi, đàn, nắm tay nhảy múa đến khuya
    lt = t - 105.67
    q = ease_shot(t, 105.67, 112.82)
    K = Cam(lerp(800, 1150, q), 540, 1.15, t=t)
    K.layer(c, 0.8)
    grad(c, skia.Rect.MakeXYWH(-2000, -2000, W + 4000, H + 4000), "#6A5A44", "#3A3024")
    for k in range(-2, 8):
        c.drawCircle(k * 320 + 160, 260, 18, P("#FFE8A8")); c.drawCircle(k * 320 + 160, 260, 70, blur("#FFE8A8", 70, 20))
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-2000, GROUND, W + 4000, 900), P("#5A4A36"))
    ST(c, "pax1", 300, GROUND, 0.9, t, face=1, hand_f=(100, -40), hand_b=(80, -10), eyes="closed", mouth="o")     # kèn túi
    fo(c, oval(300 + 0.9 * 130, GROUND - 0.9 * 330, 50, 40), "#5A7A4A", ow=4)
    for k in range(3):
        c.drawLine(300 + 0.9 * 130, GROUND - 0.9 * 360, 300 + 0.9 * (150 + k * 30), GROUND - 0.9 * (520 + k * 20), P(INK, stroke=6))
    ST(c, "pax4", 480, GROUND, 0.9, t, face=1, hand_f=(100, -120), hand_b=(60, -140), eyes="happy", mouth="smile")  # đàn vĩ cầm
    ring = [("nora", 0.82), ("pax0", 0.9), ("paxw1", 0.88), ("ir_you", 0.9), ("paxw3", 0.88), ("pax2", 0.9)]
    for i, (who, s) in enumerate(ring):
        a = lt * 1.6 + i * 2 * math.pi / len(ring)
        x = 1100 + 340 * math.cos(a)
        y = GROUND + 60 * math.sin(a)
        ST(c, who, x, y, s * (0.92 + 0.08 * math.sin(a)), t + i, face=1 if math.sin(a) < 0 else -1, walk=lt * 7 + i, hand_f=(120, -80), hand_b=(-80, -80),
           eyes="happy", mouth="grin", cap="" if who == "ir_you" else None)
    K.end(c)
    for k in range(3):
        q2 = (t * 0.7 + k / 3) % 1
        text(c, "♪", 420 + k * 60 + 80 * q2, 380 - 160 * q2, "xbold", 60, "#F4D88A", a=255 * (1 - q2), align="center")


def c_patrick(c, t):                   # 112,82–125,58  làm quen Patrick · nói nhiều, cười to, hứa dẫn đi xem nhà chọc trời
    lt = t - 112.82
    q = ease_shot(t, 112.82, 125.58)
    K = Cam(lerp(960, 1000, q), lerp(500, 470, q), lerp(1.5, 1.65, q), t=t)
    K.layer(c, 0.8)
    grad(c, skia.Rect.MakeXYWH(-2000, -2000, W + 4000, H + 4000), "#6A5A44", "#3A3024")
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-2000, GROUND, W + 4000, 900), P("#5A4A36"))
    laugh = math.sin(lt * 6)
    PAT(c, 1160, GROUND, 1.02, t, face=-1, hand_f=(160, -120 + 40 * math.sin(lt * 3)) if lt > 6 else (70, 40), eyes="happy" if laugh > 0 else "dot",
        mouth="grin" if laugh > -0.3 else "open", lean=-4 + 3 * laugh)
    YOU(c, 820, GROUND, ADULT, t, face=1, eyes="dot", look=(1, -0.2), mouth="smile", cap="")
    NORA(c, 640, GROUND, 0.85, t, face=1, eyes="dot", look=(1, -0.2), mouth="smile")
    if lt < 2.5:
        hx, hy = head_xy(1160, GROUND, 1.02, "patrick")
        label(c, "Patrick", hx, hy - 130, 50, "#F4C430", a=255 * clamp(lt / 0.4))
    K.end(c)
    if lt > 6.5:   # bong bóng tưởng tượng: nhà chọc trời
        a = clamp((lt - 6.5) / 0.6)
        c.drawCircle(1500, 260, 220 * a, P("#FFFFFF", 230)); c.drawCircle(1500, 260, 220 * a, P(INK, stroke=6))
        for k, r in enumerate([22, 14]):
            c.drawCircle(1340 - k * 50, 470 + k * 50, r * a, P("#FFFFFF")); c.drawCircle(1340 - k * 50, 470 + k * 50, r * a, P(INK, stroke=4))
        if a > 0.6:
            skyline(c, 1500, 380, 0.42)


def c_night(c, t):                     # 125,58–139,34  đêm Chủ nhật 14/4 · biển phẳng, nhiều sao, không trăng · ngủ sớm
    lt = t - 125.58
    if t < 134.81:
        q = ease_shot(t, 125.58, 134.81)
        K = Cam(lerp(700, 1200, q), 520, lerp(1.0, 1.08, q), t=t)
        sea_bg(c, K, t, night=1.0, calm=True)
        K.layer(c, 0.9)
        titanic(c, 1000 + lt * 20, 700, 0.42, t, night=True)
        K.end(c)
        K.layer(c, 1.1)
        wave_band(c, 880, t * 0.2, "#0E1426", amp=2, x0=-4000, x1=W + 4000)
        for k in range(30):
            c.drawLine(-400 + k * 90, 920 + (k % 3) * 30, -360 + k * 90, 920 + (k % 3) * 30, P("#F6D88A", 50, stroke=3))
        K.end(c)
        if lt < 2.4:
            label(c, "Chủ nhật · 14/4/1912", W / 2, 160, 60, "#FFFFFF", a=255 * clamp(lt / 0.4) * clamp((2.4 - lt) / 0.4))
        return
    q = ease_shot(t, 134.81, 139.34)
    K = Cam(560, lerp(600, 620, q), lerp(1.6, 1.75, q), t=t)
    cabin(c, K, t, light=0.0, night=True)
    K.layer(c, 1.0)
    c.save(); c.translate(760, 520); c.rotate(-90)
    YOU(c, 0, 0, 0.7, t, face=1, hand_f=(20, 120), hand_b=(-20, 120), eyes="closed", mouth="flat", cap="")
    c.restore()
    fo(c, rrect(530, 470, 260, 70, 30), "#6A7A9A", ow=5)
    K.end(c)


def c_impact(c, t):                    # 139,34–151,5  rung nhẹ như cọ vào gì đó · máy chạy thêm rồi im bặt · im lặng đáng sợ
    lt = t - 139.34
    if lt < 3.2:
        q = ease_shot(t, 139.34, 142.5)
        K = Cam(lerp(1300, 1200, q), 560, lerp(1.4, 1.3, q), t=t, shake=4 * clamp((lt - 1.2) / 0.3) * clamp((2.6 - lt) / 0.4))
        sea_bg(c, K, t, night=1.0, calm=True)
        K.layer(c, 0.8)
        iceberg(c, 1500 - lt * 40, 700, 0.75)
        titanic(c, 700 + lt * 60, 760, 0.42, t, night=True)
        K.end(c)
        sea_front(c, K, t, night=1.0, calm=True)
        return
    q = ease_shot(t, 142.5, 151.5)
    K = Cam(620, lerp(560, 540, q), lerp(2.2, 2.5, q), t=t)
    cabin(c, K, t, light=0.0, night=True)
    K.layer(c, 1.0)
    c.save(); c.translate(760, 520); c.rotate(-90)
    YOU(c, 0, 0, 0.7, t, face=1, hand_f=(20, 120), hand_b=(-20, 120), eyes="wide", look=(0.5, 0), mouth="flat", cap="", idle=0.1)
    c.restore()
    fo(c, rrect(530, 470, 260, 70, 30), "#6A7A9A", ow=5)
    K.end(c)


def c_ice(c, t):                       # 151,5–166,91  boong trước có băng vụn · người ta ném băng đùa · "con tàu không thể chìm"
    lt = t - 151.5
    q = ease_shot(t, 151.5, 166.91)
    K = Cam(lerp(800, 1150, q), 540, lerp(1.15, 1.25, q), t=t)
    deck_bg(c, K, t, night=1.0)
    K.layer(c, 1.0)
    for k in range(14):
        x = 300 + (k * 137) % 1500
        fo(c, oval(x, GROUND + 30 + (k % 3) * 40, 26 + (k % 4) * 8, 14 + (k % 3) * 5), "#E8F4FA", ow=3)
    throw = (lt * 0.8) % 1
    ST(c, "pax0", 1250, GROUND, 0.92, t, face=-1, hand_f=(lerp(-60, 160, throw), lerp(60, -160, throw)), eyes="happy", mouth="grin")
    ST(c, "pax2", 700, GROUND, 0.92, t, face=1, hand_f=(80, -60), eyes="happy", mouth="open")
    bx, by = lerp(1150, 780, throw), GROUND - 300 - 160 * math.sin(math.pi * throw)
    fo(c, oval(bx, by, 16, 12), "#E8F4FA", ow=3)
    YOU(c, 1500, GROUND, ADULT, t, face=-1, eyes="dot", look=(-1, 0.4), mouth="flat")
    K.end(c)



# ================================================================ D. Nước tràn, tìm Nora, xuồng cứu sinh (166,9 – 250,5)
def d_water(c, t):                     # 166,91–180,62  nước tràn vào hành lang · dâng tới mắt cá · điều tồi tệ
    lt = t - 166.91
    if t < 170.59:
        q = ease_shot(t, 166.91, 170.59)
        K = Cam(lerp(800, 960, q), 540, 1.2, t=t)
        corridor(c, K, t)
        K.layer(c, 1.0)
        x = lerp(400, 900, ease_out(clamp(lt / 3.0)))
        YOU(c, x, GROUND, ADULT, t, face=1, walk=lt * 5 if lt < 3.0 else None, eyes="dot", mouth="flat")
        K.end(c)
        water_over(c, K, t, 6 + lt * 4, a=150)
        return
    if t < 176.44:   # cận bàn chân, nước dâng
        lv = lerp(20, 140, ease_shot(t, 170.59, 176.44))
        grad(c, skia.Rect.MakeWH(W, H), "#C8C0AC", "#A89E88")
        c.drawRect(skia.Rect.MakeXYWH(0, 820, W, 400), P("#8A7A62"))
        for sd in (-1, 1):
            fx = W / 2 + sd * 160
            c.drawLine(fx, -100, fx, 780, P(INK, stroke=44))
            c.drawLine(fx - 10, 800, fx + sd * 0 + 170, 800, P(INK, stroke=50))
        wave_band(c, 820 - lv, t * 2, "#2E6A88", amp=10, x0=-200, x1=W + 200, a=200)
        return
    q = ease_shot(t, 176.44, 180.62)
    K = Cam(940, lerp(430, 420, q), lerp(2.4, 2.8, q), t=t)
    corridor(c, K, t)
    K.layer(c, 1.0)
    YOU(c, 900, GROUND, ADULT, t, face=1, eyes="wide", look=(0, 1), mouth="o", brow=1.0, sweat=1.0, idle=0.3)
    K.end(c)
    water_over(c, K, t, 40, a=170)


def d_crowd(c, t):                     # 180,62–196,25  tìm Nora phía đuôi tàu · hành lang chật kín · cửa sắt chặn lối
    lt = t - 180.62
    if t < 192.53:
        q = ease_shot(t, 180.62, 192.53)
        K = Cam(lerp(600, 1300, q), 540, 1.15, t=t, shake=2)
        corridor(c, K, t)
        K.layer(c, 1.0)
        crowd = [("paxw0", 300, 1), ("pax1", 520, -1), ("paxw2", 760, 1), ("pax3", 1020, -1), ("paxw4", 1300, 1), ("pax0", 1560, -1), ("paxw1", 1820, 1),
                 ("pax2", 2080, -1)]
        for i, (who, x, f) in enumerate(crowd):
            ST(c, who, x + 30 * math.sin(lt * 1.5 + i), GROUND + (i % 2) * 30, 0.9, t + i, face=f, walk=lt * 4 + i, eyes="wide", mouth="o",
               hand_f=(100, 40) if i % 3 == 0 else None, sweat=0.6)
            if i % 3 == 0:
                fo(c, rrect(x + f * 90 - 50, GROUND - 330, 100, 70, 10), "#7A5A3A", ow=4)
        YOU(c, 500 + lt * 95, GROUND + 60, ADULT, t, face=1, walk=lt * 6, eyes="wide", mouth="flat", lean=8)
        K.end(c)
        water_over(c, K, t, 30, a=140)
        return
    q = ease_shot(t, 192.53, 196.25)
    K = Cam(1460, 560, lerp(1.4, 1.55, q), t=t)
    corridor(c, K, t, gate=True)
    K.layer(c, 1.0)
    for i, who in enumerate(["pax0", "paxw2", "pax4"]):
        ST(c, who, 1180 - i * 160, GROUND, 0.9, t + i, face=1, hand_f=(150, -60 - 20 * math.sin(t * 8 + i)), eyes="wide", mouth="open", sweat=1.0)
    K.end(c)
    water_over(c, K, t, 34, a=140)


def d_find(c, t):                      # 196,25–208,29  tìm thấy Nora run rẩy, nắm chặt tràng hạt · ba người len lên boong
    lt = t - 196.25
    if t < 202.15:
        q = ease_shot(t, 196.25, 202.15)
        K = Cam(lerp(960, 1000, q), lerp(480, 460, q), lerp(1.8, 2.0, q), t=t)
        corridor(c, K, t)
        K.layer(c, 1.0)
        NORA(c, 960, GROUND, 0.85, t, face=1, hand_f=(60, 60), hand_b=(30, 70), shiver=0.8, eyes="wide", mouth="wobble", tears=0.6)
        YOU(c, 1260, GROUND, ADULT, t, face=-1, hand_f=(lerp(40, 150, ease_out(clamp((lt - 1.5) / 0.6))), 40), eyes="dot", look=(-1, 0.3), mouth="flat")
        rx, ry = 960 + 0.85 * (88 + 60 - 20), GROUND - 0.85 * (366 - 60)
        for k in range(7):
            c.drawCircle(rx + 4 * math.cos(k), ry + k * 8, 4, P("#5A3A2A"))
        K.end(c)
        water_over(c, K, t, 40, a=160)
        return
    q = ease_shot(t, 202.15, 208.29)
    K = Cam(lerp(800, 1160, q), lerp(600, 380, q), 1.1, t=t)
    K.layer(c, 0.8)
    grad(c, skia.Rect.MakeXYWH(-2000, -2000, W + 4000, H + 4000), "#D8D0BC", "#B0A890")
    K.end(c)
    K.layer(c, 1.0)
    stairs = skia.Path(); stairs.moveTo(300, GROUND + 200)
    for k in range(10):
        stairs.lineTo(300 + k * 120, GROUND + 200 - k * 70); stairs.lineTo(300 + (k + 1) * 120, GROUND + 200 - k * 70)
    stairs.lineTo(1500, GROUND + 400); stairs.lineTo(300, GROUND + 400); stairs.close()
    fo(c, stairs, "#8A6A44", ow=6)
    for i, (fn, kw, s) in enumerate([(PAT, {}, 1.0), (NORA, {}, 0.82), (YOU, {}, ADULT)]):
        prog = clamp((t - 202.15) / 5.5 - i * 0.08)
        k = prog * 8
        x = 360 + k * 120 + i * -110
        y = GROUND + 200 - max(0, math.floor((x - 300) / 120)) * 70
        fn(c, x, y, s, t + i, face=1, walk=t * 6 + i, hand_f=(150, 40) if i else (60, 40), eyes="dot", mouth="flat", lean=10)
    K.end(c)


def d_deck(c, t):                      # 208,29–223,23  gió lạnh như dao cắt · xuồng hạ · "phụ nữ và trẻ em lên trước" · chỉ đủ một nửa
    lt = t - 208.29
    if t < 217.63:
        q = ease_shot(t, 208.29, 217.63)
        K = Cam(lerp(800, 1100, q), 520, 1.05, t=t)
        deck_bg(c, K, t, night=1.0)
        K.layer(c, 1.0)
        for k in range(3):
            dx = 500 + k * 600
            c.drawLine(dx, GROUND - 160, dx + 60, GROUND - 420, P(INK, stroke=14)); c.drawLine(dx + 60, GROUND - 420, dx + 160, GROUND - 420, P(INK, stroke=10))
            low = clamp((lt - k * 1.6) / 5)
            c.drawLine(dx + 160, GROUND - 420, dx + 160, GROUND - 330 + low * 300, P(INK, 180, stroke=3))
            lifeboat(c, dx + 160, GROUND - 330 + low * 300, 0.55, people=[("paxw0", {}), ("paxw2", {}), ("nora" if k == 9 else "paxw3", {})][:2], t=t)
        ST(c, "sailor", 1350, GROUND, 0.95, t, face=-1, hand_f=(60, -200) if lt > 2.4 else (60, 40), eyes="dot", mouth="open" if lt > 2.4 else "flat")
        for i, (fn, s, x) in enumerate([(PAT, 1.0, 1650), (NORA, 0.82, 1800), (YOU, ADULT, 1940)]):
            fn(c, x, GROUND + 60, s, t + i, face=-1, eyes="wide", mouth="flat", shiver=0.3)
        K.end(c)
        for k in range(6):   # gió
            y = 200 + k * 120
            x = (t * 900 + k * 330) % (W + 600) - 300
            c.drawLine(W - x, y, W - x - 180, y + 6, P("#FFFFFF", 90, stroke=4))
        return
    # đồ họa: số chỗ trên xuồng ≈ một nửa số người
    grad(c, skia.Rect.MakeWH(W, H), "#141A2E", "#0A0E1A")
    p = clamp((t - 217.63) / 1.2)
    n_people = 40
    for i in range(n_people):
        x = 260 + (i % 20) * 72; y = 300 + (i // 20) * 120
        safe = i % 2 == 0
        col = "#F2EEE4" if (safe or p < 1) else "#5A6070"
        c.drawCircle(x, y, 16, P(col)); c.drawLine(x, y + 16, x, y + 56, P(col, stroke=8))
    if p > 0.3:
        for k in range(10):
            lifeboat(c, 300 + k * 140, 700, 0.18)
    label(c, "Xuồng cứu sinh: chỉ đủ cho khoảng một nửa", W / 2, 880, 60, "#F4C430", a=255 * clamp((t - 218.4) / 0.5))


def d_part(c, t):                      # 223,23–240,66  đẩy Nora ra xuồng · "Anh phải đi cùng em!" · lời nói dối · quấn khăn cho em
    lt = t - 223.23
    q = ease_shot(t, 223.23, 240.66)
    if t < 229.3:
        K = Cam(lerp(1000, 1060, q), 470, lerp(1.7, 1.9, q), t=t)
    elif t < 235.46:
        K = Cam(1180, 410, lerp(2.4, 2.6, ease_shot(t, 229.3, 235.46)), t=t)      # cận mặt bạn: nụ cười gượng
    else:
        K = Cam(1040, 480, 1.8, t=t)
    deck_bg(c, K, t, night=1.0)
    K.layer(c, 1.0)
    lifeboat(c, 640, GROUND - 120, 0.75, people=[("paxw0", {}), ("paxw2", {}), ("paxw4", {})], t=t)
    cling = t < 235.46
    wrap = ease_out(clamp((t - 235.6) / 1.4))
    NORA(c, 960 - (200 * clamp((t - 238.6) / 1.6)), GROUND - (60 * clamp((t - 238.6) / 1.6)), 0.82, t, face=1,
         hand_f=(170, -20) if cling else (60, 60), hand_b=(150, 0) if cling else (30, 70), eyes="closed" if 224.99 < t < 229.3 else "wide",
         mouth="open" if 224.99 < t < 229.3 else "wobble", tears=1.0, scarf="#C04A3A" if wrap > 0.6 else None)
    YOU(c, 1200, GROUND, ADULT, t, face=-1, hand_f=(lerp(60, 200, wrap), lerp(60, -40, wrap)) if t > 235.46 else (150, 40),
        eyes="happy" if 229.3 < t < 235.46 else "dot", mouth="smile" if 229.3 < t < 235.46 else "flat", look=(-1, 0.5),
        scarf="#C04A3A" if wrap < 0.6 else None, tears=0.4 if t > 231 else 0.0)
    K.end(c)


def d_lower(c, t):                     # 240,66–250,51  xuồng hạ xuống biển tối · mặt Nora thành chấm mờ · nhớ lời mẹ dặn
    lt = t - 240.66
    q = ease_shot(t, 240.66, 247.81)
    K = Cam(900, lerp(520, 760, q), lerp(1.5, 0.95, q), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-4000, -4000, W + 8000, H + 8000), "#060A18", "#0E1424")
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-4000, 1300, W + 8000, 2000), P("#0A1020"))
    fo(c, rect(1100, -2000, 2000, 2600), "#1A1A1E", ow=8)        # thân tàu
    for k in range(10):
        c.drawCircle(1180 + (k % 5) * 150, -300 + (k // 5) * 260, 14, P("#F6D88A"))
    by = lerp(120, 1260, ease_in_out(clamp(lt / 6.0)))
    c.drawLine(1010, -400, 1010, by, P("#AAAAAA", stroke=3)); c.drawLine(780, -400, 780, by, P("#AAAAAA", stroke=3))
    lifeboat(c, 900, by, 0.7, people=[("paxw0", {}), ("nora", {"eyes": "wide", "look": (0.5, -1), "tears": 1.0, "scarf": "#C04A3A"}), ("paxw2", {})], t=t)
    K.end(c)
    if t > 247.81:   # hồi ức mờ: mẹ ở bến cảng
        a = clamp((t - 247.81) / 0.5) * 0.55
        c.saveLayerAlpha(None, int(255 * a))
        b_goodbye(c, 55.0 + (t - 247.81) * 0.5)
        c.restore()



# ================================================================ E. Tàu chìm (250,5 – 337,2)
def e_tilt(c, t):                      # 250,51–257,02  mũi tàu chúi xuống, đuôi nhô cao · những chiếc xuồng cuối đã rời đi
    lt = t - 250.51
    q = ease_shot(t, 250.51, 257.02)
    K = Cam(lerp(900, 1000, q), 540, lerp(0.95, 1.05, q), t=t)
    sea_bg(c, K, t, night=1.0, calm=True)
    K.layer(c, 0.9)
    titanic(c, 960, 780 + 40 * q, 0.42, t, night=True, tilt=lerp(6, 11, q), smoke=False)
    for k in range(4):
        lifeboat(c, 200 + k * 140 + lt * 15, 900 + (k % 2) * 30, 0.16)
    K.end(c)
    sea_front(c, K, t, night=1.0, calm=True, y=880)


def e_band(c, t):                      # 257,02–264,05  ban nhạc vẫn chơi những bản nhạc nhẹ nhàng
    lt = t - 257.02
    q = ease_shot(t, 257.02, 264.05)
    K = Cam(lerp(860, 1000, q), lerp(520, 500, q), lerp(1.35, 1.5, q), t=t)
    deck_bg(c, K, t, night=1.0, tilt=-5)
    K.layer(c, 1.0)
    for i in range(4):
        bow = math.sin(lt * 5 + i)
        ST(c, "band", 700 + i * 200, GROUND + i * 10, 0.9, t + i, face=1, hand_f=(110 + 30 * bow, -110), hand_b=(70, -150), eyes="closed", mouth="flat",
           idle=0.5)
    K.end(c)
    for k in range(3):
        q2 = (t * 0.5 + k / 3) % 1
        text(c, "♪", 820 + k * 150 + 60 * q2, 300 - 140 * q2, "xbold", 54, "#F4D88A", a=200 * (1 - q2), align="center")


def e_stern(c, t):                     # 264,05–275,59  chạy về đuôi tàu, bám lan can · đèn chớp tắt, chìm vào bóng tối
    lt = t - 264.05
    lights = 1.0 if t < 270.94 else (0.0 if t > 273.4 else (1.0 if int((t - 270.94) * 6) % 2 == 0 else 0.0))
    q = ease_shot(t, 264.05, 275.59)
    K = Cam(lerp(900, 1050, q), lerp(560, 520, q), lerp(1.3, 1.45, q), t=t)
    deck_bg(c, K, t, night=1.0, tilt=lerp(-8, -16, q), lights=lights)
    K.layer(c, 1.0)
    if t < 266.91:
        x = lerp(500, 1000, ease_out(clamp(lt / 2.6)))
        PAT(c, x + 160, GROUND, 1.0, t, face=1, walk=lt * 7, run=True, hand_b=(-160, 40), eyes="wide", mouth="open", lean=14)
        YOU(c, x, GROUND, ADULT, t, face=1, walk=lt * 7 + 1, run=True, hand_f=(160, 30), eyes="wide", mouth="flat", lean=14)
    else:
        for i, who in enumerate(["pax0", "pax3", "ir_you", "patrick", "pax1", "paxw2"]):
            fn = PAT if who == "patrick" else (YOU if who == "ir_you" else None)
            s = 1.0 if who == "patrick" else 0.92
            kw = dict(face=1, hand_f=(120, 40), hand_b=(90, 50), eyes="wide", mouth="flat", lean=-10, idle=0.4)
            if fn:
                fn(c, 520 + i * 200, GROUND, s, t + i, **kw)
            else:
                ST(c, who, 520 + i * 200, GROUND, s, t + i, **kw)
    K.end(c)
    if lights == 0:
        c.drawRect(skia.Rect.MakeWH(W, H), P("#000000", 170))


def e_break(c, t):                     # 275,59–284,28  tiếng động như sấm · tàu gãy làm đôi · đuôi dựng đứng rồi tụt xuống biển
    lt = t - 275.59
    brk = clamp((t - 278.96) / 0.6)
    up = ease_in_out(clamp((t - 279.4) / 3.0))
    sink = clamp((t - 282.0) / 2.3)
    K = Cam(960, lerp(560, 520, up), lerp(1.0, 0.92, up), rot=lerp(0, -5, brk), t=t,
            shake=(10 * math.exp(-(t - 275.59) * 1.5) if t < 277 else 0) + (14 * math.exp(-(t - 278.96) * 2) if t > 278.96 else 0))
    sea_bg(c, K, t, night=1.0, calm=True)
    K.layer(c, 0.9)
    titanic(c, 960, 800 + 400 * sink, 0.42, t, night=True, lights=0.0, tilt=12 - 6 * brk, broken=brk, stern_up=up, smoke=False)
    K.end(c)
    sea_front(c, K, t, night=1.0, calm=True, y=900)
    if t > 278.96 and t - 278.96 < 0.08:
        c.drawRect(skia.Rect.MakeWH(W, H), P("#FFFFFF", 120))


def e_jump(c, t):                      # 284,28–286,51  hít một hơi thật sâu, rồi nhảy xuống
    lt = t - 284.28
    K = Cam(960, lerp(420, 900, ease_in_out(clamp((lt - 0.8) / 1.4))), 1.3, t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-4000, -4000, W + 8000, H + 8000), "#060A18", "#0E1424")
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-4000, 1300, W + 8000, 3000), P("#0A1428"))
    fo(c, rect(-600, 560, 1200, 2000), "#1A1A1E", ow=8)
    y = GROUND - 300 if lt < 0.8 else GROUND - 300 + 900 * ((lt - 0.8) / 1.4) ** 2
    YOU(c, 640 + (0 if lt < 0.8 else (lt - 0.8) * 260), y, ADULT, t, face=1, hand_f=(80, -230) if lt > 0.8 else (60, 40),
        hand_b=(-80, -230) if lt > 0.8 else (30, 50), eyes="closed" if lt < 0.8 else "wide", mouth="flat", crouch=0.6 if lt < 0.8 else 0.0)
    K.end(c)


def e_water(c, t):                     # 286,51–302,06  lạnh như nghìn mũi kim · ngoi lên thở hổn hển · tiếng kêu cứu · dưới điểm đóng băng
    lt = t - 286.51
    q = ease_shot(t, 286.51, 302.06)
    K = Cam(960, lerp(620, 560, q), lerp(1.9, 1.6, q), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-4000, -4000, W + 8000, H + 8000), "#04060E", "#0A1020")
    for k in range(60):
        x = (k * 173) % (W + 600) - 300; y = (k * 97) % 500
        c.drawCircle(x, y, 1.5 + (k % 3), P("#FFFFFF", 160))
    K.end(c)
    K.layer(c, 1.0)
    bob = 10 * math.sin(t * 2)
    YOU(c, 960, GROUND + 260 + bob, ADULT, t, face=1, hand_f=(120, -60 + 20 * math.sin(t * 3)), hand_b=(-80, -40), eyes="wide" if lt > 0.6 else "closed",
        mouth="open" if lt < 6 else "wobble", shiver=1.0, cap="")
    wave_band(c, GROUND - 40, t * 0.8, "#0E1830", amp=10, x0=-4000, x1=W + 4000, a=235)
    for k in range(10):        # vệt "mũi kim" băng giá
        ph = (lt * 1.5 + k * 0.17) % 1
        a = 200 * (1 - ph) * (1 if lt < 5 else 0.4)
        ang = k * 0.63
        r = 260 - 200 * ph
        c.drawLine(960 + r * math.cos(ang), 600 + r * 0.6 * math.sin(ang), 960 + (r - 40) * math.cos(ang), 600 + (r - 40) * 0.6 * math.sin(ang),
                   P("#DFF3FF", a, stroke=4))
    K.end(c)
    if t > 296.0:
        label(c, "−2°C", 1680, 160, 84, "#9FD3F0", a=255 * clamp((t - 296.0) / 0.5))


def e_overturned(c, t):                # 302,06–315,85  hình thù trắng bập bềnh · xuồng lật úp, vài chục người bám · bàn tay Patrick
    lt = t - 302.06
    q = ease_shot(t, 302.06, 315.85)
    K = Cam(lerp(800, 1000, q), lerp(600, 560, q), lerp(1.0, 1.5, q), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-4000, -4000, W + 8000, H + 8000), "#04060E", "#0A1020")
    K.end(c)
    K.layer(c, 1.0)
    bx, by = 1200, GROUND + 40 + 6 * math.sin(t * 1.4)
    hull = skia.Path(); hull.moveTo(bx - 340, by); hull.quadTo(bx, by - 120, bx + 340, by); hull.close()
    fo(c, hull, "#E8E4DA", ow=7)
    for i in range(7):
        ST(c, f"pax{i % 5}", bx - 260 + i * 85, by - 50 - 30 * math.sin((i + 0.5) / 7 * math.pi), 0.5, t + i, face=1, idle=0.4, eyes="closed",
           hand_f=(40, 100))
    pull = ease_out(clamp((t - 309.34) / 3.0))
    yx = lerp(500, bx - 380, ease_out(clamp(lt / 7.0)))
    YOU(c, yx, GROUND + 260 + 10 * math.sin(t * 2) - pull * 140, ADULT * 0.8, t, face=1, hand_f=(140 + 20 * math.sin(t * 6), -120), eyes="wide",
        mouth="open", shiver=0.8, cap="")
    if t > 309.34:
        PAT(c, bx - 300, by - 50, 0.55, t, face=-1, hand_f=(lerp(60, 200, ease_out(clamp((t - 309.34) / 1.0))), lerp(40, 160, ease_out(clamp((t - 309.34) / 1.0)))),
            eyes="dot", mouth="flat", crouch=0.6)
    wave_band(c, GROUND + 120, t * 0.8, "#0E1830", amp=10, x0=-4000, x1=W + 4000, a=235)
    K.end(c)


def e_balance(c, t):                   # 315,85–337,2  đứng trên lưng xuồng lật, nghiêng trái phải · không cảm nhận được chân · người buông tay · Patrick kể mãi
    lt = t - 315.85
    q = ease_shot(t, 315.85, 337.2)
    sway = 6 * math.sin(lt * 0.9)
    K = Cam(lerp(1000, 960, q), lerp(560, 520, q), lerp(1.45, 1.6, q), rot=sway * 0.25, t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-4000, -4000, W + 8000, H + 8000), lerp_col("#04060E", "#1A2238", clamp((lt - 16) / 6)), "#0A1020")
    K.end(c)
    K.layer(c, 1.0)
    c.save(); c.translate(960, GROUND + 40); c.rotate(sway)
    hull = skia.Path(); hull.moveTo(-420, 0); hull.quadTo(0, -140, 420, 0); hull.close()
    fo(c, hull, "#E8E4DA", ow=7)
    crew = ["pax0", "pax1", "ir_you", "patrick", "pax2", "pax3", "pax4"]
    for i, who in enumerate(crew):
        gone = (who in ("pax1", "pax4")) and lt > (8.0 if who == "pax1" else 11.0)
        fade = 1 - clamp((lt - (8.0 if who == "pax1" else 11.0)) / 1.2) if who in ("pax1", "pax4") else 1.0
        if fade <= 0.02:
            continue
        x = -330 + i * 110
        y = -40 - 40 * math.sin((i + 0.5) / len(crew) * math.pi)
        talk = who == "patrick"
        ST(c, who, x, y, 0.62 if who != "patrick" else 0.68, t + i, face=1 if i < 3 else -1, lean=-sway * 1.2, alpha=fade, shiver=0.5,
           hand_f=(140, -100 + 30 * math.sin(lt * 4)) if talk and lt > 13 else (60, 60), eyes="closed" if (who == "ir_you" and 8 < lt < 13) else "dot",
           mouth="open" if talk and lt > 13 and int(lt * 3) % 2 == 0 else "flat", cap="" if who == "ir_you" else None)
    c.restore()
    wave_band(c, GROUND + 90, t * 0.6, "#0E1830", amp=8, x0=-4000, x1=W + 4000, a=235)
    K.end(c)
    if lt > 13.2:   # Patrick kể về nhà chọc trời
        a = clamp((lt - 13.2) / 0.8) * (0.85 - 0.4 * clamp((lt - 19) / 2))
        c.saveLayerAlpha(None, int(255 * a))
        c.drawCircle(1500, 250, 190, P("#FFFFFF", 220)); c.drawCircle(1500, 250, 190, P(INK, stroke=5))
        skyline(c, 1500, 350, 0.36)
        c.restore()


# ================================================================ F. Bình minh, Carpathia, New York, kết (337,2 – 404,25)
def f_carpathia(c, t):                 # 337,2–349,66  trời hửng sáng · có ai hét lên · tàu Carpathia lao qua vùng băng tới cứu
    lt = t - 337.2
    q = ease_shot(t, 337.2, 349.66)
    K = Cam(lerp(960, 1200, q), 540, lerp(1.1, 1.0, q), t=t)
    sea_bg(c, K, t, night=1.0, dawn=clamp(lt / 6.0), calm=True)
    K.layer(c, 0.6)
    for k, (x, s) in enumerate([(300, 0.25), (900, 0.18), (1650, 0.3)]):
        iceberg(c, x, 640, s, night=0.3)
    cx = lerp(2300, 1500, ease_out(clamp((lt - 2.0) / 9.0)))
    c.save(); c.translate(cx, 650); c.scale(0.32, 0.32)     # Carpathia: một ống khói đỏ-đen, nhỏ hơn Titanic
    hull = skia.Path(); hull.moveTo(-800, -200); hull.lineTo(700, -200); hull.lineTo(820, -240); hull.lineTo(760, 40); hull.quadTo(600, 110, 300, 110)
    hull.lineTo(-700, 110); hull.quadTo(-820, 70, -820, -60); hull.close()
    fo(c, hull, "#1E1E22", ow=8)
    fo(c, rect(-500, -330, 900, 130), "#F2EEE4", ow=6)
    fun = skia.Path(); fun.moveTo(-60, -330); fun.lineTo(-40, -620); fun.lineTo(60, -620); fun.lineTo(80, -330); fun.close()
    fo(c, fun, "#C8502A", ow=7); c.drawRect(skia.Rect.MakeXYWH(-42, -620, 102, 60), P("#1A1A1A"))
    for k in range(4):
        q2 = (t * 0.25 + k / 4) % 1
        c.drawCircle(10 + q2 * 300, -660 - q2 * 200, 50 + q2 * 80, blur("#CFCAC0", 170 * (1 - q2), 14))
    c.drawLine(-650, -330, -650, -800, P(INK, stroke=10)); c.drawLine(600, -330, 600, -800, P(INK, stroke=10))
    c.restore()
    K.end(c)
    K.layer(c, 1.0)
    c.save(); c.translate(600, GROUND + 90)
    hull = skia.Path(); hull.moveTo(-320, 0); hull.quadTo(0, -110, 320, 0); hull.close()
    fo(c, hull, "#E8E4DA", ow=7)
    c.restore()
    ST(c, "pax0", 520, GROUND + 40, 0.6, t, face=1, hand_f=(80, -230) if lt > 0.3 else (60, 60), eyes="wide", mouth="open" if lt < 2.6 else "flat")
    YOU(c, 620, GROUND + 36, 0.6, t, face=1, eyes="wide", look=(1, 0), mouth="o", cap="", shiver=0.4)
    PAT(c, 710, GROUND + 40, 0.64, t, face=1, eyes="happy", mouth="grin", hand_f=(80, -200) if lt > 4 else (60, 60))
    wave_band(c, GROUND + 75, t * 0.4, lerp_col("#0E1830", "#6A6070", clamp(lt / 6.0)), amp=6, x0=-4000, x1=W + 4000, a=235)
    K.end(c)


def f_blanket(c, t):                   # 349,66–360,53  quấn chăn len, run không cầm nổi cốc · đi tìm từng khuôn mặt
    lt = t - 349.66
    if t < 354.48:
        q = ease_shot(t, 349.66, 354.48)
        K = Cam(1000, lerp(470, 460, q), lerp(2.0, 2.2, q), t=t)
        deck_bg(c, K, t, night=0.0)
        K.layer(c, 1.0)
        YOU(c, 1000, GROUND, ADULT, t, face=1, sit=1.0, hand_f=(110, 40), hand_b=(80, 50), shiver=1.0, eyes="dot", mouth="wobble", cap="", shawl="#8A7A6A")
        fo(c, rrect(1000 + ADULT * 120, GROUND - ADULT * 300, 40, 50, 8), "#F2EEE4", ow=4)
        for k in range(3):
            qq = (t * 0.6 + k / 3) % 1
            c.drawCircle(1000 + ADULT * 140 + 10 * math.sin(qq * 6), GROUND - ADULT * 320 - qq * 80, 10 + qq * 14, blur("#FFFFFF", 160 * (1 - qq), 6))
        K.end(c)
        return
    q = ease_shot(t, 354.48, 360.53)
    K = Cam(lerp(600, 1400, q), 540, 1.2, t=t)
    deck_bg(c, K, t, night=0.0)
    K.layer(c, 1.0)
    for i, who in enumerate(["paxw0", "pax1", "paxw2", "pax3", "paxw4", "paxw1"]):
        ST(c, who, 300 + i * 300, GROUND, 0.88, t + i, face=-1 if i % 2 else 1, sit=1.0 if i % 2 else 0.0, eyes="dot", mouth="flat", shawl="#8A7A6A")
    YOU(c, 400 + (t - 354.48) * 180, GROUND + 80, ADULT, t, face=1, walk=(t - 354.48) * 4, eyes="dot", look=(math.sin(t * 2), 0), mouth="flat",
        cap="", shawl="#8A7A6A")
    K.end(c)


def f_reunion(c, t):                   # 360,53–372,4  chiếc khăn quen · Nora quay lại · ôm nhau khóc · tràng hạt còn nguyên
    lt = t - 360.53
    if t < 365.11:
        q = ease_shot(t, 360.53, 365.11)
        K = Cam(lerp(1300, 1420, q), lerp(480, 440, q), lerp(1.8, 2.4, q), t=t)
        deck_bg(c, K, t, night=0.0)
        K.layer(c, 1.0)
        NORA(c, 1450, GROUND, 0.82, t, face=1, eyes="dot", look=(1, 0), mouth="flat", scarf="#C04A3A", shawl="#8A7A6A")
        YOU(c, 900, GROUND, ADULT, t, face=1, eyes="wide", look=(1, 0), mouth="o", cap="", shawl="#8A7A6A")
        K.end(c)
        return
    if t < 369.64:
        q = ease_shot(t, 365.11, 369.64)
        run = ease_out(clamp((t - 365.5) / 1.2))
        K = Cam(lerp(1180, 1200, q), 470, lerp(1.9, 2.1, q), t=t)
        deck_bg(c, K, t, night=0.0)
        K.layer(c, 1.0)
        hug = run > 0.95
        YOU(c, lerp(900, 1130, run), GROUND, ADULT, t, face=1, walk=None if hug else t * 7, hand_f=(150, -40) if hug else None,
            hand_b=(140, -20) if hug else None, eyes="closed" if hug else "wide", mouth="wobble" if hug else "o", tears=1.0 if hug else 0, cap="", shawl="#8A7A6A")
        NORA(c, 1280, GROUND, 0.82, t, face=-1, hand_f=(150, -60) if hug else (40, 60), hand_b=(140, -40) if hug else (20, 70),
             eyes="closed" if hug else "wide", mouth="wobble", tears=1.0, scarf="#C04A3A", shawl="#8A7A6A")
        K.end(c)
        return
    q = ease_shot(t, 369.64, 372.4)    # cận bàn tay với chuỗi tràng hạt
    grad(c, skia.Rect.MakeWH(W, H), "#C8B898", "#A8987A")
    c.save(); c.translate(W / 2, H / 2 + 40); c.scale(lerp(1.0, 1.1, q), lerp(1.0, 1.1, q))
    c.drawCircle(0, 0, 150, P("#1A1A1A"))
    for k in range(24):
        a = k * 2 * math.pi / 24
        c.drawCircle(220 * math.cos(a) * 0.9, 120 * math.sin(a) + 60, 16, P("#6A3A2A")); c.drawCircle(220 * math.cos(a) * 0.9, 120 * math.sin(a) + 60, 16, P(INK, stroke=3))
    c.drawLine(0, 180, 0, 320, P("#6A3A2A", stroke=10)); c.drawLine(-40, 250, 40, 250, P("#6A3A2A", stroke=10))
    c.restore()


def f_newyork(c, t):                   # 372,4–386,92  New York mưa tầm tã · không ai đón · ngước nhìn nhà chọc trời · cuộc đời mới
    lt = t - 372.4
    q = ease_shot(t, 372.4, 386.92)
    K = Cam(lerp(800, 1100, q), lerp(560, 460, q), lerp(1.05, 1.2, q), t=t)
    K.layer(c, 0.0)
    grad(c, skia.Rect.MakeXYWH(-3000, -3000, W + 6000, H + 6000), "#3A4252", "#6A7080")
    K.end(c)
    K.layer(c, 0.4)
    skyline(c, 1200, 700, 1.3, col="#2A303C")
    K.end(c)
    K.layer(c, 1.0)
    c.drawRect(skia.Rect.MakeXYWH(-3000, GROUND, W + 6000, 900), P("#4A4A52"))
    for i in range(9):
        x = 200 + i * 220
        if i in (4, 5):
            continue
        ST(c, f"pax{i % 5}" if i % 2 else f"paxw{i % 5}", x, GROUND - 10, 0.8, t + i, face=1 if i < 4 else -1, eyes="dot", mouth="flat", idle=0.6)
        c.drawArc(skia.Rect.MakeXYWH(x - 90, GROUND - 0.8 * 560, 180, 120), 180, 180, True, P("#1A1A22"))
    YOU(c, 1060, GROUND + 80, ADULT, t, face=1, hand_b=(-120, 60), eyes="dot", look=(0.3, -1) if lt > 6 else (0, 0), mouth="smile" if lt > 9 else "flat", cap="")
    NORA(c, 900, GROUND + 80, 0.82, t, face=1, hand_f=(120, 60), eyes="dot", look=(0.3, -1) if lt > 6 else (0, 0), mouth="smile" if lt > 9 else "flat",
         scarf="#C04A3A")
    K.end(c)
    for k in range(80):   # mưa
        x = (k * 97 + t * 200) % (W + 200) - 100; y = (k * 173 + t * 1400) % (H + 200) - 100
        c.drawLine(x, y, x - 8, y + 34, P("#C8D0E0", 130, stroke=2))


def f_stats(c, t):                     # 386,92–394,37  hơn 1.500 người không trở về · hạng ba: cứ bốn người chỉ một người sống sót
    lt = t - 386.92
    grad(c, skia.Rect.MakeWH(W, H), "#0E121C", "#05070C")
    p = back_out(clamp(lt / 0.5))
    c.save(); c.translate(W / 2, 330); c.scale(p, p)
    text(c, "1.500+", 0, 0, "xbold", 170, "#E8E2D2", align="center")
    c.restore()
    if t > 390.15:
        a = clamp((t - 390.15) / 0.5)
        for i in range(4):
            x = W / 2 - 360 + i * 240; y = 720
            col = "#F2EEE4" if i == 0 else "#3A4050"
            c.drawCircle(x, y - 90, 44, P(col, 255 * a)); c.drawLine(x, y - 46, x, y + 60, P(col, 255 * a, stroke=16))
            c.drawLine(x - 60, y, x + 60, y, P(col, 255 * a, stroke=14))
        label(c, "Hạng ba: cứ 4 người, chỉ khoảng 1 người sống sót", W / 2, 860, 52, "#F4C430", a=255 * a)


def f_promise(c, t):                   # 394,37–396,64  bạn đã giữ được lời hứa với mẹ
    a = clamp((t - 394.37) / 0.4)
    c.saveLayerAlpha(None, int(255 * a))
    b_goodbye(c, 56.5 + (t - 394.37) * 0.6)
    c.restore()


def f_question(c, t):                  # 396,64–404,25  câu hỏi cuối
    lt = t - 396.64
    q = ease_shot(t, 396.64, 404.25)
    K = Cam(960, 540, lerp(1.0, 1.06, q), t=t)
    sea_bg(c, K, t, night=1.0, calm=True)
    sea_front(c, K, t, night=1.0, calm=True, y=880)
    al = 255 * clamp((lt - 0.4) / 0.6)
    text(c, "Nếu là bạn, đứng trên boong tàu đêm hôm ấy,", W / 2, 400, "xbold", 58, "#F2E8D0", a=al, align="center")
    text(c, "bạn sẽ bước lên chiếc xuồng cứu sinh,", W / 2, 490, "xbold", 58, "#F2E8D0", a=al, align="center")
    text(c, "hay sẽ nhường chỗ cho người khác?", W / 2, 580, "xbold", 58, "#F4C430", a=255 * clamp((lt - 2.0) / 0.6), align="center")


SHOTS = [(0.0, 8.5, a_field), (8.5, 14.0, a_hearth), (14.0, 19.75, a_letters), (19.75, 27.68, a_america), (27.68, 37.53, a_tickets),
         (37.53, 48.66, a_poster), (48.66, 63.8, b_goodbye), (63.8, 69.82, b_tender), (69.82, 79.56, b_reveal), (79.56, 92.11, b_inspect),
         (92.11, 98.45, c_bulb), (98.45, 105.67, c_meal), (105.67, 112.82, c_dance), (112.82, 125.58, c_patrick), (125.58, 139.34, c_night),
         (139.34, 151.5, c_impact), (151.5, 166.91, c_ice), (166.91, 180.62, d_water), (180.62, 196.25, d_crowd), (196.25, 208.29, d_find),
         (208.29, 223.23, d_deck), (223.23, 240.66, d_part), (240.66, 250.51, d_lower),
         (250.51, 257.02, e_tilt), (257.02, 264.05, e_band), (264.05, 275.59, e_stern), (275.59, 284.28, e_break), (284.28, 286.51, e_jump),
         (286.51, 302.06, e_water), (302.06, 315.85, e_overturned), (315.85, 337.2, e_balance),
         (337.2, 349.66, f_carpathia), (349.66, 360.53, f_blanket), (360.53, 372.4, f_reunion), (372.4, 386.92, f_newyork),
         (386.92, 394.37, f_stats), (394.37, 396.64, f_promise), (396.64, DUR, f_question)]
FADE = {48.66, 92.11, 125.58, 250.51, 337.2, 372.4, 386.92}
NO_SUB_FROM = 396.64
