#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page as a 1024x1024 PNG.

The picture is a broadsheet front page: a deep-teal masthead, one lead
story with a small tariff comparison chart, then five numbered stories in
a two-column grid, and a dateline footer. It writes the finished poster to
/output/entry.png and also leaves a copy next to this file.
"""

import os
import stat

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024

PAPER = (247, 239, 224)      # warm cream newsprint
INK = (26, 26, 24)           # near-black text
TEAL = (12, 68, 64)          # deep teal masthead
TEAL_SOFT = (31, 96, 90)     # lighter teal for rules
ORANGE = (217, 93, 57)       # burnt-orange accent
GOLD = (201, 162, 39)        # gold rule
CARD = (255, 253, 246)       # story card paper
CARD_EDGE = (217, 205, 178)  # card border
MUTED = (96, 88, 74)         # secondary text

SERIF_B = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
SANS_B = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SANS_R = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"


def load(size, path):
    """Load a truetype font at the requested size."""
    return ImageFont.truetype(path, size)


def split_to_width(draw, text, font, limit):
    """Break text into lines that fit inside limit pixels, char by char."""
    rows = []
    current = ""
    for ch in text:
        trial = current + ch
        if draw.textlength(trial, font=font) <= limit:
            current = trial
        else:
            if current:
                rows.append(current)
            current = ch
    if current:
        rows.append(current)
    return rows


def paragraph(draw, text, font, x, y, limit, leading, colour):
    """Draw wrapped text starting at (x, y); return the y below it."""
    for row in split_to_width(draw, text, font, limit):
        draw.text((x, y), row, font=font, fill=colour)
        y += leading
    return y


def masthead(canvas):
    """Paint the teal banner with the paper name, date and strapline."""
    pen = ImageDraw.Draw(canvas)
    pen.rectangle([0, 0, SIDE, 138], fill=TEAL)
    pen.rectangle([0, 138, SIDE, 145], fill=GOLD)
    big = load(62, SERIF_B)
    pen.text((38, 20), "世界头版", font=big, fill=(255, 250, 238))
    date_font = load(30, SANS_B)
    stamp = "26 NOV 2026"
    pen.text((SIDE - 38 - pen.textlength(stamp, font=date_font), 30),
             stamp, font=date_font, fill=GOLD)
    sub = load(20, SANS_R)
    pen.text((40, 100), "THE WORLD IN ONE PAGE  ·  一天六条世界新闻",
             font=sub, fill=(216, 201, 163))
    weekday = load(20, SANS_B)
    tag = "星期四  THURSDAY"
    pen.text((SIDE - 38 - pen.textlength(tag, font=weekday), 100),
             tag, font=weekday, fill=(216, 201, 163))


def tariff_chart(pen, x0, y0, x1, y1):
    """Draw two bars comparing the 25% tariff with the 17% deal rate."""
    pen.rectangle([x0, y0, x1, y1], fill=CARD, outline=CARD_EDGE, width=2)
    head = load(19, SANS_B)
    pen.text((x0 + 18, y0 + 14), "关税税率  TARIFF RATE", font=head, fill=TEAL)
    base = y1 - 52
    top25 = base - 138
    top17 = base - 94
    bar_w = 74
    left25 = x0 + 52
    left17 = x0 + 196
    pen.rectangle([left25, top25, left25 + bar_w, base], fill=ORANGE)
    pen.rectangle([left17, top17, left17 + bar_w, base], fill=TEAL_SOFT)
    pen.line([x0 + 24, base, x1 - 24, base], fill=MUTED, width=2)
    pct = load(30, SANS_B)
    pen.text((left25 + 4, top25 - 40), "25%", font=pct, fill=ORANGE)
    pen.text((left17 + 4, top17 - 40), "17%", font=pct, fill=TEAL)
    lab = load(18, SANS_R)
    pen.text((left25 - 8, base + 10), "拟加征", font=lab, fill=INK)
    pen.text((left17 - 8, base + 10), "达成协议后", font=lab, fill=INK)


def lead_story(pen):
    """Paint the lead story: kicker, headline, deck and the chart."""
    kicker = load(22, SANS_B)
    pen.text((40, 168), "头条  TOP STORY  ·  贸易 TRADE", font=kicker,
             fill=ORANGE)
    title = load(46, SERIF_B)
    y = paragraph(pen, "美国拟对印度商品加征 25% 关税", title,
                  40, 202, 580, 58, INK)
    body = load(24, SANS_R)
    paragraph(pen, "若两国达成贸易协议，税率可降至 17%。",
              body, 40, y + 8, 580, 34, MUTED)
    tariff_chart(pen, 652, 168, 986, 440)
    pen.line([40, 458, 984, 458], fill=TEAL, width=3)
    pen.line([40, 464, 984, 464], fill=GOLD, width=1)


def story_card(pen, x0, y0, x1, y1, number, kicker, headline, deck):
    """Paint one numbered story card inside the given rectangle."""
    pen.rectangle([x0, y0, x1, y1], fill=CARD, outline=CARD_EDGE, width=2)
    pen.rectangle([x0, y0, x0 + 7, y1], fill=ORANGE if number % 2 else TEAL)
    num_font = load(26, SANS_B)
    badge = 40
    cx = x0 + 26
    cy = y0 + 22
    pen.ellipse([cx, cy, cx + badge, cy + badge], fill=TEAL)
    digit = str(number)
    tw = pen.textlength(digit, font=num_font)
    pen.text((cx + (badge - tw) / 2, cy + 5), digit, font=num_font,
             fill=(255, 250, 238))
    kick = load(17, SANS_B)
    pen.text((cx + badge + 12, cy + 10), kicker, font=kick, fill=ORANGE)
    head = load(27, SANS_B)
    y = paragraph(pen, headline, head, x0 + 26, y0 + 74,
                  x1 - x0 - 52, 36, INK)
    deck_font = load(20, SANS_R)
    paragraph(pen, deck, deck_font, x0 + 26, y + 4,
              x1 - x0 - 52, 28, MUTED)


def grid(pen):
    """Lay out the five remaining stories in a two-column grid."""
    stories = [
        (2, "英伟达  NVIDIA",
         "特朗普称可能赦免黄仁勋",
         "称自己促成黄仁勋回归英伟达；万斯公开为黄仁勋辩护。"),
        (3, "中东  MIDDLE EAST",
         "胡塞武装再袭利雅得",
         "霍尔木兹海峡油轮遇袭，伊朗称触水雷。"),
        (4, "安全  SECURITY",
         "北约加强东翼空中监视",
         "导弹坠落后东翼戒备升级；俄军机接近，韩国发布疏散警告。"),
        (5, "太空  SPACE",
         "首位外籍宇航员登上中国空间站",
         "巴基斯坦宇航员搭乘神舟二十四号升空。"),
        (6, "板球  CRICKET",
         "15 岁印度新星 53 球轰下 204 分",
         "Vaibhav Sooryavanshi 对阵阿联酋，创世界纪录。"),
    ]
    col_w = 462
    row_h = 152
    gap = 14
    top = 482
    positions = [
        (40, top),
        (522, top),
        (40, top + row_h + gap),
        (522, top + row_h + gap),
        (40, top + 2 * (row_h + gap)),
    ]
    for (number, kicker, headline, deck), (x0, y0) in zip(stories, positions):
        x1 = x0 + col_w if number != 6 else 984
        story_card(pen, x0, y0, x1, y0 + row_h, number, kicker, headline,
                   deck)


def footer(pen):
    """Paint the dateline strip along the bottom edge."""
    pen.line([40, 962, 984, 962], fill=CARD_EDGE, width=2)
    foot = load(19, SANS_R)
    line = "2026 年 11 月 26 日 星期四  ·  SIX STORIES  ·  NEWS-IMAGE-20261126"
    tw = pen.textlength(line, font=foot)
    pen.text(((SIDE - tw) / 2, 974), line, font=foot, fill=MUTED)


def build_poster():
    """Compose the whole front page and return the image."""
    canvas = Image.new("RGB", (SIDE, SIDE), PAPER)
    pen = ImageDraw.Draw(canvas)
    masthead(canvas)
    lead_story(pen)
    grid(pen)
    footer(pen)
    return canvas


def save_copy(image, path):
    """Save the poster and make it world-readable (mode 0644)."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    image.save(path, format="PNG")
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP
             | stat.S_IROTH)


def main():
    poster = build_poster()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    save_copy(poster, os.path.join(out_dir, "entry.png"))
    save_copy(poster, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "entry.png"))
    print("wrote entry.png (1024x1024)")


if __name__ == "__main__":
    main()
