#!/usr/bin/env python3
"""The World in One Day - a newspaper front page summing up 26 Nov 2026.

Pure stdlib Python (zlib, struct, binascii, os). Renders a 1024x1024 PNG
with a hand-drawn 5x7 bitmap font and simple vector shapes. Deterministic:
no clock, no randomness, no network. Run: python3 main.py
Output: $MAKEFUN_OUTPUT_DIR/entry.png (default ./out/entry.png).
"""
import binascii
import os
import struct
import zlib

W, H = 1024, 1024

# --- palette (newsprint) ---
PAPER = (246, 241, 229)
INK = (24, 22, 18)
RED = (178, 34, 34)
BLUE = (31, 68, 120)
GOLD = (198, 148, 44)
GREEN = (46, 110, 62)
GREY = (120, 116, 108)
LIGHT = (232, 226, 210)
DARKBLUE = (18, 38, 66)
ORANGE = (214, 110, 36)

# --- 5x7 bitmap font: each glyph is 7 rows of 5 bits ---
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '#': ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '*': ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '_': ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    '<': ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    '>': ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
}

# --- canvas ---
px = bytearray(W * H * 3)


def set_px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        px[i], px[i + 1], px[i + 2] = c


def fill_rect(x, y, w, h, c):
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    for yy in range(y0, y1):
        base = (yy * W + x0) * 3
        for xx in range(x0, x1):
            i = base + (xx - x0) * 3
            px[i], px[i + 1], px[i + 2] = c


def hline(x, y, w, c):
    fill_rect(x, y, w, 1, c)


def vline(x, y, h, c):
    fill_rect(x, y, 1, h, c)


def line(x0, y0, x1, y1, c):
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        set_px(x0, y0, c)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def disc(cx, cy, r, c):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                set_px(xx, yy, c)


def ring(cx, cy, r, t, c):
    for yy in range(cy - r - t, cy + r + t + 1):
        for xx in range(cx - r - t, cx + r + t + 1):
            d2 = (xx - cx) ** 2 + (yy - cy) ** 2
            if (r - t) ** 2 <= d2 <= (r + t) ** 2:
                set_px(xx, yy, c)


def tri(x0, y0, x1, y1, x2, y2, c):
    pts = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
    (ax, ay), (bx, by), (cx, cy) = pts
    for y in range(ay, cy + 1):
        if y < by:
            t = 0 if by == ay else (y - ay) / (by - ay)
            xa = ax + (bx - ax) * t
        else:
            t = 0 if cy == by else (y - by) / (cy - by)
            xa = bx + (cx - bx) * t
        t2 = 0 if cy == ay else (y - ay) / (cy - ay)
        xb = ax + (cx - ax) * t2
        for x in range(int(min(xa, xb)), int(max(xa, xb)) + 1):
            set_px(x, y, c)


# --- text ---
def glyph(ch):
    return FONT.get(ch.upper(), FONT['?'])


def text_w(s, sc):
    return len(s) * 6 * sc - sc


def draw_text(x, y, s, sc, c):
    cx = x
    for ch in s:
        g = glyph(ch)
        for row in range(7):
            bits = g[row]
            for col in range(5):
                if bits[col] == '1':
                    fill_rect(cx + col * sc, y + row * sc, sc, sc, c)
        cx += 6 * sc
    return cx


def wrap(s, maxw, sc):
    words = s.split(' ')
    lines, cur = [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if text_w(t, sc) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_para(x, y, s, maxw, sc, c, lh=None):
    lh = lh or int(9 * sc)
    yy = y
    for ln in wrap(s, maxw, sc):
        draw_text(x, yy, ln, sc, c)
        yy += lh
    return yy


# --- icons (drawn inside a box x, y, w, h) ---
def icon_rocket(x, y, w, h):
    # deep-space panel, ringed station + rocket
    fill_rect(x, y, w, h, DARKBLUE)
    for (sx, sy) in [(x + 18, y + 16), (x + w - 26, y + 30), (x + 40, y + h - 24),
                     (x + w - 44, y + h - 18), (x + w // 2, y + 12)]:
        disc(sx, sy, 2, PAPER)
    cx, cy = x + w // 2, y + h // 2 + 6
    # station ring (tilted ellipse approximated by two rings)
    ring(cx, cy, 46, 3, GOLD)
    ring(cx, cy, 30, 2, GOLD)
    disc(cx, cy, 16, PAPER)
    disc(cx - 5, cy - 5, 5, LIGHT)
    # solar panels: solid gold bars flanking the ring
    fill_rect(cx - 92, cy - 7, 40, 14, GOLD)
    fill_rect(cx + 52, cy - 7, 40, 14, GOLD)
    fill_rect(cx - 92, cy - 7, 40, 3, INK)
    fill_rect(cx + 52, cy - 7, 40, 3, INK)
    # rocket rising top-right
    rx, ry = x + w - 52, y + 26
    tri(rx, ry - 22, rx - 10, ry + 6, rx + 10, ry + 6, RED)
    fill_rect(rx - 10, ry + 6, 20, 26, PAPER)
    tri(rx - 10, ry + 32, rx - 18, ry + 44, rx - 10, ry + 32, RED)
    tri(rx + 10, ry + 32, rx + 18, ry + 44, rx + 10, ry + 32, RED)
    tri(rx - 5, ry + 32, rx + 5, ry + 32, rx, ry + 48, ORANGE)
    disc(rx, ry + 14, 4, BLUE)


def icon_chart(x, y, w, h):
    fill_rect(x, y, w, h, LIGHT)
    # axes
    vline(x + 14, y + 12, h - 28, INK)
    hline(x + 14, y + h - 16, w - 28, INK)
    # rising bars
    bars = [22, 34, 30, 46, 58, 74]
    bw = (w - 40) // len(bars)
    for i, bh in enumerate(bars):
        bx = x + 22 + i * bw
        fill_rect(bx, y + h - 16 - bh, bw - 6, bh, BLUE if i < 5 else RED)
    # trend arrow
    line(x + 20, y + h - 40, x + w - 20, y + 18, RED)
    tri(x + w - 20, y + 18, x + w - 34, y + 16, x + w - 20, y + 30, RED)


def icon_candle(x, y, w, h):
    fill_rect(x, y, w, h, (32, 28, 30))
    cx = x + w // 2
    # big 500K marker above the flame
    draw_text(cx - text_w("500K", 3) // 2, y + 4, "500K", 3, GOLD)
    # flame
    disc(cx, y + 36, 6, ORANGE)
    tri(cx - 5, y + 36, cx + 5, y + 36, cx, y + 24, GOLD)
    # candle body
    fill_rect(cx - 10, y + 42, 20, 24, PAPER)
    fill_rect(cx - 10, y + 42, 20, 4, GOLD)
    # base
    fill_rect(cx - 26, y + h - 6, 52, 4, GOLD)
    # two small stars of remembrance
    disc(x + 18, y + h - 16, 2, PAPER)
    disc(x + w - 18, y + 30, 2, PAPER)


def icon_dove(x, y, w, h):
    fill_rect(x, y, w, h, (214, 232, 240))
    cx, cy = x + w // 2 - 10, y + h // 2
    # body
    disc(cx, cy, 26, PAPER)
    fill_rect(cx - 26, cy - 8, 52, 26, PAPER)
    # head + beak
    disc(cx + 26, cy - 18, 11, PAPER)
    tri(cx + 35, cy - 20, cx + 48, cy - 14, cx + 35, cy - 12, ORANGE)
    disc(cx + 29, cy - 21, 2, INK)
    # raised wing
    tri(cx - 18, cy - 6, cx - 2, cy - 52, cx + 14, cy - 8, PAPER)
    line(cx - 2, cy - 52, cx + 14, cy - 8, GREY)
    # tail feathers
    tri(cx - 26, cy + 4, cx - 58, cy + 26, cx - 24, cy + 16, PAPER)
    tri(cx - 26, cy + 8, cx - 56, cy + 38, cx - 22, cy + 18, PAPER)
    # olive sprig: stem + five leaves, held low
    line(cx + 30, cy + 20, cx + 70, cy + 32, GREEN)
    for i in range(5):
        lx = cx + 36 + i * 8
        ly = cy + 23 + i * 2
        disc(lx, ly - 3, 4, GREEN)
        disc(lx + 4, ly + 2, 4, GREEN)
    disc(cx + 70, cy + 32, 4, GREEN)


def icon_coin(x, y, w, h):
    fill_rect(x, y, w, h, (238, 226, 190))
    cx, cy = x + w // 2, y + h // 2 - 4
    disc(cx, cy, 30, GOLD)
    ring(cx, cy, 30, 2, INK)
    ring(cx, cy, 23, 2, INK)
    draw_text(cx - text_w("+36%", 2) // 2, cy - 7, "+36%", 2, INK)
    # small upward arrow under the coin
    line(cx - 14, y + h - 6, cx, y + h - 16, GREEN)
    line(cx, y + h - 16, cx + 14, y + h - 6, GREEN)
    tri(cx, y + h - 18, cx - 5, y + h - 11, cx + 5, y + h - 11, GREEN)


def icon_chess(x, y, w, h):
    # 6x6 board, white king on a dark square
    s = min(w, h) // 6
    ox, oy = x + (w - 6 * s) // 2, y + (h - 6 * s) // 2
    for r in range(6):
        for c in range(6):
            col = PAPER if (r + c) % 2 == 0 else INK
            fill_rect(ox + c * s, oy + r * s, s, s, col)
    # frame
    for i in range(3):
        fill_rect(ox - 3 + i, oy - 3 + i, 6 * s + 6 - 2 * i, 1, INK)
    # white king (row 1, col 4 -> dark square) with cross
    kx, ky = ox + 4 * s + s // 2, oy + 1 * s + s // 2
    disc(kx, ky + 2, s // 2, INK)
    disc(kx, ky + 2, s // 2 - 2, PAPER)
    fill_rect(kx - 2, ky - s // 2 - 1, 4, 8, PAPER)
    fill_rect(kx - 5, ky - s // 2 + 2, 10, 4, PAPER)
    # black pawn (row 4, col 1)
    px_, py_ = ox + 1 * s + s // 2, oy + 4 * s + s // 2
    disc(px_, py_ - 2, s // 3, INK)
    fill_rect(px_ - s // 3, py_ + 2, 2 * s // 3, s // 4, INK)


def icon_mercury(x, y, w, h):
    fill_rect(x, y, w, h, (20, 20, 28))
    cx, cy = x + w // 2 - 20, y + h // 2 + 4
    # Mercury: cratered grey disc
    disc(cx, cy, 30, (168, 160, 148))
    disc(cx - 9, cy - 8, 5, (120, 114, 104))
    disc(cx + 8, cy + 6, 7, (120, 114, 104))
    disc(cx + 11, cy - 12, 4, (140, 132, 122))
    disc(cx - 12, cy + 11, 3, (140, 132, 122))
    # BepiColombo probe approaching, gold panels
    px_, py_ = x + w - 58, y + 12
    fill_rect(px_, py_, 30, 10, GOLD)
    fill_rect(px_ + 7, py_ + 10, 16, 14, PAPER)
    line(px_ + 15, py_ + 24, cx + 24, cy - 14, GOLD)
    disc(px_ + 15, py_ + 5, 3, RED)
    # dashed 8-year path
    for i in range(6):
        disc(x + 14 + i * 12, y + h - 8, 2, GOLD)


def icon_quake(x, y, w, h):
    fill_rect(x, y, w, h, (240, 228, 208))
    cx = x + w // 2
    # shaking tower
    fill_rect(cx - 14, y + 18, 28, h - 52, INK)
    for i in range(4):
        fill_rect(cx - 14, y + 26 + i * 18, 28, 3, PAPER)
    tri(cx - 14, y + 18, cx + 14, y + 18, cx, y + 4, RED)
    # ground crack lines, kept below the tower base
    base = y + h - 30
    line(x + 8, base, x + w // 3, base + 8, RED)
    line(x + w // 3, base + 8, x + 2 * w // 3, base - 2, RED)
    line(x + 2 * w // 3, base - 2, x + w - 8, base + 8, RED)
    draw_text(x + 6, y + 4, "5.6", 2, RED)


# --- panels ---
def panel(x, y, w, h, kicker, headline, body, icon=None, kcolor=RED):
    fill_rect(x, y, w, h, PAPER)
    for i in range(2):
        hline(x, y + i, w, INK)
        hline(x, y + h - 1 - i, w, INK)
        vline(x + i, y, h, INK)
        vline(x + w - 1 - i, y, h, INK)
    draw_text(x + 12, y + 10, kicker, 2, kcolor)
    yy = draw_para(x + 12, y + 30, headline, w - 24, 3, INK, lh=24)
    if icon is not None:
        ih = 72
        icon(x + 12, yy + 4, w - 24, ih)
        draw_para(x + 12, yy + 4 + ih + 8, body, w - 24, 2, INK, lh=15)
    else:
        draw_para(x + 12, yy + 4, body, w - 24, 2, INK, lh=15)


def chunk_png():
    sig = b'\x89PNG\r\n\x1a\n'

    def ch(kind, data):
        c = struct.pack('>I', len(data)) + kind + data
        return c + struct.pack('>I', binascii.crc32(kind + data) & 0xFFFFFFFF)

    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    raw = b''.join(b'\x00' + bytes(px[y * W * 3:(y + 1) * W * 3])
                   for y in range(H))
    return sig + ch(b'IHDR', ihdr) + ch(b'IDAT', zlib.compress(raw, 9)) + ch(b'IEND', b'')


def build():
    fill_rect(0, 0, W, H, PAPER)
    # outer frame
    for i in range(4):
        hline(0, i, W, INK)
        hline(0, H - 1 - i, W, INK)
        vline(i, 0, H, INK)
        vline(W - 1 - i, 0, H, INK)

    # ---- masthead ----
    title = "THE WORLD IN ONE DAY"
    draw_text((W - text_w(title, 6)) // 2, 22, title, 6, INK)
    hline(24, 78, W - 48, INK)
    hline(24, 82, W - 48, INK)
    dateline = "THURSDAY 26 NOVEMBER 2026  -  ONE DAY, ONE PAGE, THE WHOLE WORLD"
    draw_text((W - text_w(dateline, 2)) // 2, 92, dateline, 2, GREY)
    hline(24, 112, W - 48, INK)

    # ---- lead story ----
    lx, ly, lw, lh = 24, 124, W - 48, 268
    fill_rect(lx, ly, lw, lh, PAPER)
    for i in range(2):
        hline(lx, ly + i, lw, INK)
        hline(lx, ly + lh - 1 - i, lw, INK)
        vline(lx + i, ly, lh, INK)
        vline(lx + lw - 1 - i, ly, lh, INK)
    draw_text(lx + 14, ly + 10, "LEAD  -  SPACE", 2, RED)
    head = "FIRST PAKISTANI ASTRONAUT REACHES CHINA'S SPACE STATION"
    draw_para(lx + 14, ly + 32, head, 560, 4, INK, lh=36)
    body = ("Muhammad Zeeshan Ali becomes the first foreign astronaut to "
            "visit Tiangong, flying aboard Shenzhou-24. A new chapter for "
            "Pakistan in space.")
    draw_para(lx + 14, ly + 150, body, 560, 2, INK, lh=17)
    draw_text(lx + 14, ly + 232, "BY THE WORLD DESK  -  BEIJING / GENEVA", 2, GREY)
    icon_rocket(lx + 600, ly + 12, lw - 614, lh - 24)

    # ---- row 1: USA / Russia / Colombia ----
    ry, rh = 404, 236
    pw = (W - 48 - 24) // 3
    panel(24, ry, pw, rh, "USA  -  TRADE",
          "US PREPARES NEW TARIFFS ON GLOBAL PARTNERS",
          "Washington readies a plan aimed at factory overcapacity.",
          icon_chart, BLUE)
    panel(24 + pw + 12, ry, pw, rh, "UKRAINE  -  THE TOLL",
          "RUSSIA'S OWN FIGURES: NEARLY 500,000 LOST",
          "Moscow's own numbers put the toll near half a million.",
          icon_candle, RED)
    panel(24 + 2 * (pw + 12), ry, pw, rh, "COLOMBIA  -  PEACE",
          "TEN YEARS SINCE THE PEACE ACCORD",
          "A decade on, the deal that ended 50 years of war holds.",
          icon_dove, GREEN)

    # ---- row 2: Bangladesh / Chess / Mercury ----
    ry2, rh2 = 652, 236
    panel(24, ry2, pw, rh2, "BANGLADESH  -  WORK",
          "GARMENT WORKERS WIN 36% PAY RISE",
          "Dhaka lifts the entry-level minimum wage by a third.",
          icon_coin, GOLD)
    panel(24 + pw + 12, ry2, pw, rh2, "CHESS  -  GENEVA",
          "GUKESH v SINDAROV: GAME 2 A 20-MOVE DRAW",
          "The title fight stays level in Geneva after a quick draw.",
          icon_chess, INK)
    panel(24 + 2 * (pw + 12), ry2, pw, rh2, "SPACE  -  MERCURY",
          "BEPICOLOMBO REACHES MERCURY AFTER 8 YEARS",
          "The probe slips into orbit around the smallest planet.",
          icon_mercury, DARKBLUE)

    # ---- bottom strip: quake + footer ticker ----
    by, bh = 900, 108
    fill_rect(24, by, W - 48, bh, INK)
    icon_quake(36, by + 8, 120, bh - 16)
    draw_text(168, by + 12, "NEPAL SHAKEN: 5.6 QUAKE HITS KOSHI PROVINCE", 2, GOLD)
    draw_text(168, by + 34, "Near the Chinese border. No major damage reported yet.",
              2, PAPER)
    hline(168, by + 58, W - 48 - 168 - 12, GREY)
    foot1 = ("INDIA MARKS CONSTITUTION DAY  -  CAIRO TANKER FIRE KILLS 30")
    foot2 = ("HASINA EYES 16 DEC  -  FLIPKART CEO OUT  -  THANKSGIVING IN USA")
    draw_text(168, by + 66, foot1, 2, PAPER)
    draw_text(168, by + 86, foot2, 2, PAPER)


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    # the grader owns the output directory: never delete it, only clear it
    if not os.path.isdir(outdir):
        os.makedirs(outdir, exist_ok=True)
    for name in os.listdir(outdir):
        p = os.path.join(outdir, name)
        if os.path.isfile(p):
            os.remove(p)
    build()
    data = chunk_png()
    with open(os.path.join(outdir, "entry.png"), "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (os.path.join(outdir, "entry.png"), len(data)))


if __name__ == "__main__":
    main()
