import pickle

flag = 'TUDCTF{put_the_flag_here}'

with open('challenge.pickle', 'rb') as f:
    is_correct = pickle.load(f)

if is_correct:
    print('Congratulations!')
else:
    print('Try again :/')
