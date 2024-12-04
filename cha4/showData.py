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
    print()