#!/usr/local/bin/python
import os
import sys
from hashlib import sha512

ALLOWED_HASH = "181017226fdb9cbb81e3f40a6938ddf0da538a81594e34d231ebcd6a94efa1cca3d8af7d0ef106f26a77cc89b616e927e812dc9bb95f84c874f97c04d910de65"
FLAG = os.getenv("FLAG") or "TUDCTF{FAKE_FLAG}"


def xor(bytes1: bytes, bytes2: bytes) -> bytes:
    if len(bytes1) != len(bytes2):
        raise ValueError(
            f"Lengths of input arguments don't match ({len(bytes1)} != {len(bytes2)})"
        )

    out_bytes = bytearray()
    for b1, b2 in zip(bytes1, bytes2):
        out_bytes.append(b1 ^ b2)

    return bytes(out_bytes)


def compute_script_hash(lines: list[str]) -> str:
    base_hash = b"\x00" * (512 // 8)  # 512 bits converted to bytes

    for line in lines:
        base_hash = xor(base_hash, sha512(line.encode()).digest())

    return base_hash.hex()


print("Welcome to the Super Secure Script Service!\n")
print("It can only evaluate a single script, and I'll not even tell you what it is!\n")
print(
    "This is enforced through 512 bit hashing algorithm, which is known to be unbreakable."
)
print(f"The hash should be {ALLOWED_HASH}\n")
print(
    "Please provide your script below (the reading will stop as soon as you send an empty line):"
)

script_input: list[str] = []

while (line := input("> ")) != "":
    script_input.append(line)

script_hash = compute_script_hash(lines=script_input)

if script_hash != ALLOWED_HASH:
    print("Invalid script detected!")
    print(f"Computed hash: {script_hash}")
    print("The script will be stopping now. Please re-connect for a new attempt.")
    sys.exit(-1)

print("Script valid, executing...\n\n")

exec("\n".join(script_input))
print("\n\nThe script will be stopping now. Please re-connect for a new attempt.")
