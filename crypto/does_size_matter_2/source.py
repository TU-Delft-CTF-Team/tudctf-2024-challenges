from Crypto.Util.number import bytes_to_long, getPrime

p = getPrime(1024)
q = getPrime(1024)
n = p * q
e = 3

flag = b'TUDCTF{wh0_n33d5_d_4nyw4y5}'

pt = bytes_to_long(flag)
ct = pow(pt, 3, n)

print(f'{n = }\n{e = }\n{ct = }')
