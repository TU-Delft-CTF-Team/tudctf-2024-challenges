from pwn import *
import concurrent.futures
import time

def attempt(flag):
    context.log_level = 'critical'
    p = remote("localhost", 50123)
    p.recvuntil(b"Please enter the flag:\n")
    p.sendline(flag)
    p.recvuntil(b"Checking...")
    start = time.time_ns()
    p.recvuntil(b"Goodbye!")
    end = time.time_ns()
    p.close()
    return flag, int((end - start) / 1e6) # convert to ms


curr_flag = b"TUDCTF{"
max_time = attempt(curr_flag)[1]
alphabet = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789}"

while curr_flag.find(b"}") == -1:
    flag_jobs = [curr_flag + bytes([c]) for c in alphabet]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        times = list(executor.map(attempt, flag_jobs))
        curr_flag, max_time = max(times, key = lambda t: t[1])
        print(curr_flag)
