import numpy as np
from PIL import Image

# Define the size of the image
image_size = 128
channels = 3

# Function to generate and save an image based on a given name
def generate_and_save_image(name, filename):
    # Define a function to convert a string to a tensor
    def string_to_tensor(string):
        return np.array([ord(c) for c in string])

    # Define a function to generate an image from a tensor
    def generate_image_from_tensor(tensor):
        # Define a simple generator model
        def generator(input_size):
            model = [
                np.random.normal(0, 1, size=(input_size, 256)),  # Embedding
                np.random.normal(0, 1, size=(input_size, 4*4*256)),  # Dense layer
                np.random.normal(0, 1, size=(4, 4, 256)),  # Reshape
                np.random.normal(0, 1, size=(5, 5, 128)),  # Conv2DTranspose layer 1
                np.random.normal(0, 1, size=(5, 5, 64)),   # Conv2DTranspose layer 2
                np.random.normal(0, 1, size=(5, 5, channels))  # Conv2DTranspose layer 3
            ]
            return model

        # Generate image from tensor
        model = generator(tensor.shape[0])
        for layer in model:
            tensor = np.matmul(tensor, layer)

        # Rescale the pixel values from [-1, 1] to [0, 255]
        generated_image = (tensor + 1) * 127.5
        generated_image = generated_image.astype(np.uint8)

        return generated_image

    # Convert name to tensor
    name_tensor = string_to_tensor(name)

    # Generate image from tensor
    image_data = generate_image_from_tensor(name_tensor)

    # Create PIL image
    image = Image.fromarray(image_data)

    # Save image
    image.save(filename)

# Example usage:
generate_and_save_image("John Doe", "generated_image.png")
