#from .matrix.VidMegusar import CheapMatrix
from matrix.VidMegusar import FastMatrix
#from .matrix.VidMegusar.slowmatrix import *
from matrix.VidMegusar import SlowMatrix

import time
import random
error = 0

for l in range(20):
    m = random.randint(1,30)
    k = random.randint(1,30)
    n = random.randint(1,30)
    #m, n, k = 17,4,4

    sez1 = []
    sez2 = []
    for i in range(m):
        temp = []
        for j in range(k):
            temp.append(random.randint(-10, 10))
        sez1.append(temp)

    for i in range(k):
        temp = []
        for j in range(n):
            temp.append(random.randint(-10, 10))
        sez2.append(temp)


    A1 = SlowMatrix(sez1)
    B1 = SlowMatrix(sez2)
    C1 = A1*B1
    A2 = FastMatrix(sez1)
    B2 = FastMatrix(sez2)
    C2 = A2 * B2
    #A3 = CheapMatrix(sez1)
    #B3 = CheapMatrix(sez2)
    #C3 = A3 * B3

    #print(l)
    print(m, k, n)
    print('slow fast', C1 == C2, A1 == A2, B1 == B2)
    if C1 != C2:
        error += 1

print(error)
M = FastMatrix([[1,1,1,1],[1,2,3,4]])
K = M[:1,:2]
print(K)
print(M)
K = K*20
print(K)
print(M)

    #print('slow cheap', C1 == C3, A1 == A3, B1 == B3)