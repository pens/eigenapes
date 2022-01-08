#
# Copyright 2022 Seth Pendergrass. See LICENSE.
#
# This downloads all images linked from a parent directory on IPFS.
# This is to collect all images associated with a catalog of NFTs, in this case https://boredapeyachtclub.com/.
#
# Structure:
# BASE_HASH/{index} -> index_json
# index_json['image'] -> ipfs://image_hash
#
# NOTE: make sure to run `ipfs daemon` prior to running this.
#

import json
import os
import subprocess

BASE_HASH = 'QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq'
OUTPUT_DIR = 'data/apes/'
os.makedirs(OUTPUT_DIR, exist_ok=True)

SUBPROCESS_ARGS = {
    'capture_output': True,
    'check': True,
    'text': True
}

hash_list_result = subprocess.run(['ipfs', 'ls', f'{BASE_HASH}'], **SUBPROCESS_ARGS)

for line in hash_list_result.stdout.splitlines():
    metadata_hash, size, index = line.split()

    print(f'Collecting {index}')

    metadata_result = subprocess.run(['ipfs', 'cat', f'{metadata_hash}'], **SUBPROCESS_ARGS)
    metadata = json.loads(metadata_result.stdout)
    
    image_hash = metadata['image'].removeprefix('ipfs://')

    subprocess.run(['ipfs', 'get', f'{image_hash}', '-o', f'{OUTPUT_DIR}{index}.png'], **SUBPROCESS_ARGS)