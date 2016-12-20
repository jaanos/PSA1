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
        if work is None:
            work = self.__class__(nrow = self.nrow(), ncol = self.ncol())
        else:
            assert self.nrow() == work.nrow() and self.ncol() == work.ncol(), \
               "Dimenzije delovne matrike ne ustrezajo dimenzijam produkta!"

        m = left.ncol()
        n = left.nrow()
        p = right.ncol()
        ms = 2 * (m // 2)  # (ms je sodo stevilo, ki je za 1 manjse od m - ce je m liho, ali enako m - ce je m ze sodo)
        ns = 2 * (n // 2)  # (ns je sodo stevilo, ki je za 1 manjse od n - ce je n liho, ali enako n - ce je n ze sodo)
        ps = 2 * (p // 2)  # (ps je sodo stevilo, ki je za 1 manjse od p - ce je p liho, ali enako p - ce je p ze sodo)
        mc = m // 2
        nc = n // 2
        pc = p // 2

        # Ce imamo v kateri od matrik le en stolpec ali vrstico, potem le zmnozimo, saj ne moremo razdeliti
        if n == 1 or m == 1 or p == 1:
            super().multiply(left, right)

        else:
            A = left[0:n // 2, 0:m // 2]
            B = left[0:n // 2, m // 2:ms]
            C = left[n // 2:ns, 0:m // 2]
            D = left[n // 2:ns, m // 2:ms]
            E = right[0:m // 2, 0:p // 2]
            F = right[0:m // 2, p // 2:ps]
            G = right[m // 2:ms, 0:p // 2]
            H = right[m // 2:ms, p // 2:ps]

            ZL = self[0:n // 2, 0:p // 2]             # zgornja leva podmatrika koncne matrike
            ZD = self[0:n // 2, p // 2:ps]            # zgornja desna podmatrika koncne matrike
            SL = self[n // 2:ns, 0:p // 2]            # spodnja leva podmatrika koncne matrike
            SD = self[n // 2:ns, p // 2:ps]           # spodnja desna podmatrika koncne matrike

            delavna_ZL = work[0:n // 2, 0:p // 2]     # zgornja leva podmatrika delavne matrike
            delavna_ZD = work[0:n // 2, p // 2:ps]    # zgornja desna podmatrika delavne matrike
            delavna_SL = work[n // 2:ns, 0:p // 2]    # spodnja leva podmatrika delavne matrike
            delavna_SD = work[n // 2:ns, p // 2:ps]   # spodnja desna podmatrika delavne matrike

            # Izracun zgornje leve podmatrike produkta (P4 + P5 + P6 - P2)
            # P6 je uporabljena le v zgornji levi podmatriki koncne matrike
            B -= D
            G += H
            ZL.multiply(B, G, delavna_ZL)      # P6 takoj zapisemo v koncno matriko
            B += D
            G -= H

            # P2
            A += B
            ZD.multiply(A, H, delavna_SD)      # P2 zapisemo v zgornjo desno podmatriko, ker jo bomo tam potrebovali
            A -= B

            # P4
            G -= E
            SL.multiply(D, G, delavna_SD)      # P4 zapisemo v spodnjo levo podmatriko, ker jo bomo tam potrebovali
            G += E

            # P5
            A += D
            E += H
            delavna_SL.multiply(A, E, delavna_SD)
            A -= D
            E -= H

            ZL += SL + delavna_SL - ZD

            # Izracun zgornje desne podmatrike produkta (P1 + P2)
            # trenutno je ZD == P2, zato moramo le se pristeti P1

            # P1
            F -= H
            delavna_ZL.multiply(A, F, delavna_SD)
            F += H

            ZD += delavna_ZL

            # Izracun spodnje leve podmatrike produkta (P3 + P4)
            # trenutno je SL == P4, zato mormo le se pristeti P3

            # P3
            C += D
            delavna_ZD.multiply(C, E, delavna_SD)
            C -= D

            SL += delavna_ZD

            # Izracun spodnje desne podmatrike produkta (P3 + P4)

            # P7
            A -= C
            E += F
            SD.multiply(A, E, delavna_SD)
            SD *= -1
            A += C
            E -= F

            # Pristejemo se ostale produkte
            SD += delavna_ZL + delavna_SL - delavna_ZD

            # Ce leva matrika nima sodo stevilo stolpcev, pristejemo se produkte z zadnjim stolpcem
            if m % 2 != 0:
                delavna_ZL.multiply(left[0:nc, m - 1], right[m - 1, 0:pc], delavna_ZD)
                ZL += delavna_ZL
                delavna_ZL.multiply(left[0:nc, m - 1], right[m - 1, pc:ps], delavna_ZD)
                ZD += delavna_ZL
                delavna_ZL.multiply(left[nc:ns, m - 1], right[m - 1, 0:pc], delavna_ZD)
                SL += delavna_ZL
                delavna_ZL.multiply(left[nc:ns, m - 1], right[m - 1, pc:ps], delavna_ZD)
                SD += delavna_ZL

            # Ce desna matrika nima sodega stevila stolpcev, dodamo se te produkte
            if p % 2 != 0:
                self[0:n, p - 1].multiply(left, right[0:m, p - 1], work[0:n, p - 1])

            # Ce leva matrika nima sodega stevila vrstic, rocno obravnavamo zadnjo vrstico
            if n % 2 != 0:
                self[n - 1, 0:ps].multiply(left[n - 1, 0:m], right[0:m, 0:ps], work[n - 1, 0:ps])
