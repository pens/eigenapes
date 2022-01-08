#
# Copyright 2022 Seth Pendergrass. See LICENSE.
#
# 1. Uploads 'output/nft/eigenapes/*' to IPFS.
# 2. Generates corresponding ERC 721 Metadata.
# 3. Uploads folder of metadata to IPFS, as '{hash}/{index}'.
#
# NOTE: make sure `ipfs daemon` is running, and pinata is set up as a remote pinning service.
#

import json
import os
import subprocess
import time

DATA_DIR = 'data/'
IMG_DIR = 'output/nft/eigenapes/'
META_DIR = 'output/nft/metadata/'
os.makedirs(META_DIR, exist_ok=True)

SUBPROCESS_ARGS  = {
    'capture_output': True,
    'check': True,
    'text': True
}

def pin(hash, name):
    result = None
    try:
        result = subprocess.run(['ipfs', 'pin', 'remote', 'ls', '--service=pinata', f'--cid={hash}', '--status=queued,pinning,pinned'], **SUBPROCESS_ARGS)
        if not result.stdout:
            result = subprocess.run(['ipfs', 'pin', 'remote', 'add', '--service=pinata', f'--name={name}', f'{hash}'], **SUBPROCESS_ARGS)
            print(f'Pinning {name}: {hash}.')
        else:
            print(f'{name}: {hash} already pinned.')
    except: 
        print(result.stderr)
    
    # HACK: Rate limit for Pinata
    time.sleep(10)

with open(f'{DATA_DIR}eigenape_attributes.json') as f:
    attributes_all = json.load(f)

print(f'Loading apes...')

for filename in os.listdir(IMG_DIR):
    add_result = subprocess.run(['ipfs', 'add', '-q', f'{IMG_DIR}{filename}'], **SUBPROCESS_ARGS)
    image_hash = add_result.stdout.strip()

    pin(image_hash, filename)

    index = filename.removesuffix('.png')

    attributes = attributes_all[index]

    image_metadata = {
        'image': f'ipfs://{image_hash}',
        'name': f'Eigenape #{index}',
        'description': f'Principal Component #{index}',
        'attributes': attributes
    }

    with open(f'{META_DIR}{index}', 'w') as f:
        json.dump(image_metadata, f)

add_result = subprocess.run(['ipfs', 'add', '-qr', f'{META_DIR}'], **SUBPROCESS_ARGS)
metadata_hash = add_result.stdout.splitlines()[-1]

pin(metadata_hash, 'metadata')

with open(f'{DATA_DIR}test_hash', 'w') as f:
    f.write(metadata_hash)