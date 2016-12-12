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

        # Za nxn matrike, kjer je n sod:
        n = left.ncol()
        if n == 1:
            self[0,0] = left[0,0] * right[0,0]
        else:
            A = left[0:n//2, 0:n//2]
            B = left[0:n//2, n//2:n]
            C = left[n//2:n, 0:n//2]
            D = left[n//2:n, n//2:n]
            E = right[0:n//2, 0:n//2]
            F = right[0:n//2, n//2:n]
            G = right[n//2:n, 0:n//2]
            H = right[n//2:n, n//2:n]
            P1 = A * (F - H)
            P2 = (A + B) * H
            P3 = (C + D) * E
            P4 = D * (G - E)
            P5 = (A + D) * (E + H)
            P6 = (B - D) * (G + H)
            P7 = (A - C) * (E + F)
            self[0:n//2, 0:n//2] = P4 + P5 + P6 - P2
            self[0:n//2, n//2:n] = P1 + P2
            self[n//2:n, 0:n//2] = P3 + P4
            self[n//2:n, n//2:n] = P1 + P5 - P3 - P7
