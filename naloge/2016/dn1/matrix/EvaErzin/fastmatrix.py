# -*- coding: utf-8 -*-
from slowmatrix import SlowMatrix

class FastMatrix(SlowMatrix):
    """
    Matrika z množenjem s Strassenovim algoritmom.
    """
    def multiply(self, left, right):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Množenje izvede s Strassenovim algoritmom.
        """
        assert left.ncol() == right.nrow(), \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"

        n0 = left.nrow() % 2
        n1, n2 = left.nrow() // 2, left.nrow() - n0
        k0 = left.ncol() % 2
        k1, k2 = left.ncol() // 2, left.ncol() - k0
        m0 = right.ncol() % 2
        m1, m2 = right.ncol() // 2, right.ncol() - m0

        A, B, C, D = left[0 : n1, 0 : k1], \
                     left[0 : n1, k1 : k2], \
                     left[n1 : n2, 0 : k1], \
                     left[n1 : n2, k1 : k2]
        E, F, G, H = right[0 : k1, 0 : m1], \
                     right[0 : k1, m1 : m2], \
                     right[k1 : k2, 0 : m1], \
                     right[k1 : k2, m1 : m2]

        P1 = A * (F - H)
        P2 = (A + B) * H
        P3 = (C + D) * E
        P4 = D * (G - E)
        P5 = (A + D) * (E + H)
        P6 = (B - D) * (G + H)
        P7 = (A - C) * (E + F)


#         print(A)
#         print('---------------------------------------------------')
#         print(B)
#         print('---------------------------------------------------')
#         print(C)
#         print('---------------------------------------------------')
#         print(D)
#         print('---------------------------------------------------')
#         print(E)
#         print('---------------------------------------------------')
#         print(F)
#         print('---------------------------------------------------')
#         print(G)
#         print('---------------------------------------------------')
#         print(H)
#
# X = FastMatrix([[ 1,  2,  3,  4],
#                   [ 5,  6,  7,  8],
#                   [ 9, 10, 11, 12],
#                   [13, 14, 15, 16],
#                   [17, 18, 19, 20]])
#
# Y = FastMatrix([[ 1,  2,  3,  4,  5,  6],
#                   [ 7,  8,  9, 10, 11, 12],
#                   [13, 14, 15, 16, 17, 18],
#                   [19, 20, 21, 22, 23, 24]])
#
# X*Y