flag = 'S3cUr1tyThr0ughObscur1ty'

alphabet = set(c for c in flag)
states = [f'q{i}' for i in range(len(flag) + 2)]
transitions = []

for i, c in enumerate(flag):
    transitions.append(((states[i], c), states[i + 1]))
    for c2 in alphabet:
        if c2 == c:
            continue
        transitions.append(((states[i], c2), states[-1]))

for c in alphabet:
    transitions.append(((states[-2], c), states[-1]))
    transitions.append(((states[-1], c), states[-1]))

result = '('
# states
result += '{' + ','.join(states) + '}'
result += ','
# alphabet
result += '{' + ','.join(alphabet) + '}'
result += ','
# transitions
result += '{' + ','.join(f'(({a},{b}),{c})' for ((a, b), c) in transitions) + '}'
result += ','
# starting state
result += states[0]
result += ','
# accepting states
result += '{' + states[-2] + '}'
result += ')'
# locations
result += '    ,    '
result += '{' + ','.join(f'{s}:({i * 5};1)' for i, s in enumerate(states[:-1])) + f',{states[-1]}:({(len(states) - 1) * 5 // 2};20)' + '}'

print(result)
