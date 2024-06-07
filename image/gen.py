import random

from PIL import Image


side = 100
image = Image.new("RGB", (side, side), "white")

cache = []
diff = 40
le = 50
li = 240

for y in range(side):
    for x in range(side):
        cache.append(random.randint(-diff // 2, diff // 2) + li)
        image.putpixel((x, y), (sum(cache) // len(cache),) * 3)
        cache = cache[-le:]


for y in range(side):
    for x in range(side):
        cache.append(random.randint(-diff // 2, diff // 2) + li)
        pix = sum(cache) / len(cache)
        pix += image.getpixel((x, y))[0]
        pix = int(pix / 2)
        image.putpixel((x, y), (pix,) * 3)
        cache = cache[-le:]


image.save("back-lighter-dashy.png")
