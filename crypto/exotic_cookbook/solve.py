from pwn import *

p = process(["python3", "source.py"])
p.recvuntil("back? ")
p.sendline(b"true\x04\x04\x04\x04")
token = p.recvline().strip().decode().split(": ")[1]
parts = [token[i:i+16] for i in range(0, len(token), 16)]
parts[3] = parts[1]
p.sendline("".join(parts))
p.interactive()
