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

        # Matrike so velikosti:
        # left: leva x skupna
        # right: skupna x desna

        leva = left.nrow()
        leva2 = leva // 2
        levasoda = 2 * leva2
        skupna = left.ncol()
        skupna2 = skupna // 2
        skupnasoda = 2 * skupna2
        desna = right.ncol()
        desna2 = desna // 2
        desnasoda = 2 * desna2

        if leva == 1 or skupna == 1 or desna == 1:
            return super().multiply(left, right)

        # Razdelimo left
        a = left[0:leva2, 0:skupna2]
        b = left[0:leva2, skupna2:2 * skupna2]
        c = left[leva2:2 * leva2, 0:skupna2]
        d = left[leva2:2 * leva2, skupna2:2 * skupna2]
        # Razdelimo right
        e = right[0:skupna2, 0:desna2]
        f = right[0:skupna2, desna2:2 * desna2]
        g = right[skupna2:2 * skupna2, 0:desna2]
        h = right[skupna2:2 * skupna2, desna2:2 * desna2]
        # Razdelimo self
        c11 = self[0:leva2, 0:desna2]
        c12 = self[0:leva2, desna2:2*desna2]
        c21 = self[leva2:2*leva2, 0:desna2]
        c22 = self[leva2:2*leva2, desna2:2*desna2]
        # Razdelimo work
        d11 = work[0:leva2, 0:desna2]
        d12 = work[0:leva2, desna2:2 * desna2]
        d21 = work[leva2:2 * leva2, 0:desna2]
        d22 = work[leva2:2 * leva2, desna2:2 * desna2]

        # Racunamo c11 += p6
        b -= d
        g += h
        c11.multiply(b, g, d22)
        b +=d
        g -= h

        # Racunamo c12 = p1
        f -= h
        c12.multiply(a, f, d22)
        f += h

        # Racunamo c21 = p3
        c += d
        c21.multiply(c, e, d22)
        c -= d

        # Racunamo c22 = p7
        c -= a # da dobimo -
        e += f
        c22.multiply(c, e, d22)
        e -= f
        c += a

        # Racunamo c22 = p1 - p3
        c22 += c12
        c22 -= c21

        # Shranimo p2, p4, p5 v work
        a += b
        d11.multiply(a, h, d22)
        a -= b
        g -= e
        d12.multiply(d, g, d22)
        g += e
        a += d
        e += h
        d21.multiply(a, e, d22)
        a -= d
        e -= h

        # Racunamo c11 = c11 + p5 + p4 - p2
        c11 -= d11
        c11 += d12
        c11 += d21

        # Racunamo c12 = c12 + p2
        c12 += d11

        # Racunamo c21 = c21 + p4
        c21 += d12

        # Racunamo c22 = c22 + p5
        c22 += d21

        # SSS
        if leva % 2 == 0 and skupna % 2 == 0 and desna % 2 == 0:
            return self
        # SSL
        elif leva % 2 == 0 and skupna % 2 == 0 and desna % 2 != 0:
            self[0:leva2, desnasoda:desna].multiply(left[0:leva2, 0:skupna], right[0:skupna, desnasoda:desna])
            self[leva2:leva, desnasoda:desna].multiply(left[leva2:leva, 0:skupna], right[0:skupna, desnasoda:desna])
            return self
        # LSL
        elif leva % 2 != 0 and skupna % 2 == 0 and desna % 2 != 0:
            self[0:leva2, desnasoda:desna].multiply(left[0:leva2, 0:skupna], right[0:skupna, desnasoda:desna])
            self[leva2:levasoda, desnasoda:desna].multiply(left[leva2:levasoda, 0:skupna], right[0:skupna, desnasoda:desna])
            self[levasoda:leva, 0:desna2].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, 0:desna2])
            self[levasoda:leva, desna2:desnasoda].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, desna2:desnasoda])
            self[levasoda:leva, desnasoda:desna].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, desnasoda:desna])
            return self
        # LSS
        elif leva % 2 != 0 and skupna % 2 == 0 and desna % 2 == 0:
            self[levasoda:leva, 0:desna2].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, 0:desna2])
            self[levasoda:leva, desna2:desna].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, desna2:desna])
            return self
        # LLS
        elif leva % 2 != 0 and skupna % 2 != 0 and desna % 2 == 0:
            self[levasoda:leva, 0:desna2].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, 0:desna2])
            self[levasoda:leva, desna2:desna].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, desna2:desna])
            work[0:leva2, 0:desna2].multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[0:leva2, 0:desna2] += work[0:leva2, 0:desna2]
            work[0:leva2, 0:desna2].multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desna])
            self[0:leva2, desna2:desna] += work[0:leva2, 0:desna2]
            work[0:leva2, 0:desna2].multiply(left[leva2:levasoda, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[leva2:levasoda, 0:desna2] += work[0:leva2, 0:desna2]
            work[0:leva2, 0:desna2].multiply(left[leva2:levasoda, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desnasoda])
            self[leva2:levasoda, desna2:desnasoda] += work[0:leva2, 0:desna2]
            return self
        # SLS
        elif leva % 2 == 0 and skupna % 2 != 0 and desna % 2 == 0:
            work[0:leva2, 0:desna2].multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[0:leva2, 0:desna2] += work[0:leva2, 0:desna2]
            work[0:leva2, 0:desna2].multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desna])
            self[0:leva2, desna2:desna] += work[0:leva2, 0:desna2]
            work[0:leva2, 0:desna2].multiply(left[leva2:leva, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[leva2:leva, 0:desna2] += work[0:leva2, 0:desna2]
            work[0:leva2, 0:desna2].multiply(left[leva2:leva, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desna])
            self[leva2:leva, desna2:desna] += work[0:leva2, 0:desna2]
            return self
        # SLL
        elif leva % 2 == 0 and skupna % 2 != 0 and desna % 2 != 0:
            work[0:leva2, 0:desna2].multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[0:leva2, 0:desna2] += work[0:leva2, 0:desna2]
            work[0:leva2, 0:desna2].multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desnasoda])
            self[0:leva2, desna2:desnasoda] += work[0:leva2, 0:desna2]
            work[0:leva2, 0:desna2].multiply(left[leva2:leva, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[leva2:leva, 0:desna2] += work[0:leva2, 0:desna2]
            work[0:leva2, 0:desna2].multiply(left[leva2:leva, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desnasoda])
            self[leva2:leva, desna2:desnasoda] += work[0:leva2, 0:desna2]
            self[0:leva2, desnasoda:desna].multiply(left[0:leva2, 0:skupna], right[0:skupna, desnasoda:desna])
            self[leva2:leva, desnasoda:desna].multiply(left[leva2:leva, 0:skupna], right[0:skupna, desnasoda:desna])
            return self
        # LLL
        else:
            work[0:leva2, 0:desna2].multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[0:leva2, 0:desna2] += work[0:leva2, 0:desna2]
            work[0:leva2, 0:desna2].multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desnasoda])
            self[0:leva2, desna2:desnasoda] += work[0:leva2, 0:desna2]
            work[0:leva2, 0:desna2].multiply(left[leva2:levasoda, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[leva2:levasoda, 0:desna2] += work[0:leva2, 0:desna2]
            work[0:leva2, 0:desna2].multiply(left[leva2:levasoda, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desnasoda])
            self[leva2:levasoda, desna2:desnasoda] += work[0:leva2, 0:desna2]
            self[levasoda:leva, 0:desna2].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, 0:desna2])
            self[levasoda:leva, desna2:desnasoda].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, desna2:desnasoda])
            self[0:leva2, desnasoda:desna].multiply(left[0:leva2, 0:skupna], right[0:skupna, desnasoda:desna])
            self[leva2:levasoda, desnasoda:desna].multiply(left[leva2:levasoda, 0:skupna], right[0:skupna, desnasoda:desna])
            self[levasoda:leva, desnasoda:desna].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, desnasoda:desna])
            return self