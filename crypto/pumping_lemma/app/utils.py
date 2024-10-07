from hashlib import sha256
from typing import Optional
from urllib.parse import quote, unquote


def sign(key: bytes, message: bytes) -> bytes:
    return message.hex() + '/' + sha256(key + message).hexdigest()


def verify(key: bytes, signature: str) -> Optional[bytes]:
    try:
        msg_hex, digest = signature.split('/')
        msg = bytes.fromhex(msg_hex)
        if sha256(key + msg).hexdigest() == digest:
            return msg
        else:
            return None
    except ValueError:
        return None


def dump_dict(d: dict[str, str]) -> str:
    return '&'.join(quote(k) + '=' + quote(v) for k, v in d.items())


def parse_dict(d: str) -> dict[str, str]:
    return {unquote(k): unquote(v) for k, v in (p.split('=') for p in d.split('&'))}
