from Crypto.Cipher import ARC4

cipher = ARC4.new(b'\x21\x37\x69\x42amogus')
encrypted_flag = cipher.encrypt(b'TUDCTF{br4nch1355_r3v3r53_3ng1n33r1ng_ch4113ng3_1_h0p3_y0u_d0nt_h4t3_m3_t00_much_f0r_th15_:D}')

print(encrypted_flag.hex())

with open('flag_checking_round.txt', 'rt') as f:
    template = f.read()

with open('flag_checking_all_rounds.txt', 'wt') as f:
    for i, c in enumerate(encrypted_flag):
        f.write(template.format(i=i, chr=c))