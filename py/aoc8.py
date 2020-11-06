from pathlib import Path
from math import inf

def get_image_layers(raw_data, width, height):
    digits = map(int, raw_data.strip())
    layers = list()
    curr_layer = list()
    layer_size = width * height
    for digit in digits:
        curr_layer.append(digit)
        if len(curr_layer) == layer_size:
            layers.append(curr_layer)
            curr_layer = list()

    return layers

def layer_digit_count(layer, digit):
    return len(list(filter(lambda d: d == digit, layer)))

def fewest_zeros(layers):
    index = -1
    fewest = inf
    for l, layer in enumerate(layers):
        zeros = layer_digit_count(layer, 0)
        if zeros < fewest:
            fewest = zeros
            index = l

    return index

def get_layer_data(layers, index):
    layer = layers[index]
    ones = layer_digit_count(layer, 1)
    twos = layer_digit_count(layer, 2)
    return ones * twos

def display_image(layers, width, height):
    layer_size = width * height
    pixels = [list() for ls in range(layer_size)]
    for layer in layers:
        for d, digit in enumerate(layer):
            if digit != 2:
                pixels[d].append(digit)

    image = list()
    pixel_row = list()
    for pixel in pixels:
        pixel_row.append(" " if pixel[0] == 0 else "@")
        if len(pixel_row) == width:
            print("".join(pixel_row))
            pixel_row = list()

if __name__ == "__main__":
    dsn_data = Path("../etc/aoc8.txt").read_text()
    image_width = 25
    image_height = 6
    image_layers = get_image_layers(dsn_data, image_width, image_height)
    layer_index = fewest_zeros(image_layers)
    result1 = get_layer_data(image_layers, layer_index)
    print("Part 1:", result1)
    print("Part 2:")
    display_image(image_layers, image_width, image_height)
