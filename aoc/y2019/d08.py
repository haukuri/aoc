from collections import Counter

from .utils import open_input

def segment(segment_size, iterable):
    segment = []
    for x in iterable:
        segment.append(x)
        if len(segment) == segment_size:
            yield segment
            segment = []
    if segment:
        yield segment

def split_layers(image, height, width):
    layer_size = height * width
    layers = list(segment(layer_size, image))
    return layers

def print_layer(layer, height, width):
    for row in segment(width, layer):
        rendered_row = ['\u2588' if cell else ' ' for cell in row]
        print(*rendered_row, sep='')

def collapse_layers(layers):
    TRANSPARENT = 2
    collapsed = list(layers[0])
    for layer in layers[1:]:
        for i in range(len(collapsed)):
            if collapsed[i] == TRANSPARENT:
                collapsed[i] = layer[i]
    return collapsed


def main():
    encoded = open_input('d08input').readlines()[0]
    image = [int(d) for d in encoded.strip()]
    layers = split_layers(image, 6, 25)
    picked = { 0: 6 * 25 }
    for layer in layers:
        counts = Counter(layer)
        if counts[0] <= picked[0]:
            picked = counts
    checksum = picked[1] * picked[2]
    print('Checksum', checksum)

    collapsed = collapse_layers(layers)
    print_layer(collapsed, 6, 25)

if __name__ == '__main__':
    main()