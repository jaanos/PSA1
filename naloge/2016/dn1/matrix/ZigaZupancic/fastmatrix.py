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

        m = left.ncol()
        n = left.nrow()
        p = right.ncol()
        ms = 2*(m//2)  # (ms je sodo stevilo, ki je za 1 manjse od m - ce je m liho, ali enako m - ce je m ze sodo)
        ns = 2*(n//2)  # (ns je sodo stevilo, ki je za 1 manjse od n - ce je n liho, ali enako n - ce je n ze sodo)
        ps = 2*(p//2)  # (ps je sodo stevilo, ki je za 1 manjse od p - ce je p liho, ali enako p - ce je p ze sodo)

        # Ce imamo v kateri od matrik le en stolpec ali vrstico, potem le zmnozimo, saj ne moremo razdeliti
        if n == 1 or m == 1 or p == 1:
            super().multiply(left, right)

        else:
            A = left[0:n//2, 0:m//2]
            B = left[0:n//2, m//2:ms]
            C = left[n//2:ns, 0:m//2]
            D = left[n//2:ns, m//2:ms]
            E = right[0:m//2, 0:p//2]
            F = right[0:m//2, p//2:ps]
            G = right[m//2:ms, 0:p//2]
            H = right[m//2:ms, p//2:ps]
            P1 = A * (F - H)
            P2 = (A + B) * H
            P3 = (C + D) * E
            P4 = D * (G - E)
            P5 = (A + D) * (E + H)
            P6 = (B - D) * (G + H)
            P7 = (A - C) * (E + F)

            zgoraj_levo = 0
            zgoraj_desno = 0
            spodaj_levo = 0
            spodaj_desno = 0

            # Ce leva matrika nima sodo stevilo stolpcev, pristejemo se produkte z zadnjim stolpcem
            if m % 2 != 0:
                zgoraj_levo = left[0:n//2, m-1] * right[m-1, 0:p//2]
                zgoraj_desno = left[0:n//2, m-1] * right[m-1, p//2:ps]
                spodaj_levo = left[n//2:ns, m-1] * right[m-1, 0:p//2]
                spodaj_desno = left[n//2:ns, m-1] * right[m-1, p//2:ps]

            # Ce desna matrika nima sodega stevila stolpcev, dodamo se te produkte
            if p % 2 != 0:
                self[0:n, p - 1] = left * right[0:m, p - 1]

            # Ce leva matrika nima sodega stevila vrstic, rocno obravnavamo zadnjo vrstico
            if n % 2 != 0:
                self[n-1, 0:ps] = left[n-1, 0:m] * right[0:m, 0:ps]

            self[0:n//2, 0:p//2] = P4 + P5 + P6 - P2 + zgoraj_levo
            self[0:n//2, p//2:ps] = P1 + P2 + zgoraj_desno
            self[n//2:ns, 0:p//2] = P3 + P4 + spodaj_levo
            self[n//2:ns, p//2:ps] = P1 + P5 - P3 - P7 + spodaj_desno
