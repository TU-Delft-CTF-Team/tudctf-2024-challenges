#!/usr/local/bin/python

from private import FLAG
from Crypto.Util.number import *

def key_gen():
    size = 1024
    e = 65537
    p = getPrime(size)
    q = getPrime(size)
    
    N = p * q
    
    d = pow(e, -1, (p - 1) * (q - 1))
    
    return (N, e, d)

flag = bytes_to_long(FLAG)

N, e, d = key_gen()


def encrypt(p):
    global e, N
    return pow(p, e, N)

def decrypt(c):
    global d, N
    return pow(c, d, N)

if __name__ == "__main__":
    enc_flag = encrypt(flag)
    
    print(f"Here is the encrypted flag: {hex(enc_flag)}", flush=True)
    print(f"Here are the public parameters: {N = }, {e = }")
    print("You have 60 seconds, GO!")
    
    while True:
        print("What do you want to do?")
        print("1) Encrypt anything")
        print("2) Decrypt anything (not the flag)")
        
        user_input = int(input())
        
        if user_input == 1:
            print("Insert a message to encrypt as an hexadecimal integer: ", flush=True, end="")
            msg = int(input(), 16)
            enc_msg = encrypt(msg)
            print(f"Here is your encrypted message: {hex(enc_msg)}", flush=True)    
        elif user_input == 2:
            print("Insert a message to decrypt as an hexadecimal integer: ", flush=True, end="")
            ct = int(input(), 16)
            if ct == enc_flag:
                print("Come on, I will not let you decrypt the flag.")
                continue
            dec_ct = decrypt(ct)
            print(f"Here is your decrypted message: {hex(dec_ct)}", flush=True) 
        else:
            print("Command not found")
    
