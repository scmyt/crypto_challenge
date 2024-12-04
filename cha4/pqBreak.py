import re

N = []
E = []
C = []

for i in range(21):
    with open("Data/Frame"+str(i), "r") as f:
        tmp = f.read()
        N.append(int(tmp[0:256], 16))
        E.append(int(tmp[256:512], 16))
        C.append(int(tmp[512:768], 16))

for i in range(21):
    print("Frame", i)
    print('n = ', N[i])
    print('e = ', E[i])
    print('c = ', C[i])
    
with open('pq.txt', 'r') as fp:
    data = fp.read()
    p = [int(i) for i in re.findall(r'p=([0-9]+)', data)]
    q = [int(i) for i in re.findall(r'q=([0-9]+)', data)]
    pq = list(zip(p, q))

cN = [i * j for i, j in pq]
if [i for i in range(21) if cN[i] != N[i]]:
    print('[!!!]You are wrong!!')
else:
    print('[!]Well done in pq')

print('[+]Hacking Frame...')

print('  [-]Calculating Phi...', end='')
Phi = [(i - 1) * (j - 1) for i, j in pq]
print('Done!')

print('  [-]Calculating d...', end='')
D = [pow(E[i], -1, Phi[i]) for i in range(21)]
print('Done!')

print('  [-]Hacking m...', end='')
M = [('%x' % pow(C[i], D[i], N[i])) for i in range(21)]
print('Done!')

print('[+]All data is:')
for i, m in enumerate(M):
    print('  [-]Frame%d' % i)
    print('    [-]p:', '%x' % pq[i][0])
    print('    [-]q:', '%x' % pq[i][1])
    print('    [-]n:', '%x' % N[i])
    print('    [-]f:', '%x' % Phi[i])
    print('    [-]e:', '%x' % E[i])
    print('    [-]d:', '%x' % D[i])
    print('    [-]m:', m)
    print('    [-]c:', '%x' % C[i])

plain = ""
print('[!]plain text is:')
for m in sorted(set(M)):
    print(m[-16:])
    hex_string = m[-16:]
    hex_pairs = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    ascii_chars = [chr(int(pair, 16)) for pair in hex_pairs]
    resulting_string = ''.join(ascii_chars)
    print(resulting_string)
    plain+=resulting_string

print('[!]The Password is:', plain)

