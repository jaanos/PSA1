from matrix.JanezRadescek import CheapMatrix
from matrix.JanezRadescek import FastMatrix
from matrix.JanezRadescek import SlowMatrix
import time
import random

error = 0
for l in range(80,100,10):
    m = l
    k = m
    n = l

    #m=7
    #k=6
    #n=11

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

    start = time.time()


    #A1 = SlowMatrix(sez1)
    #B1 = SlowMatrix(sez2)
    #C1 = A1 * B1
    #A2 = FastMatrix(sez1)
    #B2 = FastMatrix(sez2)
    #C2 = A2 * B2
    #A3 = CheapMatrix(sez1)
    B3 = CheapMatrix(sez2)
    C3 = A3 * B3

    end = time.time()
    print(l)
    print(end - start)


    #print(m, k, n)
    #print('slow fast', C1 == C2, A1 == A2, B1 == B2)
    #print('slow cheap', C1 == C3, A1 == A3, B1 == B3)
    #print(A1, "konec")
    #print(B1, "konec")
    #print(C1, "konec")
    #print(C3)

print(error)