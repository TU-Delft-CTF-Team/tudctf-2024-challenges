#!/usr/bin/python3

from pwn import *

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pss

conn = process(['python3', 'secure_good_luck_verification_protocol.py'], level='debug')

conn.readuntil(b"Provide your N: ")

key = RSA.generate(1024)
conn.sendline(str(key.n).encode())

s = pss.new(key)

def sign(message):
    return s.sign(SHA256.new(message))

for _ in range(20):
    conn.readuntil(b"r = ")
    r = int(conn.readline().decode())

    conn.readuntil(b'Please sign my number (hex): ')

    while True:
        signature = sign(r.to_bytes(128, byteorder='big'))
        result = int.from_bytes(SHA256.new(signature).digest(), byteorder='big') % 6 + 1
        # print('result', result)
        if result == 6:
            break

    conn.sendline(signature.hex().encode())

print(conn.readall().decode())
