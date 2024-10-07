from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from flag import FLAG

###### NIST P256 
p256 = 2^256-2^224+2^192+2^96-1
a256 = p256 - 3
b256 = 41058363725152142129326129780047268409114441015993725554835256314039467401291L
## Curve order
n = 115792089210356248762697446949407573529996955224135760342422259061068512044369L
FF = GF(p256)
EC = EllipticCurve([FF(a256), FF(b256)])
EC.set_order(n)

while True:
    try:
        p = random_prime(p256)
        P = EC.lift_x(p)
        
        q = random_prime(p256)
        Q = EC.lift_x(q)
        
        S = P + Q
        break
    except:
         pass

N = int(p * q)
e = 65537L

phi = (p - 1) * (q - 1)

d = int(pow(e, -1, phi))

key = RSA.construct((N, e, d))

print(f"{N = }")
print(f"{e = }")
print(f"{S = }")

cipher = PKCS1_OAEP.new(key)
ciphertext = cipher.encrypt(FLAG)

print(f"{ciphertext = }")
