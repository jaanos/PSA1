# -*- coding: utf-8 -*-
#try:
#    from .slowmatrix import SlowMatrix
#except(SystemError):
#    from slowmatrix import SlowMatrix

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


        # left je dimenzije m*n, right je dimenzij n*k
        # Časovna zahtevnost: T(m, n, k)
        # Prostorska zahtevnost: S(m, n, k)

        # Dimenzije matrik
        m, n, k  = left.nrow(), left.ncol(), right.ncol()           # O(1)
        # Dimenzije novih bločnih matrik
        m1, n1, k1 = m//2, n//2, k//2                               # O(1)
        m2, n2, k2 = m1*2, n1*2, k1*2                               # O(1)

        """Navadno množenje z vektorjem"""
        # Če je ena izmed dimenzij = 1 => vsaj ena je vektor
        # To porabi O(n*k) ali O(m*k) ali O(n*k) operacij
        if m == 1 or n == 1 or k == 1:
            # Iz SlowMatrix podedujemo multiply oz. naivno množenje
            super().multiply(left,right)

        else:
            """Strassenov algoritem"""
            # Potrebne bločne matrike, istih dimenzij (če so bile prej lihe, jih obravnavamo kot sode, s preostanki se bomo ubadali kasneje)
            A = left[0:m1, 0:n1]
            B = left[0:m1, n1:n2]
            C = left[m1:m2, 0:n1]
            D = left[m1:m2, n1:n2]
            E = right[0:n1, 0:k1]
            F = right[0:n1, k1:k2]
            G = right[n1:n2, 0:k1]
            H = right[n1:n2, k1:k2]

            # Časovna zahtevnost: O(1)
            # Ta del skupaj porabi O(1) prostora, ker ne naredimo novih matrik, le sklice na dele originalnih matrik

            # Produkti za Strassenov algoritem

            # Izvedemo 7 produktov in za vsakega eno ali dve sestevanji/odstevanji. Produkti so rekurzivni
            # Skupaj imajo časovno zahtevnost T(m,n,k) = 7 * T(m/2,n/2,k/2) + 5 * O((m/2)*(n/2)) + 5 * O((n/2)*(k/2))

            P1 = A*(F-H)
            P2 = (A + B)*H
            P3 = (C + D)*E
            P4 = D*(G-E)
            P5 = (A + D)*(E + H)
            P6 = (B - D)*(G + H)
            P7 = (A - C)*(E + F)

            # Te matrike porabijo skupaj 7 * O((m/2)*(k/2)) prostora v tej iteraciji
            # Dodatni prostor pa porabijo začasne matrike pri seštevanju
            # Prostorska zahtevnost: S(m,n,k) = 7 * S(m/2,n/2,k/2) + 5 * O((m/2)*(n/2)) + 5 * O((n/2)*(k/2))

            """Postopek se loči, če je n lih ali sod"""

            # Ne glede na sodost/lihost dimenzij, je del matrike isti
            self[0:m1, 0:k1] = P4 + P5 + P6 -P2
            self[0:m1, k1:k2] = P1 + P2
            self[m1:m2, 0:k1] = P3 + P4
            self[m1:m2, k1:k2] = P1 + P5 - P3 - P7
            # Če so vse dimenzije sode, je to to
            # Časovna zahtevnost: 8 * O((n/2) * (k/2))
            # Prostorska zahtevnost: 8 * O((n/2) * (k/2))

            # Če je n sod
            if n % 2 == 0:
                # Če m lih
                # Vzamemo m-to vrstico matrike left in jo zmnožimo z matriko right, jo damo na mesto m-te vrstice
                if m % 2 != 0:
                    v = left[m-1,:]                 # O(1)
                    self[m-1,:] = v * right
                    # Časovna zahtevnost: O(n*k)
                    # Prostorska zahtevnost: O(k)

                # Če k lih
                # Vzamemo k-ti stolpec matrike right, pomnožimo matriko left s tem stolpcem, damo na mesto k-tega stolpca
                if k % 2 != 0:
                    u = right[:,k-1]                        # O(1)
                    self[:,k-1] = left * u
                    # Časovna zahtevnost: O(m*n)
                    # Prostorska zahtevnost: O(m)

                #Nepotrebno
                # Če k in m liha
                #if k % 2 != 0 and m % 2 != 0:     # k in m liha
                #    self[m-1,k-1] = v * u

            # Če je n lih
            else:
                # v = zadnji stolpec left brez zadnjega elementa, u = zadnja vrstica right brez zadnjega elementa
                v = left[0:m2,n-1]          # O(1)
                u = right[n-1,0:k2]         # O(1)

                # Zmnožimo v in u, nastane matrika, ki jo prištejemo obstoječi
                self[0:m2,0:k2] += v * u
                # Časovna zahtevnost: O((m-1) * (k-1))
                # Prostorska zahtevnost: O((m-1) * (k-1)) začasna matrika zaradi množenja

                # Če m lih
                # Vzamemo m-to vrstico iz left in jo pomnožimo matriko right, dodamo v m-to vrstico
                if m % 2 != 0:
                    g = left[m-1,:]             # O(1)
                    self[m-1,:] = g * right
                    # Časovna zahtevnost: O(k)
                    # Prostorska zahtevnost: O(k)

                # Če k lih
                # Vzamemo k-ti stolpec matrike right, z leve ga pomnožimo z left, dodamo v k-ti stolpec
                if k % 2 != 0:
                    h = right[:,k-1]            # O(1)
                    self[:,k-1] = left * h
                    # Časovna zahtevnost: O(n)
                    # Prostorska zahtevnost: (m)

                # Nepotrebno
                # Če m lih
                #if m % 2 != 0 and k % 2 != 0:     # m, n in k lihi
                 #   self[m-1,k-1] = g * h
