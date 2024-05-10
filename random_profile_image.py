from PIL import Image, ImageDraw, ImageFont
import random

eqs = [
    lambda x, y: x%y,
    lambda x, y: y%x,
    lambda x, y: x*y,
    lambda x, y: x**2//y,
    lambda x, y: y**2//x,
    lambda x, y: x+y,
    lambda x, y: x-y,
    lambda x, y: y-x,
    lambda x, y: x**2-y,
    lambda x, y: y**2-x,
    lambda x, y: min(x, y),
    lambda x, y: max(x, y),
    lambda x, y: x,
    lambda x, y: y,
]

def random_profile(size=500):
    image = Image.new("RGB", (size, size), "white")
    s = 1
    for _ in range(random.randint(3, 10)):
        print("m")
        f = random.choice(eqs)
        print("eee", eqs.index(f))
        b = (1, 1)#(random.randint(0, size//2), random.randint(0, size//2))
        e = (size, size)#(random.randint(size-size//2, size), random.randint(size-size//2, size))
        
        c = random.randint(0, 2)
        
        cen = size // 2
        for x in range(b[0]-cen, e[0]-cen, s):
            for y in range(b[1]-cen, e[1]-cen, s):
                if x*y == 0:
                    x = y = 1
                p = list(image.getpixel((x+cen, y+cen)))
                if sum(p) < 500:
                    continue
                fx = f(x, y)
                p[c] = fx % 256
                image.putpixel((x, y), tuple(p))
        s += 1
        s %= 3
        s += 1
    return image

if __name__ == '__main__':
    random_profile().save('image/default-photo.png')