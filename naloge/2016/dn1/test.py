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
X2=FastMatrix([[1,7,34,5],[8,13,2,6],[2,2,2,8],[2,2,2,8]])
Y2=FastMatrix([[1,7,4,4],[1,4,4,4],[1,1,4,4],[1,1,4,4]])
print(X2*Y2)
X3=CheapMatrix([[1,7,34,5],[8,13,2,6],[2,2,2,8],[2,2,2,8]])
Y3=CheapMatrix([[1,7,4,4],[1,4,4,4],[1,1,4,4],[1,1,4,4]])
print(X3*Y3)
