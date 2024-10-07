import os
from hashlib import sha256
from random import Random

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

FLAG = os.getenv("FLAG") or "TUDCTF{FAKE_FLAG}"

keep_iv_left = 10
rng = None


def get_option():
    print("\nWhat do you want to do next?")
    print("1. Encrypt a secret message")
    print("2. Decrypt a secret message")
    print("3. Get a challenge")
    print("4. Quit")
    return int(input("> "))


def encrypt():
    global keep_iv_left
    msg = bytes.fromhex(input("Your message (hex): "))
    key = bytes.fromhex(input("Your key (hex): "))
    keep_iv = input("Keep the whole IV (y/n)? ") == "y"
    iv = rng.randbytes(16)
    if keep_iv:
        if keep_iv_left <= 0:
            print("Don't be too greedy")
            return
        keep_iv_left -= 1
    else:
        iv = iv[-1:7:-1] + iv[8:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(msg, 16))
    print("The ciphertext is:", ct.hex(), "with iv:", iv.hex())


def decrypt():
    ct = bytes.fromhex(input("Your ciphertext (hex): "))
    key = bytes.fromhex(input("Your key (hex): "))
    iv = bytes.fromhex(input("Your IV (hex): "))
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = unpad(cipher.decrypt(ct), 16)
    print("The plaintext is:", msg.hex())


def challenge(key):
    secret = rng.randbytes(48)
    cipher = AES.new(key, AES.MODE_ECB)
    ct = cipher.encrypt(secret)
    print(ct.hex())
    for _ in range(3):
        guess = bytes.fromhex(input("What's the secret (hex)? "))
        if secret != guess:
            print("Oh, I don't think so")
        else:
            print("o_O")
            return True
    return False


def round():
    global rng
    rng = Random()
    key = sha256(rng.randbytes(8)).digest()[:16]
    while True:
        option = get_option()
        try:
            if option == 1:
                encrypt()
            elif option == 2:
                decrypt()
            elif option == 3:
                return challenge(key)
            elif option == 4:
                exit()
            else:
                print("Invalid option!")
        except ValueError:
            print("Something went wrong")


def main():
    for i in range(10):
        print(f"Round {i + 1}/10")
        if not round():
            print("Tough luck!")
            return
    print(FLAG)


if __name__ == "__main__":
    main()
