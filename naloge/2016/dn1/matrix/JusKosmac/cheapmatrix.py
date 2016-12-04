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
        #raise NotImplementedError("Naredi sam!")
        #velikosti matrik sta m x k in k x n
        m = left.nrow()
        k = left.ncol()
        n = right.ncol()
        if m == 1 or n == 1 or k == 1: #navadno množenje O(n^2)
            super().multiply(left, right)
        else:
            m1 = m // 2
            m2 = 2 * m1
            n1 = n // 2
            n2 = 2 * n1
            k1 = k // 2
            k2 = 2 * k1
            A = left[0:m1, 0:k1]
            B = left[0:m1, k1:k2]
            C = left[m1:m2, 0:k1]
            D = left[m1:m2, k1:k2]
            E = right[0:k1, 0:n1]
            F = right[0:k1, n1:n2]
            G = right[k1:k2, 0:n1]
            H = right[k1:k2, n1:n2]
            X = work[0:m1, 0:n1]
            Y = work[0:m1, n1:n2]
            Z = work[m1:m2, 0:n1]
            W = work[m1:m2, n1:n2]
            S1 = self[0:m1, 0:n1]
            S2 = self[0:m1, n1:n2]
            S3 = self[m1:m2, 0:n1]
            S4 = self[m1:m2, n1:n2]
            #P6
            B -= D
            G += H
            S1.multiply(B, G, X)
            B += D
            G -= H
            #P2
            A += B
            S2.multiply(A, H, Y)
            A -= B
            #P4
            G -= E
            S3.multiply(D, G, Z)
            G += E
            #P5
            A += D
            E += H
            S4.multiply(A, E, W)
            A -= D
            E -= H
            #prištejemo še P5 in P6 ter odštejemo P2
            S1 -= S2
            S1 += S3
            S1 += S4
            #P1
            F -= H
            X.multiply(A, F, Y)
            F += H
            S2 += X
            S4 += X
            #P3
            C += D
            X.multiply(C, E, Y)
            C -= D
            S3 += X
            S4 -= X
            #P7
            A -= C
            E += F
            X.multiply(A, E, Y)
            A += C
            E -= F
            S4 -= X
            if k2 == k: #sod
                if m2 != m: #lih
                    a = left[m-1, 0:k1]
                    b = left[m-1, k1:k2]
                    a1 = work[m-1, 0:n1]
                    b1 = work[m-1, n1:n2]
                    self[m-1, 0:n1].multiply(a, E, a1)
                    a1.multiply(b, G, b1)
                    self[m-1, 0:n1] += a1
                    self[m-1, n1:n2].multiply(a, F, a1)
                    a1.multiply(b, H, b1)
                    self[m-1, n1:n2] += a1
                if n2 != n: #lih
                    c = right[0:k1, n-1]
                    d = right[k1:k2, n-1]
                    c1 = work[0:m1, n-1]
                    d1 = work[m1:m2, n-1]
                    self[0:m1, n-1].multiply(A, c, c1)
                    c1.multiply(B, d, d1)
                    self[0:m1, n-1] += c1
                    self[m1:m2, n-1].multiply(C, c, c1)
                    c1.multiply(D, d, d1)
                    self[m1:m2, n-1] += c1
                if n2 != n and m2 != m: #oba liha
                    self[m-1, n-1] += a * c #ustvari se nova matrika velikosti 1x1
                    self[m-1, n-1] += b * d
            else: #k je lih
                x = left[0:m1, k-1]
                y = left[m1:m2, k-1]
                u = right[k-1, 0:n1]
                w = right[k-1, n1:n2]
                X.multiply(x, u, Y)
                S1 += X
                X.multiply(x, w, Y)
                S2 += X
                X.multiply(y, u, Y)
                S3 += X
                X.multiply(y, w, Y)
                S4 += X
                if m2 != m: #lih
                    a = left[m-1, 0:k1]
                    b = left[m-1, k1:k2]
                    alfa = left[m-1, k-1]
                    a1 = work[m-1, 0:n1]
                    b1 = work[m-1, n1:n2]
                    self[m-1, 0:n1].multiply(a, E, a1)
                    a1.multiply(b, G, b1)
                    self[m-1, 0:n1] += a1
                    for i in range(n1):
                        self[m-1, i] += alfa * u[0, i]
##                    a1.multiply(alfa, u, b1)
##                    self[m-1, 0:n1] += a1
                    self[m-1, n1:n2].multiply(a, F, a1)
                    a1.multiply(b, H, b1)
                    self[m-1, n1:n2] += a1
                    for i in range(n1):
                        self[m-1, i + n1] += alfa * w[0, i]
##                    a1.multiply(alfa, w, b1)
##                    self[m-1, n1:n2] += a1
                if n2 != n: #lih
                    c = right[0:k1, n-1]
                    d = right[k1:k2, n-1]
                    beta = right[k-1, n-1]
                    c1 = work[0:m1, n-1]
                    d1 = work[m1:m2, n-1]
                    self[0:m1, n-1].multiply(A, c, c1)
                    c1.multiply(B, d, d1)
                    self[0:m1, n-1] += c1
                    for i in range(m1):
                        self[i, n-1] += beta * x[i, 0]
##                    c1.multiply(x, beta, d1)
##                    self[0:m1, n-1] += c1
                    self[m1:m2, n-1].multiply(C, c, c1)
                    c1.multiply(D, d, d1)
                    self[m1:m2, n-1] += c1
                    for i in range(m1):
                        self[i + m1, n-1] += beta * y[i, 0]
##                    c1.multiply(y, beta, d1)
##                    self[m1:m2, n-1] += c1
                if n2 != n and m2 != m: #oba liha
                    self[m-1, n-1] += a * c #ustvari se nova matrika velikosti 1x1
                    self[m-1, n-1] += b * d
                    self[m-1, n-1] += alfa * beta       
