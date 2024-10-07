#!/usr/local/bin/python
import os

# On your local machine, this will be the fake flag.
# On the server, this will be the real flag.
FLAG = os.getenv("FLAG") or "TUDCTF{FAKE_FLAG}"

thing_to_run = input("What do you want to run? ")

# Prevent the user from executing arbitrary code
if "print" in thing_to_run:
    print("You can't do that!")
    exit(1)

print("We will execute the following code:")
print(thing_to_run)
print("----------------------")

try:
    # Note: this is now exec, not eval
    # https://docs.python.org/3/library/functions.html#exec
    exec(thing_to_run)
except:
    print("An error has occurred while executing your code")

