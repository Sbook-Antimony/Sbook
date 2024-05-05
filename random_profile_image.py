import tensorflow as tf
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Define the size of the image
image_size = 128
channels = 3

# Function to generate an image based on a given name
def generate_from_name(name):
    # Define a function to convert a string to a tensor
    def string_to_tensor(string):
        return tf.convert_to_tensor([ord(c) for c in string])

    # Define a function to generate an image from a tensor
    def generate_image_from_tensor(tensor):
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(input_dim=128, output_dim=256),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(4*4*256, use_bias=False),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.LeakyReLU(),
            tf.keras.layers.Reshape((4, 4, 256)),
            tf.keras.layers.Conv2DTranspose(128, (5, 5), strides=(2, 2), padding='same', use_bias=False),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.LeakyReLU(),
            tf.keras.layers.Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='same', use_bias=False),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.LeakyReLU(),
            tf.keras.layers.Conv2DTranspose(channels, (5, 5), strides=(2, 2), padding='same', use_bias=False, activation='tanh')
        ])

        # Generate image from tensor
        generated_image = model(tensor, training=False)

        # Rescale the pixel values from [-1, 1] to [0, 255]
        generated_image = (generated_image + 1) * 127.5
        generated_image = tf.cast(generated_image, tf.uint8)

        return generated_image.numpy()[0]

    # Convert name to tensor
    name_tensor = string_to_tensor(name)

    # Generate image from tensor
    image_data = generate_image_from_tensor(name_tensor)

    return Image.fromarray(image_data)


