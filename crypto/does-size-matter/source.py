from Crypto.Util.number import *

p = -1 # REDACTED
q = -1 # REDACTED

N = p*q
e = 65537

FLAG = b"TUDCTF{REDACTED}"

pt = bytes_to_long(FLAG)

ct = pow(pt, e, N)

print(f"{N = }")
print(f"{e = }")
print(f"{ct = }")
