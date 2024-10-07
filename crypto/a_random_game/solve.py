from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
from hashlib import sha256
from pwn import *
import struct

N = 624
M = 397
_A = 0x9908b0df
UP = 0x80000000
LO = 0x7fffffff
A = [0, _A]


def previous_number(st):
    assert len(st) == N
    p_up = ((st[623] ^ st[M - 1] ^ A[st[0] & 1]) & (UP >> 1)) << 1
    y = st[622] ^ st[M - 2]

    if y & (1 << 31) != 0:
        p_lo = (((y ^ _A) & (LO >> 1)) << 1) | 1
    else:
        p_lo = (y & (LO >> 1)) << 1

    return p_up | p_lo


def previous_possible_numbers(st):
    assert len(st) == N
    y = st[622] ^ st[M - 2]

    if y & (1 << 31) != 0:
        p_lo = (((y ^ _A) & (LO >> 1)) << 1) | 1
    else:
        p_lo = (y & (LO >> 1)) << 1

    return [p_lo, (1 << 31) | p_lo]


def temper(y):
    y ^= ((y >> 11) & 0xFFFFFFFF)
    y ^= ((y << 7) & 0x9d2c5680)
    y ^= ((y << 15) & 0xefc60000)
    return y ^ (y >> 18)


# stolen shamelessly from https://github.com/kmyk/mersenne-twister-predictor/blob/master/mt19937predictor.py
def untemper(y):
    y ^= (y >> 18)
    y ^= (y << 15) & 0xefc60000
    y ^= ((y <<  7) & 0x9d2c5680) ^ ((y << 14) & 0x94284000) ^ ((y << 21) & 0x14200000) ^ ((y << 28) & 0x10000000)
    y ^= (y >> 11) ^ (y >> 22)
    return y


# io = process(['python3', './challenge.py'])
io = remote('localhost', 50021)


def unpack_rng_word(w):
    return untemper(struct.unpack('<I', w)[0])


def receive_chunk(all):
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b': ', b'42' * 16)
    io.sendlineafter(b': ', b'42' * 16)
    if all:
        io.sendlineafter(b'? ', b'y')
        result = unhexlify(io.recvline().split(b' ')[-1].strip())
        assert len(result) == 16, f'Length of result was {len(result)}, not 16'
        return [unpack_rng_word(result[:4]), unpack_rng_word(result[4:8]), unpack_rng_word(result[8:12]), unpack_rng_word(result[12:])]
    else:
        io.sendlineafter(b'? ', b'n')
        result = unhexlify(io.recvline().split(b' ')[-1].strip()[16:])
        assert len(result) == 8, f'Length of result was {len(result)}, not 8'
        return [None, None, unpack_rng_word(result[:4]), unpack_rng_word(result[4:])]


for i in range(10):
    _ = io.recvline()
    state = []
    for i in range(156):
        state += receive_chunk(i == 155)

    possible_numbers = previous_possible_numbers(state)
    possible_numbers_2 = [p64((temper(x) << 32) | temper(previous_number([x] + state[:-1]))) for x in possible_numbers]

    possible_keys = [sha256(x).digest()[:16] for x in possible_numbers_2]

    io.sendlineafter(b'> ', b'3')
    ct = unhexlify(io.recvline().strip())

    for key in possible_keys:
        cipher = AES.new(key, AES.MODE_ECB)
        pt = cipher.decrypt(ct)
        io.sendlineafter(b'? ', hexlify(pt))
        res = io.recvline()
        if b'o_O' in res:
            print('Got it!')
            break
    else:
        print('Failed miserably')
        exit()

print(io.recvline().strip().decode())
