# -*- coding: utf-8 -*-
from .slowmatrix import SlowMatrix

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

        if left.nrow() == 1 or left.ncol() == 1 or right.ncol() == 1:
            return super().multiply(left, right)

        n0 = left.nrow() % 2
        n1, n2 = left.nrow() // 2, left.nrow() - n0
        k0 = left.ncol() % 2
        k1, k2 = left.ncol() // 2, left.ncol() - k0
        m0 = right.ncol() % 2
        m1, m2 = right.ncol() // 2, right.ncol() - m0

        A, B, C, D = left[0: n1, 0: k1], \
                     left[0: n1, k1: k2], \
                     left[n1: n2, 0: k1], \
                     left[n1: n2, k1: k2]
        E, F, G, H = right[0: k1, 0: m1], \
                     right[0: k1, m1: m2], \
                     right[k1: k2, 0: m1], \
                     right[k1: k2, m1: m2]

        P1 = A * (F - H)
        P2 = (A + B) * H
        P3 = (C + D) * E
        P4 = D * (G - E)
        P5 = (A + D) * (E + H)
        P6 = (B - D) * (G + H)
        P7 = (A - C) * (E + F)

        if k0 == 0:

            self[0 : n1, 0 : m1] = P4 + P5 + P6 - P2
            self[n1 : n2, 0 : m1] = P3 + P4
            self[0 : n1, m1 : m2] = P1 + P2
            self[n1 : n2, m1 : m2] = P1 + P5 - P3 - P7

            if n0 == 1:
                self[n2, 0: m2 + m0] = left[n2, 0: k2] * right

            if m0 == 1:
                self[0: n2 + n0, m2] = left * right[0: k2, m2]

            return self

        else:

            self[ : , : ] = left[0 : n2 + n0, 0 : k2] * right[0 : k2, 0 : m2 + m0]
            self[ : , : ] += left[0 : n2 + n0, k2] * right[k2, 0 : m2 + m0]

            return self






