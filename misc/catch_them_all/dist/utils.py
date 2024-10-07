# you can use this script to combine the shares into a flag (requires pycryptodome to be installed to work)
from base64 import b64encode, b64decode
from secrets import randbelow
import struct

p = 286243821277577036983567871719069679537


# a very bad implementation of Shamir's secret sharing
class SSS:
    def __init__(self, poly, p):
        self.__poly = poly
        self.p = p

    @staticmethod
    def secret_from_shares(shares, p):
        secret = 0
        for i, (x, y) in enumerate(shares):
            part = y
            for j, (x2, _) in enumerate(shares):
                if j == i:
                    continue
                part = (part * x2 * pow(x2 - x, -1, p)) % p
            secret = (secret + part) % p
        return secret

    def eval_poly(self, x):
        result = 0
        for c in self.__poly[::-1]:
            result = (result * x + c) % p
        return result

    def generate_share(self):
        x = randbelow(self.p)
        y = self.eval_poly(x)
        return (x, y)


def pack_u128(n):
    assert n < 2**128
    return struct.pack('<Q', n % 2**64) + struct.pack('<Q', n // 2**64)


def unpack_u128(b):
    assert len(b) == 16
    return struct.unpack('<Q', b[:8])[0] + 2**64 * struct.unpack('<Q', b[8:])[0]


def encode_share(share):
    x, y = share
    data = pack_u128(x) + pack_u128(y)
    return 'Share_' + b64encode(data).decode()


def decode_share(share):
    if not share.startswith('Share_'):
        return None
    try:
        data = b64decode(share[6:])
        return unpack_u128(data[:16]), unpack_u128(data[16:])
    except:
        return None


if __name__ == '__main__':
    from Crypto.Util.number import long_to_bytes

    inp = input('Please enter your shares in text format (i.e. "Share_[...]"; in one line, comma-separated): ')
    shares = [decode_share(s.strip()) for s in inp.split(',')]

    if len(shares) < 7:
        print('You need at least 7 shares to recover the flag!')
        exit(1)

    print('TUDCTF{' + long_to_bytes(SSS.secret_from_shares(shares, p)).decode() + '}')