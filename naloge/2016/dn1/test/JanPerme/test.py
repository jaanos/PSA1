from matrix.JanPerme import SlowMatrix
from matrix.JanPerme import FastMatrix
from matrix.JanPerme import CheapMatrix
import numpy
import time
X = SlowMatrix([[ 1,  2,  3,  4],
                  [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                  [13, 14, 15, 16],
                [17, 18, 19, 20]])
Y = SlowMatrix([[ 1,  2,  3,  4,  5,  6],
                  [ 7,  8,  9, 10, 11, 12],
                  [13, 14, 15, 16, 17, 18],
                  [19, 20, 21, 22, 23, 24]])
print(X * Y)
X2=FastMatrix([[1,2,3],[1,6,7],[1,4,5],[2,3,4]])
Y2=FastMatrix([[5,1,1],[1,6,1],[1,1,6]])
print("------------FastMatrix-------------")
print(X2*Y2)
X3=CheapMatrix([[1,2,3],[1,6,7],[1,4,5],[2,3,4]])
Y3=CheapMatrix([[5,1,1],[1,6,1],[1,1,6]])
print("------------CheapMatrix------------")
print(X3*Y3)

f = open('rcode.txt', 'w')
koda="| n | Slow | Fast | Cheap |\n"
for n in range(1,40,5):
    a=numpy.random.random((n,n))
    b=numpy.random.random((n,n))
    X=SlowMatrix(a.tolist())
    Y=SlowMatrix(b.tolist())
    st=time.time()
    X*Y
    st=time.time()-st
    X=FastMatrix(a.tolist())
    Y=FastMatrix(b.tolist())
    ft=time.time()
    X*Y
    ft=time.time()-ft
    X=CheapMatrix(a.tolist())
    Y=CheapMatrix(b.tolist())
    ct=time.time()
    X*Y
    ct=time.time()-ct
    koda+="| "+str(n)+" | "+str(st)+" | "+str(ft)+" | "+str(ct)+"|\n"
f.write(koda)
f.close()

