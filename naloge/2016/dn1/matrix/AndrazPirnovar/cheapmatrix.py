# -*- coding: utf-8 -*-
#try:
#    from .slowmatrix import SlowMatrix
#except(SystemError):
#    from slowmatrix import SlowMatrix

from .slowmatrix import SlowMatrix

class CheapMatrix(SlowMatrix):
    """
    Matrika s prostorsko nepotratnim množenjem.
    """
    def multiply(self, left, right, work = None):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Kot neobvezen argument lahko podamo še delovno matriko.
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
        #raise NotImplementedError("Naredi sam!")

        m, n, k  = left.nrow(), left.ncol(), right.ncol()       #Dimenzije matrik
        m1, n1, k1 = m//2, n//2, k//2                           #Dimenzije novih blocnih matrik
        m2, n2, k2 = m1*2, n1*2, k1*2

        """Navadno množenje z vektorjem"""
        if m == 1 or n == 1 or k == 1:          # Če je ena izmed dimenzij = 1 => vsaj ena je vektor
            super().multiply(left,right)       #Iz SlowMatrix podedujemo multiply

        else:

            """Naredimo si blocne matrike"""
            A = left[0:m1, 0:n1]
            B = left[0:m1, n1:n2]
            C = left[m1:m2, 0:n1]
            D = left[m1:m2, n1:n2]
            E = right[0:n1, 0:k1]
            F = right[0:n1, k1:k2]
            G = right[n1:n2, 0:k1]
            H = right[n1:n2, k1:k2]

            """Pripravimo si delovne matrike"""
            W1 = work[0:m1,0:k1]
            W2 = work[0:m1,k1:k2]
            W3 = work[m1:m2,0:k1]
            W4 = work[m1:m2,k1:k2]

            """Pripravimo si ciljno matriko"""
            S1 = self[0:m1,0:k1]
            S2 = self[0:m1,k1:k2]
            S3 = self[m1:m2,0:k1]
            S4 = self[m1:m2,k1:k2]

            """Izracunamo clene za Strassnov"""
