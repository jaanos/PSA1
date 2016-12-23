# -*- coding: utf-8 -*-
from slowmatrix import SlowMatrix
from matrix import AbstractMatrix

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

        # Matrike so velikosti:
        # left: leva x skupna
        # right: skupna x desna

        leva = left.nrow()
        leva2 = leva//2
        levasoda = 2*leva2
        skupna = left.ncol()
        skupna2 = skupna//2
        skupnasoda = 2*skupna2
        desna = right.ncol()
        desna2 = desna//2
        desnasoda = 2*desna2

        if leva == 1 or desna == 1 or skupna == 1:
            return SlowMatrix.multiply(self, left, right)
        a = left[0:leva2, 0:skupna2]
        b = left[0:leva2, skupna2:skupnasoda]
        c = left[leva2:levasoda, 0:skupna2]
        d = left[leva2:levasoda, skupna2:skupnasoda]
        e = right[0:skupna2, 0:desna2]
        f = right[0:skupna2, desna2:desnasoda]
        g = right[skupna2:skupnasoda, 0:desna2]
        h = right[skupna2:skupnasoda, desna2:desnasoda]

        p1 = FastMatrix(nrow=a.nrow(), ncol=f.ncol())
        p1.multiply(a, f-h)
        p2 = FastMatrix(nrow=a.nrow(), ncol=h.ncol())
        p2.multiply(a+b, h)
        p3 = FastMatrix(nrow=c.nrow(), ncol=e.ncol())
        p3.multiply(c+d, e)
        p4 = FastMatrix(nrow=d.nrow(), ncol=g.ncol())
        p4.multiply(d, g-e)
        p5 = FastMatrix(nrow=a.nrow(), ncol=e.ncol())
        p5.multiply(a+d, e+h)
        p6 = FastMatrix(nrow=b.nrow(), ncol=g.ncol())
        p6.multiply(b-d, g+h)
        p7 = FastMatrix(nrow=a.nrow(), ncol=f.ncol())
        p7.multiply(a-c, e+f)

        self[0:leva2, 0:desna2] = p4 + p5 + p6 - p2
        self[0:leva2, desna2:desnasoda] = p1 + p2
        self[leva2:levasoda, 0:desna2] = p3 + p4
        self[leva2:levasoda, desna2:desnasoda] = p1 + p5 - p3 - p7

        # SSS
        if leva%2 == 0 and skupna%2 == 0 and desna%2 == 0:
            return self
        # SSL
        elif leva%2 == 0 and skupna%2 == 0 and desna%2 != 0:
            self[0:leva2, desnasoda:desna].multiply(left[0:leva2, 0:skupna], right[0:skupna, desnasoda:desna])
            self[leva2:leva, desnasoda:desna].multiply(left[leva2:leva, 0:skupna], right[0:skupna, desnasoda:desna])
            return self
        # LSL
        elif leva%2 != 0 and skupna%2 == 0 and desna%2 != 0:
            self[0:leva2, desnasoda:desna].multiply(left[0:leva2, 0:skupna], right[0:skupna, desnasoda:desna])
            self[leva2:levasoda, desnasoda:desna].multiply(left[leva2:levasoda, 0:skupna], right[0:skupna, desnasoda:desna])
            self[levasoda:leva, 0:desna2].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, 0:desna2])
            self[levasoda:leva, desna2:desnasoda].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, desna2:desnasoda])
            self[levasoda:leva, desnasoda:desna].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, desnasoda:desna])
            return self
        # LSS
        elif leva%2 != 0 and skupna%2 == 0 and desna%2 == 0:
            self[levasoda:leva, 0:desna2].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, 0:desna2])
            self[levasoda:leva, desna2:desna].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, desna2:desna])
            return self
        # LLS
        elif leva%2 != 0 and skupna%2 != 0 and desna%2 == 0:
            self[levasoda:leva, 0:desna2].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, 0:desna2])
            self[levasoda:leva, desna2:desna].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, desna2:desna])
            r1 = FastMatrix(nrow = leva2, ncol = desna2)
            r2 = FastMatrix(nrow = leva2, ncol = desna2)
            r3 = FastMatrix(nrow = leva2, ncol = desna2)
            r4 = FastMatrix(nrow = leva2, ncol = desna2)
            self[0:leva2, 0:desna2] += r1.multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[0:leva2, desna2:desna] += r2.multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desna])
            self[leva2:levasoda, 0:desna2] += r3.multiply(left[leva2:levasoda, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[leva2:levasoda, desna2:desnasoda] += r4.multiply(left[leva2:levasoda, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desnasoda])
            return self
        # SLS
        elif leva%2 == 0 and skupna%2 != 0 and desna%2 == 0:
            r1 = FastMatrix(nrow = leva2, ncol = desna2)
            r2 = FastMatrix(nrow = leva2, ncol = desna2)
            r3 = FastMatrix(nrow = leva2, ncol = desna2)
            r4 = FastMatrix(nrow = leva2, ncol = desna2)
            self[0:leva2, 0:desna2] += r1.multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[0:leva2, desna2:desna] += r2.multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desna])
            self[leva2:leva, 0:desna2] += r3.multiply(left[leva2:leva, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[leva2:leva, desna2:desna] += r4.multiply(left[leva2:leva, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desna])
            return self
        # SLL
        elif leva%2 == 0 and skupna%2 != 0 and desna%2 != 0:
            r1 = FastMatrix(nrow=leva2, ncol=desna2)
            r2 = FastMatrix(nrow=leva2, ncol=desna2)
            r3 = FastMatrix(nrow=leva2, ncol=desna2)
            r4 = FastMatrix(nrow=leva2, ncol=desna2)
            self[0:leva2, 0:desna2] += r1.multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[0:leva2, desna2:desnasoda] += r2.multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desnasoda])
            self[leva2:leva, 0:desna2] += r3.multiply(left[leva2:leva, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[leva2:leva, desna2:desnasoda] += r4.multiply(left[leva2:leva, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desnasoda])
            self[0:leva2, desnasoda:desna].multiply(left[0:leva2, 0:skupna], right[0:skupna, desnasoda:desna])
            self[leva2:leva, desnasoda:desna].multiply(left[leva2:leva, 0:skupna], right[0:skupna, desnasoda:desna])
            return self
        # LLL
        else:
            r1 = FastMatrix(nrow=leva2, ncol=desna2)
            r2 = FastMatrix(nrow=leva2, ncol=desna2)
            r3 = FastMatrix(nrow=leva2, ncol=desna2)
            r4 = FastMatrix(nrow=leva2, ncol=desna2)
            self[0:leva2, 0:desna2] += r1.multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[0:leva2, desna2:desnasoda] += r2.multiply(left[0:leva2, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desnasoda])
            self[leva2:levasoda, 0:desna2] += r3.multiply(left[leva2:levasoda, skupnasoda:skupna], right[skupnasoda:skupna, 0:desna2])
            self[leva2:levasoda, desna2:desnasoda] += r4.multiply(left[leva2:levasoda, skupnasoda:skupna], right[skupnasoda:skupna, desna2:desnasoda])
            self[0:leva2, desnasoda:desna].multiply(left[0:leva2, 0:skupna], right[0:skupna, desnasoda:desna])
            self[leva2:levasoda, desnasoda:desna].multiply(left[leva2:levasoda, 0:skupna], right[0:skupna, desnasoda:desna])
            self[levasoda:leva, 0:desna2].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, 0:desna2])
            self[levasoda:leva, desna2:desnasoda].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, desna2:desnasoda])
            self[levasoda:leva, desnasoda:desna].multiply(left[levasoda:leva, 0:skupna], right[0:skupna, desnasoda:desna])
            return self