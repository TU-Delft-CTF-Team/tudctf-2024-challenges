from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

p256 = 2^256-2^224+2^192+2^96-1
a256 = p256 - 3
b256 = 41058363725152142129326129780047268409114441015993725554835256314039467401291L

N = 5263091526002310358713253746430983648957374396594142858467294133393289652113425527742806105572888024891467911799231733585405648983874397151382549194440413L
e = 65537L

Sx = 85924306762757268856776393681616085205867304211289522805684550580620346963724
Sy = 107846703320728484375490195974162467066274800152239264881557414841006797910796

enc_flag = b'6\xc8]c\xcd\x9a\x97\x8f}\xd0z\xd3\x01\\\x8d_-Q\xbd\xc4\xddx+O\x01oO\r|M^\xa9\xfa\xb4\xa1F\xf1\xf9\x00\x99\xc3\xf9\xa8\x85D\x1a\x97k\xf6dVC\xd2Pz\x13p\x19Hc\xa6\xdf\xaa\xdc'

F = GF(p256)
R.<Px> = PolynomialRing(F)

Py2 = Px^3 + a256*Px + b256

f1 = (N + (Sx + Px)*Px)*(Px - Sx)^2
f2 = Px*(Py2 + Sy^2)

sol = (f1 - f2)^2 - (4*Px^2*Sy^2*Py2)

p = sol.roots()[0][0]

p = int(p)

assert is_prime(p)
q = N // p

assert is_prime(q)

phi = int((p - 1) * (q - 1))

d = int(pow(e, -1, phi))

key = RSA.construct((N, e, d))

cipher = PKCS1_OAEP.new(key)

f = cipher.decrypt(enc_flag)

print(b"TUDCTF{" + f + b"}")
