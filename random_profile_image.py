from PIL import Image, ImageDraw, ImageFont
import random

def random_profile(size=500):
    # Create a new image with white background
    image = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(image)

    # Define the limited color palette
    colors = [(229, 43, 80), (0, 255, 255), (255, 171, 129)]  # Antimony, Cyan, Napples

    # Draw random circles
    for _ in range(random.randint(1, 3)):
        x = random.randint(0, size)
        y = random.randint(0, size)
        radius = random.randint(size // 8, size // 3)
        color = random.choice(colors)
        draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=color)

    # Draw random squares
    for _ in range(random.randint(1, 3)):
        x1 = random.randint(0, size)
        y1 = random.randint(0, size)
        min_size = size // 5
        max_size = size // 2
        width = random.randint(min_size, max_size)
        height = random.randint(min_size, max_size)
        color = random.choice(colors)
        draw.rectangle([(x1, y1), (x1 + width, y1 + height)], fill=color)

    # Save the image
    return image
