"""Compose Naya Nagrik carousel slides (1080x1350) from raw panels + text."""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
SAFFRON = (255, 153, 51)
GREEN = (19, 136, 8)
NAVY = (27, 42, 74)
OFFWHITE = (250, 247, 240)
RED = (200, 70, 60)

GF = "/usr/share/fonts/truetype/google-fonts/"
F_HOOK = GF + "Poppins-Bold.ttf"
F_BODY = GF + "Poppins-Medium.ttf"
F_SMALL = GF + "Poppins-Medium.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=fnt) <= max_w:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def fit_panel(path):
    im = Image.open(path).convert("RGB")
    scale = W / im.width
    im = im.resize((W, int(im.height * scale)), Image.LANCZOS)
    if im.height >= H:
        top = int((im.height - H) * 0.35)
        im = im.crop((0, top, W, top + H))
    else:
        bg = Image.new("RGB", (W, H), OFFWHITE)
        bg.paste(im, (0, (H - im.height) // 2))
        im = bg
    return im


def pill(draw, xy, text, fnt, fill, color, pad=(22, 10), anchor="lt"):
    x, y = xy
    tw = draw.textlength(text, font=fnt)
    asc, desc = fnt.getmetrics()
    w, h = tw + pad[0] * 2, asc + desc + pad[1] * 2
    if anchor == "rb":
        x, y = x - w, y - h
    draw.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=fill)
    draw.text((x + pad[0], y + pad[1]), text, font=fnt, fill=color)


def text_card(img, title, body, hook=False, accent=SAFFRON, y=95):
    d = ImageDraw.Draw(img, "RGBA")
    max_w = W - 2 * 70 - 2 * 40
    ft = font(F_HOOK, 74 if hook else 52)
    fb = font(F_BODY, 38)
    tl = wrap(d, title, ft, max_w) if title else []
    bl = wrap(d, body, fb, max_w) if body else []
    lh_t, lh_b = int(ft.size * 1.22), int(fb.size * 1.38)
    h = 40 * 2 + len(tl) * lh_t + len(bl) * lh_b + (16 if tl and bl else 0)
    x0, x1 = 70, W - 70
    # soft shadow
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x0 + 6, y + 10, x1 + 6, y + h + 10), 34, fill=(0, 0, 0, 70))
    img.paste(Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(10))).convert("RGB"))
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((x0, y, x1, y + h), 34, fill=OFFWHITE + (246,))
    d.rounded_rectangle((x0, y, x0 + 14, y + h), 7, fill=accent)
    cy = y + 40
    for ln in tl:
        d.text((x0 + 50, cy), ln, font=ft, fill=NAVY)
        cy += lh_t
    if tl and bl:
        cy += 16
    for ln in bl:
        d.text((x0 + 50, cy), ln, font=fb, fill=NAVY)
        cy += lh_b
    return img


def bg_ok(img):
    r, g, b = img.getpixel((90, 50))[:3]
    return not (r > 230 and 130 < g < 180 and b < 90)


def chrome(img, series, idx, total, handle="@naya.nagrik"):
    d = ImageDraw.Draw(img, "RGBA")
    fs = font(F_SMALL, 28)
    pill(d, (70, 34), series, fs, SAFFRON if bg_ok(img) else OFFWHITE, NAVY)
    pill(d, (W - 70, H - 40), handle, fs, NAVY + (225,), OFFWHITE, anchor="rb")
    pill(d, (70, H - 40 - 54), f"{idx}/{total}", fs, OFFWHITE + (225,), NAVY)
    if idx < total:
        # swipe hint arrow
        d.text((W - 70 - 50, H // 2 - 40), "›", font=font(F_HOOK, 90), fill=OFFWHITE + (200,))
    return img


def cta_slide(lines, faces, series, idx, total):
    img = Image.new("RGB", (W, H), OFFWHITE)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 420), fill=SAFFRON)
    x = W // 2 - 360
    for f in faces:
        fc = Image.open(f).convert("RGBA").resize((330, 330), Image.LANCZOS)
        m = Image.new("L", fc.size, 0)
        ImageDraw.Draw(m).ellipse((0, 0, 330, 330), fill=255)
        ring = Image.new("RGBA", (350, 350), OFFWHITE + (255,))
        rm = Image.new("L", (350, 350), 0)
        ImageDraw.Draw(rm).ellipse((0, 0, 350, 350), fill=255)
        img.paste(ring, (x - 10, 240), rm)
        img.paste(fc, (x, 250), m)
        x += 390
    ft, fb = font(F_HOOK, 84), font(F_BODY, 46)
    y = 700
    for i, ln in enumerate(lines):
        f = ft if i == 0 else fb
        for w in wrap(d, ln, f, W - 160):
            tw = d.textlength(w, font=f)
            d.text(((W - tw) / 2, y), w, font=f, fill=NAVY if i else GREEN)
            y += int(f.size * 1.3)
        y += 24
    d.rectangle((0, H - 130, W, H), fill=GREEN)
    return chrome(img, series, idx, total)


def text_slide(title, body, kind, series, idx, total, small="", label=None):
    bg = {"rule": GREEN, "fact": NAVY, "mirror": SAFFRON, "plain": OFFWHITE}[kind]
    fg = OFFWHITE if kind in ("rule", "fact") else NAVY
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    # decorative corner circles
    d.ellipse((W - 260, -140, W + 140, 260), fill=tuple(min(255, c + 25) for c in bg))
    d.ellipse((-160, H - 300, 220, H + 80), fill=tuple(max(0, c - 20) for c in bg))
    label = {"rule": "RULE OF THUMB", "fact": "KYUN ZAROORI HAI?", "mirror": "BHARAT MEIN PEHLE SE", "plain": ""}[kind] if label is None else label
    ft, fb, fl = font(F_HOOK, 76), font(F_BODY, 44), font(F_HOOK, 30)
    tl = wrap(d, title, ft, W - 180) if title else []
    bl = wrap(d, body, fb, W - 180) if body else []
    total_h = 60 + len(tl) * int(ft.size * 1.2) + 40 + len(bl) * int(fb.size * 1.4)
    y = (H - total_h) // 2 - 40
    if label:
        d.text((90, y), label, font=fl, fill=fg)
    y += 70
    for ln in tl:
        d.text((90, y), ln, font=ft, fill=fg); y += int(ft.size * 1.2)
    y += 40
    for ln in bl:
        d.text((90, y), ln, font=fb, fill=fg); y += int(fb.size * 1.4)
    if small:
        fs = font(F_SMALL, 26)
        d.text((90, H - 190), small, font=fs, fill=fg)
    return chrome(img, series, idx, total)


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    out = spec["out"]
    os.makedirs(out, exist_ok=True)
    total = len(spec["slides"])
    for i, s in enumerate(spec["slides"], 1):
        if s.get("type") == "text":
            img = text_slide(s.get("title",""), s.get("body",""), s.get("kind","plain"), spec["series"], i, total, s.get("small",""), s.get("label"))
        elif s.get("type") == "cta":
            img = cta_slide(s["lines"], s["faces"], spec["series"], i, total)
        else:
            img = fit_panel(s["panel"])
            img = text_card(img, s.get("title", ""), s.get("body", ""), hook=(i == 1),
                            accent=GREEN if s.get("rule") else (RED if s.get("mistake") else SAFFRON),
                            y=s.get("y", 118))
            img = chrome(img, spec["series"], i, total)
        p = os.path.join(out, f"{spec['slug']}_{i:02d}.jpg")
        img.save(p, quality=92)
        print(p)
