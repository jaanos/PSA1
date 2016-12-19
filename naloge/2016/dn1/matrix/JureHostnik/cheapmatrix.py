# -*- coding: utf-8 -*-
from slowmatrix import SlowMatrix

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
        # Rekurzivno množimo ustrezne bloke, podobno kot pri FastMatrix,
        # vendar ne ustvarjamo novih matrik.
        #
        # left  [     |      ]  0        [     |      ]  0   right
        #       [     |      ]           [     |      ]
        #       [------------]  c        [------------]  a
        #       [     |      ]           [     |      ]
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
            
            self[0:c, 0:e] = ((left[0:c, 0:a] + left[c:d, a:b]) * (right[0:a, 0:e] + right[a:b, e:f])) + (left[c:d, a:b] * (right[a:b, 0:e] - right[0:a, 0:e])) - ((left[0:c, 0:a] + left[0:c, a:b]) * right[a:b, e:f]) + ((left[0:c, a:b] - left[c:d, a:b]) * (right[a:b, 0:e] + right[a:b, e:f]))
            self[0:c, e:f] = (left[0:c, 0:a] * (right[0:a, e:f] - right[a:b, e:f])) + ((left[0:c, 0:a] + left[0:c, a:b]) * right[a:b, e:f])
            self[c:d, 0:e] = ((left[c:d, 0:a] + left[c:d, a:b]) * right[0:a, 0:e]) + (left[c:d, a:b] * (right[a:b, 0:e] - right[0:a, 0:e]))
            self[c:d, e:f] = (left[0:c, 0:a] * (right[0:a, e:f] - right[a:b, e:f])) + ((left[0:c, 0:a] + left[c:d, a:b]) * (right[0:a, 0:e] + right[a:b, e:f])) - ((left[c:d, 0:a] + left[c:d, a:b]) * right[0:a, 0:e]) - ((left[0:c, 0:a] - left[c:d, 0:a]) * (right[0:a, 0:e] + right[0:a, e:f]))

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
