import bcrypt
import hashlib
import subprocess
import os
import stat

def get_secure_hash(path):
    with open(path, 'rb') as f:
        content = f.read()
    insecure_hash = hashlib.sha256(content).digest()
    secure_hash = bcrypt.kdf(password=insecure_hash, salt='NaCl'.encode(), desired_key_bytes=32, rounds=256).hex()
    return secure_hash

def is_allowed(h):
    with open('hashes.txt', 'r') as f:
        hashes = f.readlines()
    return any(h == hsh.strip() for hsh in hashes)

def execute_script(path):
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
    proc = subprocess.run([path], capture_output=True)
    output = proc.stdout.decode('utf-8') + proc.stderr.decode('utf-8')
    return output
