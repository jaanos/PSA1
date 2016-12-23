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

        m = left.nrow()  # št. vrstic leve matrike
        n = right.nrow() # št. stolpcev leve = št. vrstic desne matrike
        o = right.ncol() # št. stolpcev desne matrike

        # Če je katera od dimenzij 0, naredimo skalarni produkt.
        if m * n * o == 0:
            for i in range(m):
                for j in range(o):
                    self[i, j] = sum(left[i, k]*right[k, j] for k in range(n))

        # Če sta matriki dimenzij 1x1, zmnožimo skalarje.
        elif m * n * o == 1:
            self[0, 0] = left[0, 0] * right[0, 0]

        # Če je katera od dimenzij liha, spustimo ustrezen stolpec
        # ali vrstico.
        # Rekurzivno množimo ustrezne bloke.
        #
        # left  [  A  |  B   ]  0        [  E  |  F   ]  0   right
        #       [     |      ]           [     |      ]
        #       [------------]  c        [------------]  a
        #       [  C  |  D   ]           [  G  |  H   ]
        #       [     |      ]  d        [     |      ]  b
        #
        #       0     a      b           0     e      f
        else:
            a = n//2
            b = n - (n % 2)
            c = m//2
            d = m - (m % 2)
            e = o//2
            f = o - (o % 2)
            
            A = left[0:c, 0:a]
            B = left[0:c, a:b]
            C = left[c:d, 0:a]
            D = left[c:d, a:b]
            E = right[0:a, 0:e]
            F = right[0:a, e:f]
            G = right[a:b, 0:e]
            H = right[a:b, e:f]

            P7 = (A - C) * (E + F)
            P6 = (B - D) * (G + H)
            P5 = (A + D) * (E + H)
            P4 = D * (G - E)
            P3 = (C + D) * E
            P2 = (A + B) * H
            P1 = A * (F - H)
            
            self[0:c, 0:e] = P5 + P4 - P2 + P6
            self[0:c, e:f] = P1 + P2
            self[c:d, 0:e] = P3 + P4
            self[c:d, e:f] = P1 + P5 - P3 - P7

            # Če je n liho, vsem elementom prištejemo ustrezen produkt.
            if n % 2 == 1:
                for i in range(m):
                    for j in range(o):
                        self[i, j] += left[i, n-1]*right[n-1, j]

            # Če je m liho, izračunamo še spodnjo vrstico.
            if m % 2 == 1:
                for j in range(o):
                    self[m-1, j] = sum(left[m-1, k]*right[k, j] for k in range(n))

            # Če je o liho, izračunamo še zadnji stolpec.
            if o % 2 == 1:
                for i in range(m):
                    self[i, o-1] = sum(left[i, k]*right[k, o-1] for k in range(n))
