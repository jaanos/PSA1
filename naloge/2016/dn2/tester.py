import random
import time
from KevinStampar import maxCycleTreeIndependentSet

def randomTree(k,binary=False):
    seznam=[]
    for i in range(k):
        seznam.append([])
    i=1
    while i<k:
        a = random.randint(0,i-1)
        if binary:
            if len(seznam[a])<3:
                seznam[a] += [i]
                seznam[i] += [a]
                i += 1

        else:
            seznam[a] +=[i]
            seznam[i] +=[a]
            i+=1
    return seznam

def randomWeights(n,k):
    seznam=[]
    for i in range(k):
        vrstica=[]
        for j in range(n):
            vrstica+=[random.randint(0,15)]
        seznam.append(vrstica)
    return seznam


def testTimeMaxCycle(tuple1,tuple2):
    (zac1,konec1,korak1)=tuple1
    (zac2,konec2,korak2)=tuple2
    seznam=[]
    for i in range((konec1-zac1)//korak1):
        seznam.append([0]*((konec2-zac2)//korak2))
    print('Dimenzija drevesa|Dimenzija cikla|Porabljeni cas')
    counterTree=0
    for i in range(zac1,konec1,korak1):
        counterCycle=0
        for j in range(zac2,konec2,korak2):
            T=randomTree(i)
            w=randomWeights(i,j)
            start=time.clock()
            maxCycleTreeIndependentSet(T,w)
            stop=time.clock()
            seznam[counterTree][counterCycle] = stop-start
            print(str(i) + '               |' +str(j)+'              |' + str(stop-start))
            counterCycle+=1
        counterTree+=1    
    return seznam

seznam = testTimeMaxCycle((40,100,20),(5,15,1))

i=1
while i<len(seznam):
    j=1
    print('Vrstica '+str(i))
    while j<len(seznam[0]):
        print(seznam[i][j] - seznam[i-1][j])
        j+=1
    i+=1
