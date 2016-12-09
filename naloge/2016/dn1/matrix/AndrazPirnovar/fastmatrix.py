# -*- coding: utf-8 -*-
try:
    from .slowmatrix import SlowMatrix
except(SystemError):
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
        #raise NotImplementedError("Naredi sam!")

        #left je dimenzije m*n, right je dimenzij n*k


        m, n, k  = left.nrow(), left.ncol(), right.ncol()       #Dimenzije matrik
        m1, n1, k1 = m//2, n//2, k//2                           #Dimenzije novih blocnih matrik
        m2, n2, k2 = m1*2, n1*2, k1*2

        """Navadno množenje z vektorjem"""
        if m == 1 or n == 1 or k == 1:          # Če je ena izmed dimenzij = 1 => vsaj ena je vektor
            super().multiply(left,right)       #Iz SlowMatrix podedujemo multiply

        else:

            #Potrebne blocne matrike, istih dimenzij (ce so bile prej lihe, jih obravnavamo kot sode)

            A = left[0:m1, 0:n1]
            B = left[0:m1, n1:n2]
            C = left[m1:m2, 0:n1]
            D = left[m1:m2, n1:n2]
            E = right[0:n1, 0:k1]
            F = right[0:n1, k1:k2]
            G = right[n1:n2, 0:k1]
            H = right[n1:n2, k1:k2]

            #Produkti

            P1 = A*(F-H)
            P2 = (A + B)*H
            P3 = (C + D)*E
            P4 = D*(G-E)
            P5 = (A + D)*(E + H)
            P6 = (B - D)*(G + H)
            P7 = (A - C)*(E + F)

            """Postopek se loči, če je n lih ali sod"""
            self[0:m1, 0:k1] = P4 + P5 + P6 -P2
            self[0:m1, k1:k2] = P1 + P2
            self[m1:m2, 0:k1] = P3 + P4
            self[m1:m2, k1:k2] = P1 + P5 - P3 - P7

            if n % 2 == 0:          #n sod
                if m % 2 != 0:       #m lih
                    v = left[m-1,:]
                    self[m-1,:] = v * right
                if k % 2 != 0:       #k lih
                    u = right[:,k-1]
                    self[:,k-1] = left * u
                if k % 2 != 0 and m % 2 != 0:     #k in m liha
                    self[m-1,k-1] = v * u
            else:                   #n lih
                v = left[0:m2,n-1]
                u = right[n-1,0:k2]
                self[0:m2,0:k2] += v * u
                if m % 2 != 0:      #m lih
                    g = left[m-1,:]
                    self[m-1,:] = g * right
                if k % 2 != 0:      #k lih
                    h = right[:,k-1]
                    self[:,k-1] = left * h
                if m % 2 != 0 and k % 2 != 0:     #m, n in k lihi
                    self[m-1,k-1] = g * h


















