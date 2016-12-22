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
        k = left.ncol()
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        if work is None:
            work = self.__class__(nrow = self.nrow(), ncol = self.ncol())
        else:
            assert self.nrow() == work.nrow() and self.ncol() == work.ncol(), \
               "Dimenzije delovne matrike ne ustrezajo dimenzijam produkta!"
        m = self.nrow()
        n = self.ncol()

        # Konec rekurzije, ko je ena od dimenzij 1 pomnožimo na naiven način
        if (1 in (m, k, n)):
            super().multiply(left, right)

        elif k % 2 == 1:
            self.multiply(left[0:m, 0:k-1], right[0:k-1, 0:n], work)
            self += left[0:m, k-1] * right[k-1, 0:n]


        elif m % 2 == 1:
            p = left[m-1, 0:k]
            self[m - 1, 0:n] = p * right
            self[0:m-1, 0:n] = left[0:m-1, 0:k] * right


        elif n % 2 == 1:
            p = right[0:k, n-1]
            self[0:m, n - 1] = left * p
            self[0:m, 0:n-1] = left * right[0:k, 0:n-1]

        else:

            A = left[0:m // 2, 0:k // 2]
            B = left[0:m // 2, k // 2:k]
            C = left[m // 2:m, 0:k // 2]
            D = left[m // 2:m, k // 2:k]

            E = right[0:k // 2, 0:n // 2]
            F = right[0:k // 2, n // 2:n]
            G = right[k // 2:k, 0:n // 2]
            H = right[k // 2:k, n // 2:n]

            P6 = self[0:m//2, 0:n//2]
            P2 = self[0:m//2, n//2:n]
            P4 = self[m//2:m, 0:n//2]
            P1 = self[m//2:m, n//2:n]

            P3 = work[0:m // 2, 0:n // 2]
            P5 = work[0:m // 2, n // 2:n]
            P7 = work[m // 2:m, 0:n // 2]
            M = work[m // 2:m, n // 2:n] #namenjena za množenje

            # porazdelitev komponent za Strassenovo množenje
            # S:    |  W:
            # P6 P2 |  P3 P5
            # P4 P1 |  P7 M

            # P1 = A * (F - H)
            # P2 = (A + B) * H
            # P3 = (C + D) * E
            # P4 = D * (G - E)
            # P5 = (A + D) * (E + H)
            # P6 = (B - D) * (G + H)
            # P7 = (A - C) * (E + F)

            F -= H
            P1.multiply(A, F, M)
            F += H

            A += B
            P2.multiply(A, H, M)
            A -= B

            C += D
            P3.multiply(C, E, M)
            C -= D

            G -= E
            P4.multiply(D, G, M)
            G += E

            A += D
            E += H
            P5.multiply(A, E, M)
            A -= D
            E -= H

            B -= D
            G += H
            P6.multiply(B, G, M)
            B += D
            G -= H

            A -= C
            E += F
            P7.multiply(A, E, M)
            A += C
            E -= F

            #seštevanej/odštevanje
            P6 += P4
            P6 += P5
            P6 -= P2

            P2 += P1

            P4 += P3

            P1 += P5
            P1 -= P3
            P1 -= P7



