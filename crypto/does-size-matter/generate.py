from Crypto.Util.number import *

p = getPrime(32)
q = getPrime(1024)

N = p*q
e = 65537

FLAG = b"TUDCTF{f4ct0rization-b3c0mes-t00-easy}"

pt = bytes_to_long(FLAG)

ct = pow(pt, e, N)

print(f"{N = }")
print(f"{e = }")
print(f"{ct = }")
