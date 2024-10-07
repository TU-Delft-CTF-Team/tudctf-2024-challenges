#!/usr/bin/env python3
import utils
import os

directory = 'static/files'
files = os.listdir(directory)
hashes = [utils.get_secure_hash(os.path.join(directory, file)) + "\n" for file in files]
with open('hashes.txt', 'w') as f:
    f.writelines(hashes)
