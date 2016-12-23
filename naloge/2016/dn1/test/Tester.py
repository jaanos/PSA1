from matrix.KevinStampar import CheapMatrix as CHP
from matrix.KevinStampar import SlowMatrix as SM
from matrix.KevinStampar import FastMatrix as FM
import time
from matrix import AbstractMatrix
import random

def randomMatrix(v,s):
    matrika1 = SM(None,v,s)
    matrika2 = FM(None,v,s)
    matrika3 = CHP(None,v,s)
    i=0
    while(i<v):
        j=0
        while(j<s):
            ranint = random.randint(0,10)
            matrika1[i, j] = ranint
            matrika2[i, j] = ranint
            matrika3[i, j] = ranint

            j = j + 1
        i = i + 1
    return (matrika1,matrika2,matrika3)


def testiraj(stTestov,minDim,maxDim=None):
    if (maxDim==None):
        maxDim = minDim
    i=0
    while(i<stTestov):
        v1=random.randint(minDim,maxDim)
        s1=random.randint(minDim,maxDim)
        s2=random.randint(minDim,maxDim)
        (Slow1,Fast1,Cheap1) = randomMatrix(v1,s1)
        (Slow2, Fast2, Cheap2) = randomMatrix(s1, s2)



        print("Test #" + str(i+1))

        print('Naivno mnozenje je porabilo:')
        start = time.clock()
        naivniZmnozek = Slow1 * Slow2
        stop = time.clock()
        print(stop-start)

        start = time.clock()
        fastZmnozek = Fast1*Fast2
        stop = time.clock()

        print('Hitro mnozenje je porabilo:')
        print(stop - start)

        start = time.clock()
        poceniZmnozek = Cheap1*Cheap2
        stop = time.clock()

        print('Poceni mnozenje je porabilo:')
        print(stop - start)
        print('Preverjam resitve')

        if(naivniZmnozek._data != poceniZmnozek._data or naivniZmnozek._data != fastZmnozek._data):
            print('Zmnozki so napacni!')
        else:
            print('PRAVILNO ZMNOZENO!')
        print('-------------')
        print('\n')



        i = i + 1



