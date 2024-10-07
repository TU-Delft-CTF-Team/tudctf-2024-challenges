#!/usr/local/bin/python
import os

# On your local machine, this will be the fake flag.
# On the server, this will be the real flag.
FLAG = os.getenv("FLAG") or "TUDCTF{FAKE_FLAG}"

thing_to_print = input("What do you want to print? ")

code_to_execute = f'print("{thing_to_print}")'

print("We will execute the following code:")
print(code_to_execute)
print("----------------------")

# https://docs.python.org/3/library/functions.html#eval
eval(code_to_execute)
