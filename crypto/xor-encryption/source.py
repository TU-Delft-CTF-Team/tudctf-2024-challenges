#!/usr/local/bin/python

from secrets import token_bytes
from private import FLAG

length = len(FLAG)

key = token_bytes(length)

def encrypt(byte_string, key):
    return bytes(a ^ b for a, b in zip(byte_string, key))

if __name__ == "__main__":
    enc_flag = encrypt(FLAG, key)
    
    print(f"Here is the encrypted flag: {enc_flag}", flush=True)
    print("Now insert a string to encrypt: ", flush=True, end='')
    user_input = bytes(input(), 'utf-8')
    
    enc_input = encrypt(user_input, key) 
    print(f"Here is the encrypted input: {enc_input}", flush=True)
    print("Bye-bye!", flush=True)
    
