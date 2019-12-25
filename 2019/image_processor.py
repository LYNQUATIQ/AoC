import logging

IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6
IMAGE_SIZE = IMAGE_WIDTH * IMAGE_HEIGHT

WHITE = "0"
BLACK = "1"
TRANSPARENCY = "2"

pixel_map = {
    WHITE: " ",
    BLACK: u"\u2588",
    TRANSPARENCY: ".",
}


def read_layers(filename):
    layers = []
    with open(filename) as f:
        while True:
            layer = f.read(IMAGE_SIZE)
            if not layer:
                break
            layers.append(layer)
    return layers


def process_layers(layers):
    image = [pixel_map[TRANSPARENCY] for _ in range(IMAGE_SIZE)]
    for location in range(IMAGE_SIZE):
        for layer in layers:
            pixel = layer[location]
            if pixel == TRANSPARENCY:
                continue
            image[location] = pixel_map[pixel]
            break
    return image


def display_image(image):
    for i in range(0, IMAGE_SIZE, IMAGE_WIDTH):
        print("".join(image[i : i + IMAGE_WIDTH]))


layers = read_layers("image.txt")
image = process_layers(layers)
display_image(image)
