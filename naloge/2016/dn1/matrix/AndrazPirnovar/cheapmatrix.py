# -*- coding: utf-8 -*-

from .slowmatrix import SlowMatrix


class CheapMatrix(SlowMatrix):
    """
    Matrika s prostorsko nepotratnim množenjem.
    """

    def multiply(self, left, right, work=None):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Kot neobvezen argument lahko podamo še delovno matriko.
        """
        assert left.ncol() == right.nrow(), \
            "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
            "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        if work is None:
            work = self.__class__(nrow=self.nrow(), ncol=self.ncol())
        else:
            assert self.nrow() == work.nrow() and self.ncol() == work.ncol(), \
                "Dimenzije delovne matrike ne ustrezajo dimenzijam produkta!"

        # left je dimenzije m*n, right je dimenzij n*k
        # Časovna zahtevnost: T(m, n, k)
        # Prostorska zahtevnost: S(m, n, k)

        # Dimenzije matrik
        m, n, k = left.nrow(), left.ncol(), right.ncol()  # O(1)
        # Dimenzije novih blocnih matrik
        m1, n1, k1 = m // 2, n // 2, k // 2  # O(1)
        m2, n2, k2 = m1 * 2, n1 * 2, k1 * 2  # O(1)

        """Navadno množenje z vektorjem"""
        # Če je ena izmed dimenzij = 1 => vsaj ena je vektor
        # To porabi O(n*k) ali O(m*k) ali O(n*k) operacij
        # Porabi O(1) prostora
        if m == 1 or n == 1 or k == 1:
            # Iz SlowMatrix podedujemo multiply oz. naivno množenje
            super().multiply(left, right)  # Iz SlowMatrix podedujemo multiply


        else:
            """Strassenov algoritem"""

            """Naredimo si blocne matrike"""
            A = left[0:m1, 0:n1]
            B = left[0:m1, n1:n2]
            C = left[m1:m2, 0:n1]
            D = left[m1:m2, n1:n2]
            E = right[0:n1, 0:k1]
            F = right[0:n1, k1:k2]
            G = right[n1:n2, 0:k1]
            H = right[n1:n2, k1:k2]
            # Časovna zahtevnost: O(1)
            # Prostorska zahtevnost: O(1)

            """Pripravimo si delovne matrike"""
            W1 = work[0:m1, 0:k1]
            W2 = work[0:m1, k1:k2]
            # Časovna zahtevnost: O(1)
            # Prostorska zahtevnost: O(1)

            """Pripravimo si ciljno matriko"""
            S1 = self[0:m1, 0:k1]
            S2 = self[0:m1, k1:k2]
            S3 = self[m1:m2, 0:k1]
            S4 = self[m1:m2, k1:k2]
            # Časovna zahtevnost: O(1)
            # Prostorska zahtevnost: O(1)

            """Izracunamo clene za Strassnov"""
            # Prvo bomo izracunali sode dele za izhodno matriko, nato pa bomo pogledali se lihe primere
            # Vrstni red bo tak, da bomo prvo "definirali" S1,...,S4, nato pa pristevali in odstevali


            """ P1 """
            F -= H
            W1.multiply(A, F, W2)
            F += H
            # Dodamo W1 == P1 v primerne bloke
            S2[:, :] = W1
            S4[:, :] = W1
            # Časovna zahtevnost: T(m/2,n/2,k/2) + O(n*k)
            # Prostorska zahtevnost: S(m/2,n/2,k/2)

            """ P3 """
            C += D
            W1.multiply(C, E, W2)
            C -= D
            # Dodamo W1 == P3 v primerne bloke
            S3[:, :] = W1
            S4 -= W1
            # Časovna zahtevnost: T(m/2,n/2,k/2) + O(m*n) + O(m*k)
            # Prostorska zahtevnost: S(m/2,n/2,k/2)

            """ P4 """
            G -= E
            W1.multiply(D, G, W2)
            G += E
            # Dodamo W1 == P4 v primerne bloke
            S1[:, :] = W1
            S3 += W1
            # Časovna zahtevnost: T(m/2,n/2,k/2) + O(n*k) + O(m*k)
            # Prostorska zahtevnost: S(m/2,n/2,k/2)

            """ P2 """
            A += B
            W1.multiply(A, H, W2)
            A -= B
            # Dodamo W1 == P2 v primerne bloke
            S1 -= W1
            S2 += W1
            # Časovna zahtevnost: T(m/2,n/2,k/2) + O(m*n) + O(m*k)
            # Prostorska zahtevnost: S(m/2,n/2,k/2)

            """ P5 """
            A += D
            E += H
            W1.multiply(A, E, W2)
            A -= D
            E -= H
            # Dodamo W1 == P5 v primerne bloke
            S1 += W1
            S4 += W1
            # Časovna zahtevnost: T(m/2,n/2,k/2) + O(n*k) + O(m*n) + O(m*k)
            # Prostorska zahtevnost: S(m/2,n/2,k/2)

            """ P6 """
            B -= D
            G += H
            W1.multiply(B, G, W2)
            B += D
            G -= H
            # Dodamo W1 == P6 v primerne bloke
            S1 += W1
            # Časovna zahtevnost: T(m/2,n/2,k/2) + O(n*k) + =(m*n) + O(m*k)
            # Prostorska zahtevnost: S(m/2,n/2,k/2)

            """ P7 """
            A -= C
            E += F
            W1.multiply(A, E, W2)
            A += C
            E -= F
            # Dodamo W1 == P7 v primerne bloke
            S4 -= W1
            # Časovna zahtevnost: T(m/2,n/2,k/2) + O(n*k) + O(m*n) + O(m*k)
            # Prostorska zahtevnost: S(m/2,n/2,k/2)

            # Skupaj:
            # Časovna zahtevnost: 7*T(m/2,n/2,k/2) + O(n*k) + O(m*n) + O(m*k)
            # Prostorska zahtevnost:7*S(m/2,n/2,k/2)


            """ Računanje preostalih delov"""

            # Če je n sod
            if n % 2 == 0:
                # Če m lih
                # Vzamemo m-to vrstico matrike left in jo zmnožimo z matriko right, jo damo na mesto m-te vrstice
                if m % 2 != 0:
                    v = left[m - 1, :]  # O(1)
                    self[m - 1, :].multiply(v, right, work[m - 1, :])
                    # Časovna zahtevnost: O(n*k)
                    # Prostorska zahtevnost: O(1)       (ker algoritem uporabi naivno množenje)

                # Če k lih
                # Vzamemo k-ti stolpec matrike right, pomnožimo matriko left s tem stolpcem, damo na mesto k-tega stolpca
                if k % 2 != 0:
                    u = right[:, k - 1]  # O(1)
                    self[:, k - 1].multiply(left, u, work[:, k - 1])
                    # Časovna zahtevnost: O(m*n)
                    # Prostorska zahtevnost: O(1)

            # Če je n lih
            else:
                # v = zadnji stolpec left brez zadnjega elementa, u = zadnja vrstica right brez zadnjega elementa
                v = left[0:m2, n - 1]  # O(1)
                u = right[n - 1, 0:k2]  # O(1)

                # Zmnožimo v in u, nastane matrika, ki jo prištejemo obstoječi
                for i in range(m2):
                    for j in range(k2):
                        self[i, j] += v[i, 0] * u[0, j]

                # Časovna zahtevnost: O((m-1) * (k-1))
                # Prostorska zahtevnost: O(1)

                # Če m lih
                # Vzamemo m-to vrstico iz left in jo pomnožimo matriko right, dodamo v m-to vrstico
                if m % 2 != 0:
                    g = left[m - 1, :]  # O(1)
                    self[m - 1, :].multiply(g, right, work[m - 1, :])
                    # Časovna zahtevnost: O(k)
                    # Prostorska zahtevnost: O(1)

                # Če k lih
                # Vzamemo k-ti stolpec matrike right, z leve ga pomnožimo z left, dodamo v k-ti stolpec
                if k % 2 != 0:
                    h = right[:, k - 1]  # O(1)
                    self[:, k - 1].multiply(left, h, work[:, k - 1])
                    # Časovna zahtevnost: O(n)
                    # Prostorska zahtevnost: O(1)
