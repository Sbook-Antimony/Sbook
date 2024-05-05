import random
import math
from PIL import Image, ImageDraw

def generate_profile_image(url, size=500):
    # Create a new blank image
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)

    # Define center and radius
    center_x = size // 2
    center_y = size // 2
    radius = size // 2

    # Generate random colors for background and shapes
    bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Fill the background with a random color
    draw.rectangle([(0, 0), (size, size)], fill=bg_color)

    # Generate random number of circles
    num_circles = random.randint(4, 8)
    for _ in range(num_circles):
        # Generate random circle parameters
        circle_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        cx = random.randint(0, size)
        cy = random.randint(0, size)
        r = random.randint(10, size // 2)

        # Draw circle
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=circle_color)

    # Save the image
    img.save(url)

