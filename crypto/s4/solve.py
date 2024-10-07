#!/usr/bin/python3.11
import random
import string
from hashlib import sha512

from sage.all import GF, matrix, vector
from tqdm import tqdm

ALLOWED_HASH = bytes.fromhex(
    "181017226fdb9cbb81e3f40a6938ddf0da538a81594e34d231ebcd6a94efa1cca3d8af7d0ef106f26a77cc89b616e927e812dc9bb95f84c874f97c04d910de65"
)

DESIRED_SCRIPT_LINE = "print(FLAG)"


def to_vector(h: bytes) -> list[int]:
    v: list[int] = []
    for c in h:
        for i in range(8):
            v.append((c >> i) & 1)
    return v


def xor(bytes1: bytes, bytes2: bytes) -> bytes:
    if len(bytes1) != len(bytes2):
        raise ValueError(
            f"Lengths of input arguments don't match ({len(bytes1)} != {len(bytes2)})"
        )

    out_bytes = bytearray()
    for b1, b2 in zip(bytes1, bytes2):
        out_bytes.append(b1 ^ b2)

    return bytes(out_bytes)


start_line_hash = sha512(DESIRED_SCRIPT_LINE.encode()).digest()
goal = to_vector(xor(ALLOWED_HASH, start_line_hash))


vectors: list[list[int]] = []
comments: list[str] = []

gf2 = GF(2)

pbar = tqdm(total=512)
current_rank = 0
iterations = 0
while len(vectors) < 512:
    iterations += 1
    random_str = "# " + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=5)
    )

    random_vec = to_vector(sha512(random_str.encode()).digest())

    m = matrix(gf2, vectors + [random_vec])

    if m.rank() > current_rank:
        vectors.append(random_vec)
        comments.append(random_str)
        current_rank = m.rank()
        pbar.update(1)
pbar.close()

m = matrix(gf2, vectors).transpose()
solved_eq = m.solve_right(vector(goal))

out_comments = []
for is_part_of_solution, comment in zip(solved_eq, comments):
    if is_part_of_solution:
        out_comments.append(comment)

with open("malicious.py", "w") as f:
    f.write(DESIRED_SCRIPT_LINE + "\n")
    f.write("\n".join(out_comments))
    f.write("\n")

print(f"Found solution in {iterations} iterations")
