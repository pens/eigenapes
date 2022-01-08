#
# Copyright 2022 Seth Pendergrass. See LICENSE.
#
# Generates some simple images to make into test NFTs
# Note: run from root directory
#

import json
import os

import numpy as np
from numpy.random import default_rng
from PIL import Image

rng = default_rng(256)

OUTPUT_DIR = 'output/'
IMG_DIR = f'{OUTPUT_DIR}test_images/'
os.makedirs(IMG_DIR, exist_ok=True)

attributes = {}

for i in range(400):
    r = rng.integers(256, dtype=int)
    g = rng.integers(256, dtype=int)
    b = rng.integers(256, dtype=int)

    x = np.ndarray((256, 256, 3), dtype=np.uint8)
    x[...] = [r, g, b]
    im = Image.fromarray(x)

    name = f'{r:02x}{g:02x}{b:02x}'

    im.save(f'{IMG_DIR}{i}.jpg')

    print(f'Saved {name}')

    attributes[i]  = {
        'red': r,
        'green': g,
        'blue': b
    }

with open(f'{OUTPUT_DIR}test_attributes.json', 'w') as f:
    json.dump(attributes, f)