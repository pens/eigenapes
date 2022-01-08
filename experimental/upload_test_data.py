#
# Copyright 2022 Seth Pendergrass. See LICENSE.
#
# 1. Uploads 'output/nft/eigenapes/*' to IPFS.
# 2. Generates corresponding ERC 721 Metadata.
# 3. Uploads folder of metadata to IPFS, as '{hash}/{index}'.
#
# NOTE: make sure `ipfs daemon` is running.
#

import json
import os
import subprocess

DATA_DIR = 'output/'
IMG_DIR = f'{DATA_DIR}test_images/'
META_DIR = f'{DATA_DIR}test_metadata/'
os.makedirs(META_DIR, exist_ok=True)

SUBPROCESS_ARGS  = {
    'capture_output': True,
    'check': True,
    'text': True
}

with open(f'{DATA_DIR}test_attributes.json') as f:
    attributes_all = json.load(f)

for filename in os.listdir(IMG_DIR):
    add_result = subprocess.run(['ipfs', 'add', '-q', f'{IMG_DIR}{filename}'], **SUBPROCESS_ARGS)
    image_hash = add_result.stdout.strip()

    print(f'Uploaded {filename} as {image_hash}')

    index = filename.removesuffix('.jpg')

    attributes = attributes_all[index]

    image_metadata = {
        'image': f'ipfs://{image_hash}',
        'name': f'Color #{index}',
        'description': f'Randomly generated color #{index}',
        'attributes': attributes
    }

    with open(f'{META_DIR}{index}', 'w') as f:
        json.dump(image_metadata, f)

add_result = subprocess.run(['ipfs', 'add', '-qr', f'{META_DIR}'], **SUBPROCESS_ARGS)
hash = add_result.stdout.splitlines()[-1]

print(f'Uploaded metadata to {hash}')
with open(f'{DATA_DIR}test_hash', 'w') as f:
    f.write(hash)