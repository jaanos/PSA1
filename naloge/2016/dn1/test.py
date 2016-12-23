from matrix.JanPerme import SlowMatrix
from matrix.JanPerme import FastMatrix
from matrix.JanPerme import CheapMatrix
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
