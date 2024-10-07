from Crypto.Util.number import bytes_to_long, long_to_bytes
from fastecdsa.curve import W25519 as C
from fastecdsa.encoding import sec1
from hashlib import sha256
import json
import pyshark

from sage.all import *


def Hagg(p, L):
    l = sum(L.values(), start=C.G.IDENTITY_ELEMENT)
    e = sec1.SEC1Encoder()
    l = e.encode_public_key(l)
    p = e.encode_public_key(p)
    return bytes_to_long(sha256(l + p).digest()) % C.q


def decode_key(r):
    e = sec1.SEC1Encoder()
    return e.decode_public_key(bytes.fromhex(r), C)


def zip_dicts(*ds):
    keys = set(k for d in ds for k in d.keys())
    for k in keys:
        yield (k, tuple(d.get(k) for d in ds))


keys = {}
interesting_id = '5e547334-68c1-4ca2-9748-57f560372648'
cs = []
ss = []

with pyshark.FileCapture('dump.pcapng', display_filter='tcp.dstport == 7070 && tcp.flags.push == 1') as cap:
    for p in cap:
        data = bytes.fromhex(p.data.data).decode('utf-8')
        try:
            msg = json.loads(data)
            if 'pubkey' in msg:
                keys['xd'] = decode_key(msg['pubkey'])
            elif 'sigma' in msg:
                [c, z, s] = msg['sigma']
                cs.append(c)
        except:
            continue

with pyshark.FileCapture('dump.pcapng', display_filter='tcp.srcport == 7070 && tcp.flags.push == 1') as cap:
    for p in cap:
        data = bytes.fromhex(p.data.data).decode('utf-8')
        try:
            msg = json.loads(data)
            if (key := msg.get('pubkey')) is not None:
                keys[msg['id']] = decode_key(key)
            else:
                if msg['id'] != interesting_id:
                    continue
                if (s := msg.get('s')) is not None:
                    ss.append(s)
        except:
            continue

ts = {k: Hagg(pubk, keys) for k, pubk in keys.items()}
pk = sum([t * pubk for _, (t, pubk) in zip_dicts(ts, keys)], start=C.G.IDENTITY_ELEMENT)
t = ts[interesting_id]
q = C.q

p = C.q
samples = [((t * c) % q, s) for (c, s) in zip(cs, ss)]
num_samples = 2 * ceil(sqrt(log(p, 2)))
B = p // (2**(ceil(sqrt(log(p, 2))) + ceil(log(log(p, 2), 2))))

assert len(samples) >= num_samples, f'{len(samples)} < {num_samples}'
num_samples = len(samples)

mat = matrix.identity(num_samples) * p
mat = mat.augment(matrix([[0 for _ in range(2)] for _ in range(num_samples)]))
mat = mat.stack(matrix([t for (t, a) in samples] + [Rational((B, p)), 0]))
mat = mat.stack(matrix([a for (t, a) in samples] + [0, B]))
reduced = mat.LLL()
recovered = reduced[1][-2] * p // B
print(long_to_bytes(abs(int(recovered))).decode())
