#!/usr/local/bin/python

from random import randbytes

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from secrets import FLAG

USERNAME = "user312"
PASSWORD = "hunter"

def serialize_user_token(user_token):
    return (user_token["name"] + "@" +
            user_token["security_question"] + "@" +
            user_token["password"] + "@" +
            user_token["is_admin"])


def reconstruct_user_token(serialized_user_token):
    if serialized_user_token.count("@") != 3:
        raise ValueError("Invalid user token format")
    return {
        "name": serialized_user_token.split("@")[0],
        "security_question": serialized_user_token.split("@")[1],
        "password": serialized_user_token.split("@")[2],
        "is_admin": serialized_user_token.split("@")[3]
    }


print(f"Welcome to my exotic recipe service, {USERNAME}.")
print(f"I've created an account for you, here's your password: {PASSWORD}. Please change it after you login.")
print("If you lose your password, we can help you recover it if you provide the answer to the following security question:")
security_question = input("What is your mother's credit card number, the expiration date, and the three digits on the back? ")

userToken = {
    "name": USERNAME,
    "security_question": security_question,
    "password": PASSWORD,
    "is_admin": "nope"
}

key = randbytes(8)
cipher = DES.new(key, DES.MODE_ECB)
ciphertext = cipher.encrypt(pad(serialize_user_token(userToken).encode(), 8))
print(f"Thank you! Here's your login token: {ciphertext.hex()}")

try:
    token = bytes.fromhex(input("Please enter your token: "))
    plaintext = unpad(cipher.decrypt(token), 8).decode()
    userToken = reconstruct_user_token(plaintext)
except ValueError:
    print("Invalid token")
    exit(1)

if userToken["name"] != USERNAME or userToken["password"] != PASSWORD:
    print("I don't seem to recognize you, please come back another time.")
    exit(1)

if userToken["is_admin"] == "true":
    print("Welcome back! Here's a recipe for you:")
    print("1. Get a bowl")
    print("2. Add cereal")
    print("3. Add milk")
    print("4. Add a cool flag on top, I suggest you try this one:", FLAG)
    print("5. Enjoy!")
else:
    print("Welcome back! Here's a recipe for you:")
    print("1. Get a bowl")
    print("2. Add cereal")
    print("3. Add milk")
    print("4. Enjoy!")


