from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *
from random import randint, randbytes

# context.log_level = 'debug'

# io = process(['python3', 'source.py'])
io = remote('localhost', 50037r)

def sign(m):
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b': ', m.hex().encode())
    return bytes.fromhex(io.recvline().decode())


def verify(s):
    io.sendlineafter(b'> ', b'2')
    io.sendlineafter(b': ', s.hex().encode())
    return io.recvline()


def encrypt_with_pubkey(m):
    return bytes.fromhex(verify(m).decode().split('said ')[1].split('.')[0])


e = 65537
m1 = b'\x02'
m2 = b'\x03'
c1 = bytes_to_long(encrypt_with_pubkey(m1))
c2 = bytes_to_long(encrypt_with_pubkey(m2))

a = ZZ(bytes_to_long(m1))**e - c1
b = ZZ(bytes_to_long(m2))**e - c2
log.info('Calculating n...')
n = gcd(a, b)
log.info(f'{n = }')

m = long_to_bytes((int(pow(2, e, n)) * bytes_to_long(b'I hereby declare that I don\'t like coatis!1')) % n)
s = sign(m)
sf = long_to_bytes((int(pow(2, -1, n)) * bytes_to_long(s)) % n)

log.info(verify(sf).decode())
