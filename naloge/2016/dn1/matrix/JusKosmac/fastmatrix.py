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
            P1 = A * (F - H)
            P2 = (A + B) * H
            P3 = (C + D) * E
            P4 = D * (G - E)
            P5 = (A + D) * (E + H)
            P6 = (B - D) * (G + H)
            P7 = (A - C) * (E + F)
            if k2 == k: #sod
                self[0:m1, 0:n1] = P4 + P5 + P6 - P2
                self[0:m1, n1:n2] = P1 + P2
                self[m1:m2, 0:n1] = P3 + P4
                self[m1:m2, n1:n2] = P1 + P5 - P3 - P7
                if m2 != m: #lih
                    a = left[m-1, 0:k1]
                    b = left[m-1, k1:k2]
                    self[m-1, 0:n1] = a * E + b * G
                    self[m-1, n1:n2] = a * F + b * H
                if n2 != n: #lih
                    c = right[0:k1, n-1]
                    d = right[k1:k2, n-1]
                    self[0:m1, n-1] = A * c + B * d
                    self[m1:m2, n-1] = C * c + D * d
                if n2 != n and m2 != m: #oba liha
                    self[m-1, n-1] = a * c + b * d
            else: #k je lih
                x = left[0:m1, k-1]
                y = left[m1:m2, k-1]
                u = right[k-1, 0:n1]
                w = right[k-1, n1:n2]
                self[0:m1, 0:n1] = P4 + P5 + P6 - P2 + x * u
                self[0:m1, n1:n2] = P1 + P2 + x * w
                self[m1:m2, 0:n1] = P3 + P4 + y * u
                self[m1:m2, n1:n2] = P1 + P5 - P3 - P7 + y * w
                if m2 != m: #lih
                    a = left[m-1, 0:k1]
                    b = left[m-1, k1:k2]
                    alfa = left[m-1, k-1]
                    self[m-1, 0:n1] = a * E + b * G + alfa * u
                    self[m-1, n1:n2] = a * F + b * H + alfa * w
                if n2 != n: #lih
                    c = right[0:k1, n-1]
                    d = right[k1:k2, n-1]
                    beta = right[k-1, n-1]
                    self[0:m1, n-1] = A * c + B * d + x * beta
                    self[m1:m2, n-1] = C * c + D * d + y * beta
                if n2 != n and m2 != m: #oba liha
                    self[m-1, n-1] = a * c + b * d + alfa * beta
                
                
            
