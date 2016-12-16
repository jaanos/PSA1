# -*- coding: utf-8 -*-
from slowmatrix import SlowMatrix

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
##        raise NotImplementedError("Naredi sam!")

        m = left.nrow()
        n = right.nrow()
        o = right.ncol()

        if m * n * o == 0:
            for i in range(m):
                for j in range(o):
                    self[i, j] = sum(left[i, k]*right[k, j] for k in range(n))
        
        elif m * n * o == 1:
            self[0, 0] = left[0, 0] * right[0, 0]
        
        elif m % 2 == 1 and o % 2 == 1 and n % 2 == 0:
            A = left[0:m//2, 0:n//2]
            B = left[0:m//2, n//2:]
            C = left[m//2:m-1, 0:n//2]
            D = left[m//2:m-1, n//2:]
            E = right[0:n//2, 0:o//2]
            F = right[0:n//2, o//2:o-1]
            G = right[n//2:, 0:o//2]
            H = right[n//2:, o//2:o-1]
            P1 = A * (F - H)
            P2 = (A + B) * H
            P3 = (C + D) * E
            P4 = D * (G - E)
            P5 = (A + D) * (E + H)
            P6 = (B - D) * (G + H)
            P7 = (A - C) * (E + F)
            self[0:m//2, 0:o//2] = P5 + P4 - P2 + P6
            self[0:m//2, o//2:o-1] = P1 + P2
            self[m//2:m-1, 0:o//2] = P3 + P4
            self[m//2:m-1, o//2:o-1] = P1 + P5 - P3 - P7
            for i in range(m):
                self[i, o-1] = sum(left[i, k]*right[k, o-1] for k in range(n))
            for j in range(o-1):
                self[m-1, j] = sum(left[m-1, k]*right[k, j] for k in range(n))
        elif m % 2 == 0 and o % 2 == 1 and n % 2 == 0:
            A = left[0:m//2, 0:n//2]
            B = left[0:m//2, n//2:]
            C = left[m//2:, 0:n//2]
            D = left[m//2:, n//2:]
            E = right[0:n//2, 0:o//2]
            F = right[0:n//2, o//2:o-1]
            G = right[n//2:, 0:o//2]
            H = right[n//2:, o//2:o-1]
            P1 = A * (F - H)
            P2 = (A + B) * H
            P3 = (C + D) * E
            P4 = D * (G - E)
            P5 = (A + D) * (E + H)
            P6 = (B - D) * (G + H)
            P7 = (A - C) * (E + F)
            self[0:m//2, 0:o//2] = P5 + P4 - P2 + P6
            self[0:m//2, o//2:o-1] = P1 + P2
            self[m//2:, 0:o//2] = P3 + P4
            self[m//2:, o//2:o-1] = P1 + P5 - P3 - P7
            for i in range(m):
                self[i, o-1] = sum(left[i, k]*right[k, o-1] for k in range(n))
        elif m % 2 == 1 and o % 2 == 0 and n % 2 == 0:
            A = left[0:m//2, 0:n//2]
            B = left[0:m//2, n//2:]
            C = left[m//2:m-1, 0:n//2]
            D = left[m//2:m-1, n//2:]
            E = right[0:n//2, 0:o//2]
            F = right[0:n//2, o//2:]
            G = right[n//2:, 0:o//2]
            H = right[n//2:, o//2:]
            P1 = A * (F - H)
            P2 = (A + B) * H
            P3 = (C + D) * E
            P4 = D * (G - E)
            P5 = (A + D) * (E + H)
            P6 = (B - D) * (G + H)
            P7 = (A - C) * (E + F)
            self[0:m//2, 0:o//2] = P5 + P4 - P2 + P6
            self[0:m//2, o//2:] = P1 + P2
            self[m//2:m-1, 0:o//2] = P3 + P4
            self[m//2:m-1, o//2:] = P1 + P5 - P3 - P7
            for j in range(o):
                self[m-1, j] = sum(left[m-1, k]*right[k, j] for k in range(n))
        elif m % 2 == 0 and o % 2 == 0 and n % 2 == 0:
            A = left[0:m//2, 0:n//2]
            B = left[0:m//2, n//2:]
            C = left[m//2:, 0:n//2]
            D = left[m//2:, n//2:]
            E = right[0:n//2, 0:o//2]
            F = right[0:n//2, o//2:]
            G = right[n//2:, 0:o//2]
            H = right[n//2:, o//2:]
            P1 = A * (F - H)
            P2 = (A + B) * H
            P3 = (C + D) * E
            P4 = D * (G - E)
            P5 = (A + D) * (E + H)
            P6 = (B - D) * (G + H)
            P7 = (A - C) * (E + F)
            self[0:m//2, 0:o//2] = P5 + P4 - P2 + P6
            self[0:m//2, o//2:] = P1 + P2
            self[m//2:, 0:o//2] = P3 + P4
            self[m//2:, o//2:] = P1 + P5 - P3 - P7
        elif m % 2 == 0 and o % 2 == 0 and n % 2 == 1:
            A = left[0:m//2, 0:n//2]
            B = left[0:m//2, n//2:n-1]
            C = left[m//2:, 0:n//2]
            D = left[m//2:, n//2:n-1]
            E = right[0:n//2, 0:o//2]
            F = right[0:n//2, o//2:]
            G = right[n//2:n-1, 0:o//2]
            H = right[n//2:n-1, o//2:]
            P1 = A * (F - H)
            P2 = (A + B) * H
            P3 = (C + D) * E
            P4 = D * (G - E)
            P5 = (A + D) * (E + H)
            P6 = (B - D) * (G + H)
            P7 = (A - C) * (E + F)
            self[0:m//2, 0:o//2] = P5 + P4 - P2 + P6
            self[0:m//2, o//2:] = P1 + P2
            self[m//2:, 0:o//2] = P3 + P4
            self[m//2:, o//2:] = P1 + P5 - P3 - P7
            for i in range(m):
                for j in range(o):
                    self[i, j] += left[i, n-1]*right[n-1, j]
        elif m % 2 == 1 and o % 2 == 0 and n % 2 == 1:
            A = left[0:m//2, 0:n//2]
            B = left[0:m//2, n//2:n-1]
            C = left[m//2:m-1, 0:n//2]
            D = left[m//2:m-1, n//2:n-1]
            E = right[0:n//2, 0:o//2]
            F = right[0:n//2, o//2:]
            G = right[n//2:n-1, 0:o//2]
            H = right[n//2:n-1, o//2:]
            P1 = A * (F - H)
            P2 = (A + B) * H
            P3 = (C + D) * E
            P4 = D * (G - E)
            P5 = (A + D) * (E + H)
            P6 = (B - D) * (G + H)
            P7 = (A - C) * (E + F)
            self[0:m//2, 0:o//2] = P5 + P4 - P2 + P6
            self[0:m//2, o//2:] = P1 + P2
            self[m//2:m-1, 0:o//2] = P3 + P4
            self[m//2:m-1, o//2:] = P1 + P5 - P3 - P7
            for i in range(m):
                for j in range(o):
                    self[i, j] += left[i, n-1]*right[n-1, j] 
            for j in range(o):
                self[m-1, j] = sum(left[m-1, k]*right[k, j] for k in range(n))
        elif m % 2 == 0 and o % 2 == 1 and n % 2 == 1:
            A = left[0:m//2, 0:n//2]
            B = left[0:m//2, n//2:n-1]
            C = left[m//2:, 0:n//2]
            D = left[m//2:, n//2:n-1]
            E = right[0:n//2, 0:o//2]
            F = right[0:n//2, o//2:o-1]
            G = right[n//2:n-1, 0:o//2]
            H = right[n//2:n-1, o//2:o-1]
            P1 = A * (F - H)
            P2 = (A + B) * H
            P3 = (C + D) * E
            P4 = D * (G - E)
            P5 = (A + D) * (E + H)
            P6 = (B - D) * (G + H)
            P7 = (A - C) * (E + F)
            self[0:m//2, 0:o//2] = P5 + P4 - P2 + P6
            self[0:m//2, o//2:o-1] = P1 + P2
            self[m//2:, 0:o//2] = P3 + P4
            self[m//2:, o//2:o-1] = P1 + P5 - P3 - P7
            for i in range(m):
                for j in range(o):
                    self[i, j] += left[i, n-1]*right[n-1, j]
            for i in range(m):
                self[i, o-1] = sum(left[i, k]*right[k, o-1] for k in range(n))
        elif m % 2 == 1 and o % 2 == 1 and n % 2 == 1:
            A = left[0:m//2, 0:n//2]
            B = left[0:m//2, n//2:n-1]
            C = left[m//2:m-1, 0:n//2]
            D = left[m//2:m-1, n//2:n-1]
            E = right[0:n//2, 0:o//2]
            F = right[0:n//2, o//2:o-1]
            G = right[n//2:n-1, 0:o//2]
            H = right[n//2:n-1, o//2:o-1]
            P1 = A * (F - H)
            P2 = (A + B) * H
            P3 = (C + D) * E
            P4 = D * (G - E)
            P5 = (A + D) * (E + H)
            P6 = (B - D) * (G + H)
            P7 = (A - C) * (E + F)
            self[0:m//2, 0:o//2] = P5 + P4 - P2 + P6
            self[0:m//2, o//2:o-1] = P1 + P2
            self[m//2:m-1, 0:o//2] = P3 + P4
            self[m//2:m-1, o//2:o-1] = P1 + P5 - P3 - P7
            for i in range(m):
                for j in range(o):
                    self[i, j] += left[i, n-1]*right[n-1, j]
            for i in range(m):
                self[i, o-1] = sum(left[i, k]*right[k, o-1] for k in range(n))
            for j in range(o-1):
                self[m-1, j] = sum(left[m-1, k]*right[k, j] for k in range(n))
