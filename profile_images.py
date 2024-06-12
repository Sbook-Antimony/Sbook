import random
import json

from PIL import Image
from PIL import ImageDraw
from PIL import ImageEnhance
from PIL import ImageFont
from django.core.files import File
eqs = [
    lambda x, y: x % y,
    lambda x, y: y % x,
    lambda x, y: x * y,
    lambda x, y: x**2 // y,
    lambda x, y: y**2 // x,
    lambda x, y: x + y,
    lambda x, y: x - y,
    lambda x, y: y - x,
    lambda x, y: x**2 - y,
    lambda x, y: y**2 - x,
    lambda x, y: min(x, y),
    lambda x, y: max(x, y),
    lambda x, y: x,
    lambda x, y: y,
]


def random_profile(size=200, scale=2):
    image = Image.new("RGB", (size, size), "white")
    s = 1
    for _ in range(random.randint(3, 10)):
        print("m")
        f = random.choice(eqs)
        print("eee", eqs.index(f))
        b = (1, 1)  # (random.randint(0, size//2), random.randint(0, size//2))
        e = (
            size,
            size,
        )
        c = random.randint(0, 2)

        cenx = random.randint(0, size)
        ceny = random.randint(0, size)
        for x in range(b[0] - cenx, e[0] - cenx, s):
            for y in range(b[1] - ceny, e[1] - ceny, s):
                if x * y == 0:
                    x = y = 1
                p = list(image.getpixel((x + cenx, y + ceny)))
                if sum(p) < 500:
                    continue
                fx = f(x * scale, y * scale)
                p[c] = fx % 256
                image.putpixel((x + cenx, y + ceny), tuple(p))
        s += 1
        s %= 3
        s += 1

    return ImageEnhance.Color(
        ImageEnhance.Contrast(image).enhance(5),
    ).enhance(5)


def average_color(image, step=10):
    width, height = image.size
    pixels = image.load()

    red = 0
    green = 0
    blue = 0

    for x in range(0, width, step):
        for y in range(0, height, step):
            try:
                r, g, b = pixels[x, y]
            except TypeError:
                try:
                    r = g = b = pixels[x, y]
                except Exception:
                    return (128, 128, 128)
            red += r
            green += g
            blue += b

    num = width * height // step // step

    return (red // num, green // num, blue // num)


profile_images = [
    f"media/profiles/random/{x}.png"
    for x in json.loads(
        open('media/profiles/random/random-profiles.json').read()
    )
]


def get_random():
    return random.choice(profile_images)


def get_random_file():
    return File(open(get_random(), 'rb'))
