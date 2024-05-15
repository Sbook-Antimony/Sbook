from PIL import Image, ImageDraw, ImageFont, ImageEnhance
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

def random_profile(size=500, scale=2):
    image = Image.new("RGB", (size, size), "white")
    s = 1
    for _ in range(random.randint(3, 10)):
        print("m")
        f = random.choice(eqs)
        print("eee", eqs.index(f))
        b = (1, 1)#(random.randint(0, size//2), random.randint(0, size//2))
        e = (size, size)#(random.randint(size-size//2, size), random.randint(size-size//2, size))
        
        c = random.randint(0, 2)
        
        cenx = random.randint(0, size)
        ceny = random.randint(0, size)
        for x in range(b[0]-cenx, e[0]-cenx, s):
            for y in range(b[1]-ceny, e[1]-ceny, s):
                if x*y == 0:
                    x = y = 1
                p = list(image.getpixel((x+cenx, y+ceny)))
                if sum(p) < 500:
                    continue
                fx = f(x*scale, y*scale)
                p[c] = fx % 256
                image.putpixel((x+cenx, y+ceny), tuple(p))
        s += 1
        s %= 3
        s += 1

    return ImageEnhance.Color(
        ImageEnhance.Contrast(
            image
        ).enhance(5),
    ).enhance(5)

if __name__ == '__main__':
    random_profile().save('accounts/4/profile.png')