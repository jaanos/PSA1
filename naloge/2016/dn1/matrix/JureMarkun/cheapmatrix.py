# -*- coding: utf-8 -*-
import time
from .slowmatrix import SlowMatrix
from .fastmatrix2 import FastMatrix2 as FastMatrix
from ..matrix import AbstractMatrix
import timeit
import numpy

class CheapMatrix(SlowMatrix):
    """
    Matrika z množenjem s Strassenovim algoritmom.
    """
    def multiply(self, left, right, work=None):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Množenje izvede s Strassenovim algoritmom.
        """
        assert left.ncol() == right.nrow(), \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        if work is None:
            work = self.__class__(nrow = self.nrow(), ncol = self.ncol())
        else:
            assert self.nrow() == work.nrow() and self.ncol() == work.ncol(), \
               "Dimenzije delovne matrike ne ustrezajo dimenzijam produkta!"
        l = right.ncol()  # št.stolpcev prve = št.vrstic druge
        n = left.nrow() #št.vrstic prve
        m = right.nrow()  #št.stolpcev druge

        #skica
        #      m                l               l
        #   [       ]       [        ]      [       ]
        # n [       ]   * m [        ] =  n [       ]
        #   [       ]       [        ]      [       ]
        n2 = 0
        l2 = 0
        m2 = 0
        #n2,m2 in l2 predstavljajo največje število, ki je večkratnik 2 in manjše od indeksov n,m in l
        if n%2==0:
            n2 = n
        else:
            n2 = (n-1)
        if m%2==0:
            m2 = m
        else:
            m2 = (m-1)
        if l%2==0:
            l2 = l
        else:
            l2 = (l-1)

        if l==1 or n==1 or m==1: #robni pogoj, ko postane eden od parametrov l,m ali n enak 1. V tem primeru uporabimo naivno množenj
            C = SlowMatrix.multiply(self,left,right)
            return C
        else: #primer, kjer nobena od komponent ni enaka 1
            C = AbstractMatrix([([0, ] * l), ]*n) #velikost ciljne matrike. Moral bi biti self, vendar potem pride narobe.
            A11 = left[0:(n2//2),0:(m2//2)] #razdelitev bločnega dela leve matrike na štiri enako veliko matrike
            A12 = left[0:n2//2,(m2//2):m2]
            A21 = left[n2//2:n2,0:m2//2]
            A22 = left[n2//2:n2,m2//2:m2]

            B11 = right[0:(m2//2),0:(l2//2)] #razdelitev bločnega dela desnega matrike na štiri enako veliko matrike
            B12 = right[0:m2//2,(l2//2):l2]
            B21 = right[m2//2:m2,0:l2//2]
            B22 = right[m2//2:m2,l2//2:l2]

            #Na tej točki se začne koda cheapmatrix razlikovati od fastmatrix

            W11 = work[0:(n2 // 2), 0:(l2 // 2)]
            W12 = work[0:(n2 // 2), (l2 // 2):l2]
            W21 = work[(n2 // 2):n2, 0:(l2 // 2)]
            W22 = work[(n2 // 2):n2, (l2 // 2):l2]

            work[0:work.nrow(), 0:work.ncol()] = 0
            #Sedaj bomo vsako Matriko Mi posebej izračunali, saj ne smemo uporabiti seštevanja dveh matrik, tako kot prej, ker to ustvari novo matriko.

            #M7
            CheapMatrix.multiply(W11,(A12 - A22),(B21 + B22),W12)
            W12[0:(n2 // 2), 0:(l2 // 2)] = 0
            self += work
            work[0:n2, 0:l2] = 0

            #M6
            CheapMatrix.multiply(W22,(A21 - A11), (B11 + B12),W21)
            W21[:(n2 // 2), 0:(l2 // 2)] = 0
            self += work
            work[0:n2, 0:l2] = 0


            #M4
            CheapMatrix.multiply(W11,(A22), (B21 - B11), W21)
            W21[0:(n2 // 2), 0:(l2 // 2)] = W11[0:(n2 // 2), 0:(l2 // 2)]
            self += work
            work[0:n2, 0:l2] = 0

            #M3
            CheapMatrix.multiply(W12,(A11), (B12 - B22), W22)
            W22[0:(n2 // 2), 0:(l2 // 2)] = W12[0:(n2 // 2), 0:(l2 // 2)]
            self += work
            work[0:n2, 0:l2] = 0

            #M5
            CheapMatrix.multiply(W12,(A11 + A12), (B22), W11)
            W11[0:(n2 // 2), 0:(l2 // 2)] -= W12[0:(n2 // 2), 0:(l2 // 2)]
            self += work
            work[0:n2, 0:l2] = 0

            #M2
            CheapMatrix.multiply(W21,(A21 + A22),(B11), W22)
            W22[0:(n2 // 2), 0:(l2 // 2)] -= W21[0:(n2 // 2), 0:(l2 // 2)]
            self += work
            work[0:n2, 0:l2] = 0

            #M1
            CheapMatrix.multiply(W11,(A11 + A22), (B11 + B22), W22)
            W22[0:(n2 // 2), 0:(l2 // 2)] = W11[0:(n2 // 2), 0:(l2 // 2)]
            W21[0:W21.nrow(), 0:W21.ncol()] = 0
            W12[0:W12.nrow(), 0:W12.ncol()] = 0
            self += work
            work[0:n2, 0:l2] = 0

            #odvečni deli, ki niso deli bloka
            #print(n, m,l)
            for n1 in range(n):
                for l1 in range(l):
                    for m1 in range(m):
                        #print(n1,n-n2,"nji",m1, m-m2,"mji", l1, l - l2, "lji")
                        if not (n1 < n2 and m1 < m2 and l1 < l2):
                            self[n1, l1] += left[n1, m1] * right[m1, l1]
            return self

#
#
#
# A = AbstractMatrix([[1, 2, 3, 4],
#     [5, 6, 7, 8],
#     [9, 10, 11, 12],
#     [13, 14, 15, 16],
#     [3,3,3,3]])
# B = AbstractMatrix([[1, 2, 3, 4],
#      [5, 6, 7, 8],
#      [9, 10, 11, 12],
#      [13, 14, 15, 16]])
# F = AbstractMatrix([[0, 0, 0, 0],
#      [0, 0, 0, 0],
#      [0, 0, 0, 0],
#      [0, 0, 0, 0],
#      [0,0,0,0]])
#print(SlowMatrix.multiply(F,A,B))
#print(FastMatrix.multiply(F,A,B))

# T = AbstractMatrix([[1,2,1,0,0,3,3,3,3,3,5,3,4,5],
#                     [2,1,0,1,0,4,5,6,7,8,8,3,4,5],
#                     [1,2,5,3,3,5,5,6,2,7,7,3,3,7],
#                     [2, 1, 0, 1, 0, 4, 5, 6, 7, 8, 8,4,5,4],
#                     [2, 1, 0, 1, 0, 4, 5, 6, 7, 8, 8,3,2,4]])
# S = AbstractMatrix([[2,8,2,0,0,1,2],
#                     [1,3,0,1,8,5,2],
#                     [0,2,0,1,0,1,2],
#                     [2,1,2,1,2,1,2],
#                     [3,4,6,2,3,1,3],
#                     [2, 1, 2, 1, 2, 1, 2],
#                     [2, 1, 2, 1, 2, 1, 2],
#                     [2, 1, 2, 1, 2, 1, 2],
#                     [2, 1, 2, 1, 2, 1, 2],
#                     [2, 1, 2, 1, 2, 1, 2],
#                     [2, 1, 2, 1, 2, 1, 2],
#                     [2, 1, 2, 1, 2, 1, 2],
#                     [2, 1, 2, 1, 2, 1, 2],
#                     [2, 1, 2, 1, 2, 1, 2]])
# U = AbstractMatrix([([0, ] * 7), ] * 5)

#print(SlowMatrix.multiply(U,T,S))

#start = time.time()
#print(CheapMatrix.multiply(U,T,S),"Cheap")
#end = time.time()
#print(end - start,"tempus")