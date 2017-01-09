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
        k = left.ncol()
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        m = self.nrow()
        n = self.ncol()
        # k,m,n sem vpeljal, zaradi osebne preglednosti, minimalno skrajsa cas iskanja števila vrstic in stolpcev

        #Konec rekurzije, ko je ena od dimenzij 1 pomnožimo na naiven način
        if (1 in (m, k, n)):
            self[0:m, 0:n] = FastMatrix(SlowMatrix(left)*SlowMatrix(right))

        #Če je število stolpcev ali vrstic liho, matriko razdelimo na sodi del in na zadnjo vrstico/stolpec.
        #V naslednjem koraku rekurzije bomo vrstico/stolpec zmnožili na naiven način, na sodem delu bomo pa uporabili Strassenov algoritem
        elif k % 2 == 1:
            ld = left[0:m, k-1] * right[k-1, 0:n]
            LD = left[0:m, 0:k-1] * right[0:k-1, 0:n]
            self[0:m, 0:n] = LD + ld

        elif m % 2 == 1:
            p = left[m-1, 0:k]
            self[m - 1, 0:n] = p * right
            self[0:m-1, 0:n] = left[0:m-1, 0:k] * right

        elif n % 2 == 1:
            p = right[0:k, n-1]
            self[0:m, n - 1] = left * p
            self[0:m, 0:n-1] = left * right[0:k, 0:n-1]

        #Ko smo gotovi, da so dimenzije obeh matrik sode Uporabimo Strassenov algoritem.
        else:
            A = left[0:m // 2, 0:k // 2]
            B = left[0:m // 2, k // 2:k]
            C = left[m // 2:m, 0:k // 2]
            D = left[m // 2:m, k // 2:k]

            E = right[0:k // 2, 0:n // 2]
            F = right[0:k // 2, n // 2:n]
            G = right[k // 2:k, 0:n // 2]
            H = right[k // 2:k, n // 2:n]

            P1 = A * (F - H) # +1 matika
            P2 = (A + B) * H # +1 matika
            P3 = (C + D) * E # +1 matika
            P4 = D * (G - E) # +1 matika
            P5 = (A + D) * (E + H) # +2 matika
            P6 = (B - D) * (G + H) # +2 matika
            P7 = (A - C) * (E + F) # +2 matika

            self[0:m // 2, 0:n // 2] = P4 + P5 + P6 - P2
            self[0:m // 2, n // 2:n] = P1 + P2
            self[m // 2:m, 0:n // 2] = P3 + P4
            self[m // 2:m, n // 2:n] = P1 + P5 - P3 - P7



