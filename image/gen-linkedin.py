import random

from PIL import Image

w, h = size = (1000, 200)
image = Image.new("RGB", size, "white")

cache = []
diff = 40
le = 3
li = 20

for y in range(h):
    for x in range(w):
        cache.append(random.randint(-diff // 2, diff // 2) + li)
        image.putpixel((x, y), (sum(cache) // len(cache),) * 3)
        cache = cache[-le:]


for x in range(w):
    for y in range(h):
        cache.append(random.randint(-diff // 2, diff // 2) + li)
        pix = sum(cache) / len(cache)
        pix += image.getpixel((x, y))[0]
        pix = int(pix / 2)
        image.putpixel((x, y), (pix,) * 3)
        cache = cache[-le:]


image.save("back-linkedin.png")
