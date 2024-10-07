#!/usr/bin/python3

from flag import FLAG

from Crypto.Random.random import getrandbits
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pss

def main():
    print("Welcome to the Secure Good Luck Verification Protocol!")
    print("The flag will only be revealed to the luckiest of all.")
    print("We use a secure die rolling protocol, so we are both sure neither of us is cheating!")
    print("Good luck, and who knows, maybe even have a little bit of fun!")

    n = int(input("Provide your N: "))

    if n.bit_length() < 1024:
        print("This is not secure enough!")
        return

    e = 65537
    print(f"{e = }")
    key = RSA.construct((n, e))
    s = pss.new(key)

    def sign(message):
        return s.sign(SHA256.new(message))

    def verify(signature, message):
        try:
            s.verify(SHA256.new(message), signature)
        except:
            return False
        return True

    print("We will now securely roll a die together such that neither of us can cheat. You can't predict my number; I can't predict your signature.")

    for rnd in range(20):
        print(f"Round {rnd + 1}/20")

        r = getrandbits(1024)
        print(f"{r = }")
        signature = bytes.fromhex(input("Please sign my number (hex): "))

        if not verify(signature, r.to_bytes(128, byteorder='big')):
            print("Wrong signature!")
            return

        result = int.from_bytes(SHA256.new(signature).digest(), byteorder='big') % 6 + 1

        if result != 6:
            print(f"Skill issue, you only rolled a {result}!")
            return


    print("Wow, you truly are the luckiest of all!")
    print("Here's a flag:")
    print(FLAG)

if __name__ == "__main__":
    main()