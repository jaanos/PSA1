import time

from matrix.AndrazPirnovar import SlowMatrix
from matrix.AndrazPirnovar import FastMatrix
from matrix.AndrazPirnovar import CheapMatrix

def cas_zah(m,n,k, algoritem = "SM", poskusi = 10):
    casi = []
    if algoritem == "SM":
        A = SlowMatrix([[1 for j in range(n)] for i in range(m)])
        B = SlowMatrix([[1 for j in range(k)] for i in range(n)])
    elif algoritem == "FM":
        A = FastMatrix([[1 for j in range(n)] for i in range(m)])
        B = FastMatrix([[1 for j in range(k)] for i in range(n)])
    elif algoritem =="CM":
        A = CheapMatrix([[1 for j in range(n)] for i in range(m)])
        B = CheapMatrix([[1 for j in range(k)] for i in range(n)])
    #Kolikor je vrednost poskusi, tolikokrat mnozimo in izracunamo povprecje
    for i in range(poskusi):
        zacetek = time.time()
        A*B
        konec = time.time()
        casi.append(konec - zacetek)
    return sum(casi)/poskusi

print("SlowMatrix m=10,n=10,k=10: " + str(cas_zah(10,10,10,"SM")))
print("FastMatrix m=10,n=10,k=10: " + str(cas_zah(10,10,10,"FM")))
print("CheapMatrix m=10,n=10,k=10: " + str(cas_zah(10,10,10,"CM")))

print("SlowMatrix m=25,n=25,k=25: " + str(cas_zah(25,25,25,"SM")))
print("FastMatrix m=25,n=25,k=25: " + str(cas_zah(25,25,25,"FM")))
print("CheapMatrix m=25,n=25,k=25: " + str(cas_zah(25,25,25,"CM")))

print("SlowMatrix m=50,n=50,k=50: " + str(cas_zah(50,50,50,"SM")))
print("FastMatrix m=50,n=50,k=50: " + str(cas_zah(50,50,50,"FM")))
print("CheapMatrix m=50,n=50,k=50: " + str(cas_zah(50,50,50,"CM")))

print("SlowMatrix m=100,n=100,k=100: " + str(cas_zah(100,100,100,"SM")))
print("FastMatrix m=100,n=100,k=100: " + str(cas_zah(100,100,100,"FM")))
print("CheapMatrix m=100,n=100,k=100: " + str(cas_zah(100,100,100,"CM")))

print("SlowMatrix m=250,n=250,k=250: " + str(cas_zah(250,250,250,"SM")))
print("FastMatrix m=250,n=250,k=250: " + str(cas_zah(250,250,250,"FM")))
print("CheapMatrix m=250,n=250,k=250: " + str(cas_zah(250,250,250,"CM")))

print("SlowMatrix m=500,n=500,k=500: " + str(cas_zah(500,500,500,"SM")))
print("FastMatrix m=500,n=500,k=500: " + str(cas_zah(500,500,500,"FM")))
print("CheapMatrix m=500,n=500,k=500: " + str(cas_zah(500,500,500,"CM")))

