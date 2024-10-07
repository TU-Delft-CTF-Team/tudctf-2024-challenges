from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long
import os

FLAG = os.getenv('FLAG', "TUDCTF{FAKE_FLAG}")
incriminating_message = b'I hereby declare that I don\'t like coatis!1'
operations_left = 4


def sign(m):
    if incriminating_message in m:
        return None
    m = bytes_to_long(m)
    return long_to_bytes(pow(m, d, N))


def verify(s):
    s = bytes_to_long(s)
    m = pow(s, e, N)
    m = long_to_bytes(m)
    return m


if __name__ == '__main__':
    p, q = getPrime(1024), getPrime(1024)
    N = p * q
    e = 65537
    d = pow(e, -1, (p - 1) * (q - 1))

    while True:
        if operations_left == 0:
            print('I got bored, no more signing or verifying for you')
            break
        print('What do you want to do?\n1) Sign a message\n2) Get the flag\n3) Quit')
        try:
            choice = int(input('> '))
            if choice == 1:
                operations_left -= 1
                m = bytes.fromhex(input('Your message (hex): '))
                if bytes_to_long(m) > N:
                    print('Your message is too big, sorry!')
                    continue
                s = sign(m)
                if s is None:
                    print('Nice try! But I won\'t sign a message that incriminates me.')
                else:
                    print(s.hex())
            elif choice == 2:
                operations_left -= 1
                s = bytes.fromhex(input('Your signature (hex): '))
                if bytes_to_long(s) > N:
                    print('I don\'t recall signing anything this long 🤨')
                    continue
                m = verify(s)
                if m == incriminating_message:
                    print(f'What the hell did I sign 😳? Here\'s the flag, in return please don\'t show this incriminating signature to anyone: {FLAG}')
                    break
                else:
                    print(f'So I said {m.hex()}. Ok, and?')
            elif choice == 3:
                print('Bye!')
                break
            else:
                raise ValueError
        except ValueError:
            print('Invalid choice!')
