import random

from PIL import Image


side = 100
image = Image.new("RGB", (side, side), "white")

cache = []
diff = 100
le = 5
li = 100
theme = (120, 35, 170)


def themex(n):
    return tuple(map(lambda x: int(((x + n) // 2 + n) // 2), theme))


for y in range(side):
    for x in range(side):
        cache.append(random.randint(-diff / 2, diff / 2) + li)
        image.putpixel((x, y), themex(sum(cache) / len(cache)))
        cache = cache[-le:]


for y in range(side):
    for x in range(side):
        cache.append(random.randint(-diff / 2, diff / 2) + li)
        pix = sum(cache) / len(cache)
        pix += image.getpixel((x, y))[0]
        pix = int(pix / 2)
        image.putpixel((x, y), themex(pix))
        cache = cache[-le:]


image.save("quizz-header.png")
