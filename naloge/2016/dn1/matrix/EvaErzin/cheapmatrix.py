# -*- coding: utf-8 -*-
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


        if left.nrow() == 1 or left.ncol() == 1 or right.ncol() == 1:
            return super().multiply(left, right)

        #Delovno matriko ustvarimo le, če jo res potrebujemo
        if work is None:
            work = self.__class__(nrow=self.nrow(), ncol=self.ncol())
        else:
            assert self.nrow() == work.nrow() and self.ncol() == work.ncol(), \
                "Dimenzije delovne matrike ne ustrezajo dimenzijam produkta!"

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

        S1, S2, S3, S4 = self[0: n1, 0: m1], \
                         self[0: n1, m1: m2], \
                         self[n1: n2, 0: m1], \
                         self[n1: n2, m1: m2]

        W1, W2, W3, W4 = work[0: n1, 0: m1], \
                         work[0: n1, m1: m2], \
                         work[n1: n2, 0: m1], \
                         work[n1: n2, m1: m2]

        if k0 == 0:

            # Najprej izracunamo P1 in ga zapisemo na ustrezna mesta v ciljni matriki
            # Enako storimo z ostalimi šestimi produkti

            # P1 = A * (F - H)
            F -= H
            W1.multiply(A, F, W2)
            F += H

            S2[:,:] = W1
            S4[:,:] = W1

            # P4 = D * (G - E)
            G -= E
            W1.multiply(D, G, W2)
            G += E

            S1[:,:] = W1
            S3[:,:] = W1

            # P2 = (A + B) * H
            A += B
            W1.multiply(A, H, W2)
            A -= B

            S1[:,:] -= W1
            S2[:,:] += W1

            # P3 = (C + D) * E
            C += D
            W1.multiply(C, E, W2)
            C -= D

            S3[:,:] += W1
            S4[:,:] -= W1

            # P5 = (A + D) * (E + H)
            A += D
            E += H
            W1.multiply(A, E, W2)
            E -= H
            A -= D

            S1[:,:] += W1
            S4[:,:] += W1

            # P6 = (B - D) * (G + H)
            B -= D
            G += H
            W1.multiply(B, G, W2)
            G -= H
            B += D

            S1[:,:] += W1

            # P7 = (A - C) * (E + F)
            A -= C
            E += F
            W1.multiply(A, E, W2)
            E -= F
            A += C

            S4[:,:] -= W1

            if n0 == 1:
                self[n2, 0: m2 + m0].multiply(left[n2,:], right, work[n2, 0 : m2 + m0])

            if m0 == 1:
                self[0: n2 + n0, m2].multiply(left, right[0: k2, m2], work[0 : n2 + n0, m2])

            return self

        else:

            self[:,:].multiply(left[0 : n2 + n0, 0 : k2], right[0 : k2, 0 : m2 + m0], work)
            #Naslednji korak si lahko privoščimo, ker bo prvi pogoj ujel to množenje in ne bo ustvaril nove delovne matrike
            #Tako ne bomo porabili dodatnega prostora
            work.multiply(left[0: n2 + n0, k2], right[k2, 0: m2 + m0])
            self += work

            return self
