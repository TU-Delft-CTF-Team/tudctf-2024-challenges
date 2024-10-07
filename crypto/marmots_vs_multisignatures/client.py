import asyncio
from Crypto.Util.number import bytes_to_long, long_to_bytes
from fastecdsa.curve import W25519 as C
from fastecdsa.encoding import sec1
from hashlib import sha256
import json
from os import getenv
from secrets import randbelow, token_bytes


def Hagg(p, L):
    l = sum(L.values(), start=C.G.IDENTITY_ELEMENT)
    e = sec1.SEC1Encoder()
    l = e.encode_public_key(l)
    p = e.encode_public_key(p)
    return bytes_to_long(sha256(l + p).digest()) % C.q


def Hck(m):
    a = bytes_to_long(sha256(m).digest()) % C.q
    return a * C.G


def Hc(T, pk, m):
    e = sec1.SEC1Encoder()
    T = e.encode_public_key(T)
    pk = e.encode_public_key(pk)
    return bytes_to_long(sha256(T + pk + m).digest()) % C.q


def zip_dicts(*ds):
    keys = set(k for d in ds for k in d.keys())
    for k in keys:
        yield (k, tuple(d.get(k) for d in ds))


class Signer:
    def __init__(self, id, privkey, pubkey, all_pubkeys, msg):
        self.id = id
        self.privkey = privkey
        self.pubkey = pubkey
        self.all_pubkeys = all_pubkeys
        self.msg = msg
    
    def round1(self):
        self.t = {k: Hagg(pubk, self.all_pubkeys) for k, pubk in self.all_pubkeys.items()}
        self.pk = sum([t * pubk for _, (t, pubk) in zip_dicts(self.t, self.all_pubkeys)], start=C.G.IDENTITY_ELEMENT)
        U = Hck(self.msg)
        self.r = randbelow(C.q >> 32)
        self.z = randbelow(C.q >> 32)
        self.T = self.z * U + self.r * C.G
        self.zs = {self.id: self.z}
        self.Ts = {self.id: self.T}

    def round2(self):
        self.T = sum(self.Ts.values(), start=C.G.IDENTITY_ELEMENT)
        self.c = Hc(self.T, self.pk, self.msg)
        self.s = (self.privkey * self.t[self.id] * self.c + self.r) % C.q
        self.ss = {'id': self.s}

    def combine(self):
        z = sum(self.zs.values()) % C.q
        s = sum(self.ss.values()) % C.q
        return [self.c, z, s]


async def client():
    num_clients = 3
    privkey = getenv('FLAG')
    if privkey is not None:
        privkey = bytes_to_long(privkey.encode())
    else:
        privkey = randbelow(C.q)
    pubkey = privkey * C.G

    e = sec1.SEC1Encoder()
    reader, writer = await asyncio.open_connection('172.21.37.1', 7070)
    id = (await reader.readline()).decode()

    while True:
        msg = await reader.readline()
        pubkeys = {id: pubkey}

        await asyncio.sleep(1)

        writer.write((json.dumps({'pubkey': e.encode_public_key(pubkey).hex()}) + '\n').encode())
        await writer.drain()
        while len(pubkeys) < num_clients:
            r = json.loads((await reader.readline()).decode())
            pubkeys |= {r['id']: e.decode_public_key(bytes.fromhex(r['pubkey']), C)}
        
        s = Signer(id, privkey, pubkey, pubkeys, msg)
        s.round1()
        
        writer.write((json.dumps({'T': e.encode_public_key(s.T).hex()}) + '\n').encode())
        await writer.drain()
        while len(s.Ts) < num_clients:
            r = json.loads((await reader.readline()).decode())
            s.Ts |= {r['id']: e.decode_public_key(bytes.fromhex(r['T']), C)}
        
        s.round2()

        writer.write((json.dumps({'z': s.z, 's': s.s}) + '\n').encode())
        await writer.drain()
        while len(s.ss) < num_clients:
            r = json.loads((await reader.readline()).decode())
            s.ss |= {r['id']: r['s']}
            s.zs |= {r['id'] : r['z']}

        writer.write((json.dumps({'sigma': s.combine()}) + '\n').encode())
        await writer.drain()


if __name__ == '__main__':
    asyncio.run(client())
