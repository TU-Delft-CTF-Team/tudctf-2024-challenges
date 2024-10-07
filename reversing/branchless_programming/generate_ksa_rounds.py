with open('ksa_round.txt', 'rt') as f:
    template = f.read()

with open('ksa_all_rounds.txt', 'wt') as f:
    for i in range(256):
        f.write(template.format(i=i, imod=i%10))
