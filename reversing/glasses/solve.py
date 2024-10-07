from itertools import cycle

encryptedCore = "#==\v1t\v?p\"a\u001b$'t3'p98w&`\u001b#fp&\n#8a7'fq"
key = "TUD"

flag = "TUDCTF{" + "".join([chr(ord(a) ^ ord(b)) for a, b in zip(encryptedCore, cycle(key))]) + "}"
print(flag)