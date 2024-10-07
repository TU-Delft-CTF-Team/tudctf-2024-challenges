from os import environ

print("Hello student, please submit your one-column thesis paper for grading.")

cmd = input()
flagflagflagflag = environ.get("FLAG") or "TUDCTF{this_is_a_fake_flag}"
environ.clear()

banned = "#&\tH$8d@OZzy/ht<CJ}HxpW}b,=<m^\fzCEcnPera0cGUf~EbyZ\fV[{a4+XI\n@xl8'SMU/|L\r \rhoit&-qfAseDJ\\m^]Ilw ,P$\"wqk?ti;!\n!u\"X*WB\r?7j\\D=gs{h+Z%7\vpBP[WG N\tQ!R%yfeW@2$gZ~\\AX\vOAY0Twu3R]r\"+$IQ%=KT5jn\\3aA:J4*1c?cNH2,N`q94B?,b[\rd\vv{9]BQ3`-V\"pb#KNYLn/GJ-Xk1jEusM<s86'F\fI6k\nKTF`:-#2d+0Y;SOwg369i&[:<xp;l!nmE*1DUoSlLD:550vO2h`\vjiKYkS>\t }H\tC]~|'T8|v7MQ}e5F@V4xq'Rg/FoMzmC&>G\n9zV6vd\fLP{%#y>;u1fRU|t>=^a7rro*~^'"


got_caught = False

for c in cmd:
    if c in banned:
        print(f"ACADEMIC FRAUD DETECTED: You got caught committing plagiarism by using the character '{c}', which you took straight from Wikipedia! Andy will soon fire you from this course!")
        got_caught = True

if len(cmd) > 12:
    print("Your one-column thesis paper is too long! It may not exceed 12 characters!")
    got_caught = True

if got_caught:
    exit()

print(f"{eval(cmd)}")