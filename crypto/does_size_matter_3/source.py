from Crypto.Util.number import bytes_to_long, getPrime
import gmpy2

p = getPrime(1024)
q = getPrime(1024)
n = p * q
phi = n - p - q + 1
d = getPrime(256)
e = pow(d, -1, phi)

flag = b'TUDCTF{sm4ll_d_15_n0_g00d}'

pt = bytes_to_long(flag)
ct = pow(pt, e, n)

print(f'{n = }\n{e = }\n{ct = }')
print(e.bit_length())
