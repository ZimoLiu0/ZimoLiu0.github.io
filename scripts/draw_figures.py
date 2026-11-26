"""Generate illustrative site figures. Requires Pillow."""
from math import cos, pi, sin, sqrt
from pathlib import Path
from random import Random

from PIL import Image, ImageDraw

OUTPUT = Path(__file__).resolve().parents[1] / "assets/images"
WIDTH, HEIGHT = 960, 560
BLUE = "#235c88"
TEAL = "#44939b"
PALE = "#a3c7d9"
INK = "#163954"


def canvas():
    image = Image.new("RGB", (WIDTH, HEIGHT), "#edf5f8")
    pen = ImageDraw.Draw(image)
    for x in range(0, WIDTH, 32):
        pen.line((x, 0, x, HEIGHT), fill="#e0edf2")
    for y in range(0, HEIGHT, 32):
        pen.line((0, y, WIDTH, y), fill="#e0edf2")
    return image, pen


def sphere(pen, x, y, r, color):
    pen.ellipse((x-r, y-r, x+r, y+r), fill=color)
    pen.ellipse((x-r*.48, y-r*.55, x-r*.06, y-r*.19), fill="#d7ebf1")


def lattice(pen):
    def point(i, j, layer):
        return 207 + i*66 + j*46, 340 + i*14 - j*25 - layer*101

    for layer in range(3):
        if layer:
            for i, j in [(0, 1), (1, 3), (3, 1), (4, 3), (5, 1)]:
                x, y = point(i, j, layer)
                pen.line((x+14, y+15, x+14, y+79), fill="#85a9b9", width=2)
                sphere(pen, x+14, y+46, 13, TEAL)
        corners = [point(i, j, layer) for i, j in [(0, 0), (6, 0), (6, 4), (0, 4)]]
        pen.polygon(corners, fill="#dcecf3", outline="#9cbccd", width=2)
        for i in range(7):
            for j in range(5):
                start = point(i, j, layer)
                for ni, nj in [(i+1, j), (i, j+1), (i+1, j-1)]:
                    if ni < 7 and 0 <= nj < 5:
                        pen.line((start, point(ni, nj, layer)), fill="#81aabd", width=3)
        for i in range(7):
            for j in range(5):
                sphere(pen, *point(i, j, layer), 8, BLUE if (i+j) % 3 else "#628ca6")


def electrochemistry(pen):
    pen.rounded_rectangle((214, 103, 747, 467), 72, fill="#e1eef2", outline=PALE, width=4)
    pen.rounded_rectangle((250, 137, 711, 431), 48, outline="#c1dce4", width=3)
    pen.polygon([(218, 188), (484, 316), (509, 287), (233, 167)], fill="#abd3df")
    pen.line((222, 177, 497, 301), fill=TEAL, width=5)
    for y, shade in [(332, "#6d9aaf"), (307, BLUE), (290, TEAL)]:
        pen.rounded_rectangle((370, y, 600, y+30), 6, fill=shade)
    for x in (405, 563):
        pen.line((x, 362, x, 397), fill=INK, width=4)
        sphere(pen, x, 401, 7, BLUE)
    for x, y in [(454, 267), (510, 256), (545, 232), (574, 265), (480, 228)]:
        sphere(pen, x, y, 8, TEAL)


def microscopy(pen):
    rng = Random(22)
    pen.rounded_rectangle((207, 91, 753, 466), 22, fill="#dfeef3", outline=PALE, width=3)
    for col in range(21):
        for row in range(14):
            x = 235 + col*24
            y = 116 + row*24
            if col >= 10:
                y += (col-10)*2
                x += (row-6)*2
            x += rng.uniform(-2, 2)
            y += rng.uniform(-2, 2)
            sphere(pen, x, y, rng.uniform(4, 7), rng.choice([BLUE, TEAL, "#719bac"]))
    pen.line([(489, 92), (466, 210), (504, 333), (514, 466)], fill="#518c9c", width=3)
    pen.rectangle((320, 165, 428, 272), outline="#2b6a8a", width=4)
    pen.rectangle((549, 245, 657, 352), outline="#2b6a8a", width=4)


def photocatalysis(pen):
    cx, cy, radius = 480, 282, 164
    for r in range(radius, 0, -1):
        t = r/radius
        color = (int(214-130*t), int(238-89*t), int(244-63*t))
        pen.ellipse((cx-r, cy-r, cx+r, cy+r), fill=color)
    for j in range(-5, 6):
        for i in range(-5, 6):
            x, y = i*30 + (j%2)*15, j*27
            d = sqrt(x*x+y*y)
            if d < radius-11:
                sphere(pen, cx+x, cy+y, max(4, 10-d/28), BLUE if (i+j)%2 else TEAL)
    for a in (0.10, 0.85, 2.35, 3.13, 4.1, 5.12):
        x, y = cx+radius*cos(a), cy+radius*sin(a)
        sphere(pen, x, y, 13, "#ad7742")
    pen.arc((238, 159, 724, 403), 16, 144, fill="#86b4c4", width=3)
    pen.arc((238, 159, 724, 403), 193, 339, fill="#86b4c4", width=3)


OUTPUT.mkdir(parents=True, exist_ok=True)
for drawing in (lattice, electrochemistry, microscopy, photocatalysis):
    image, pen = canvas()
    drawing(pen)
    image.save(OUTPUT / f"{drawing.__name__}.webp", quality=88)
