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

        # Vrednosti dimenzij shranimo v nove spremenljivke kot v FastMatrix
        ## Časovna zahtevnost: O(1)
        ## Prostorska zahtevnost: O(1)

        n = left.nrow()
        m = left.ncol()  # = right.nrow()
        k = right.ncol()

        # Definiramo nove spremenljivke
        ## Časovna zahtevnost: O(1)
        ## Prostorska zahtevnost: O(1)

        N = n // 2
        M = m // 2
        K = k // 2
        N2 = 2 * N
        M2 = 2 * M
        K2 = 2 * K

        # Če je ena od dimenzij matrik enaka 1, imamo navadno množenje - SlowMatrix; množenje podedujemo iz SlowMatrix.
        ## Časovna in prostorska zahtevnost sta enaki zahtevnosti algoritma SlowMatrix.

        if n == 1 or m == 1 or k == 1:
            super().multiply(left, right)

        else:

            # Definiramo podmatrike za Strassenov algoritem (isto kot v FastMatrix)
            ## Časovna zahtevnost: O(1)
            ## Prostorska zahtevnost: O(1)


            A = left[0:N, 0:M]
            B = left[0:N, M:M2]             # V primeru, da je left.ncol() liho število, gremo do vključno predzadnjega stolpca.
            C = left[N:N2, 0:M]             # Isto kot pri lihih stolpcih, s tem da sedaj lihe vrstice.
            D = left[N:N2, M:M2]            # Pri D pazimo na lihe vrstice in lihe stolpce.

                                            # Podobno naredimo še za desno matriko.

            E = right[0:M, 0:K]
            F = right[0:M, K:K2]
            G = right[M:M2, 0:K]
            H = right[M:M2, K:K2]

            # Končno matriko self, ki ima trenutno vrednosti 0, in jo razdelimo na 4 sode dele
            # zaenkrat ignoriramo lihe dele dimenzije, kot v FastMatrix
            ## Časovna zahtevnost: O(1)
            ## Prostorska zahtevnost: O(1)

            S1 = self[0:N, 0:K]
            S2 = self[0:N, K:K2]
            S3 = self[N:N2, 0:K]
            S4 = self[N:N2, K:K2]

            # Prav tako razdelimo delovno matriko na 4 dele (v nadaljevanju bomo sicer potrebovali le dva dela)
            ## Časovna zahtevnost: O(1)
            ## Prostorska zahtevnost: O(1)

            D1 = work[0:N, 0:K]
            D2 = work[0:N, K:K2]
            D3 = work[N:N2, 0:K]
            D4 = work[N:N2, K:K2]


            # V nadaljevanju bomo računali matriko self, vsak del posebej, pri čemer
            # S1 = P4 + P5 + P6 - P2
            # S2 = P1 + P2
            # S3 = P3 + P4
            # S4 = P1 + P5 - P3 - P7
            # Da se izognemo veliki prostorski porabi pri seštevanju matrik, uporabimo operatorja += oz. -=,
            # pri čemer se ne ustvari nova matrika in torej ne potrebujemo dodatnega prostora


            # RAČUNANJE Pi, i = 1,...,,7, pri čemer porabimo manj prostora (pazimo pri P2!)

            # P1
            ## Časovna zahtevnost: O(M*K) + T(N, M, K) + O(1) + O(M*K)
            ## Prostorska zahtevnost: P(N, M, K)

            F -= H
            S2.multiply(A, F, D1)                                       # Novo stanje S2: S2 = P1
            S4[0:N,0:K] = S2                                            # Novo stanje S4: S4 = P1
            F += H

            # P3
            ## Časovna zahtevnost: O(N*M) + T(N, M, K) + O(N*K) + O(N*M)
            ## Prostorska zahtevnost: P(N, M, K)

            C += D
            S3.multiply(C, E, D1)                                       # Novo stanje S3: S3 = P3
            S4 -= S3                                                    # Novo stanje S4: S4 = P1 - P3
            C -= D

            # P4
            ## Časovna zahtevnost: O(M*K) + T(N, M, K) + 2*O(N*K) + O(M*K)
            ## Prostorska zahtevnost: P(N, M, K)

            G -= E
            D1.multiply(D, G, D2)
            S3 += D1                                                    # Podmatrika S3 je sedaj gotova: S3 = P3 + P4
            S1 += D1                                                    # Novo stanje S1: S1 = P4
            G += E

            # P2
            ## Časovna zahtevnost: O(N*M) + T(N, M, K) + 2*O(N*K) + O(M*K)
            ## Prostorska zahtevnost: P(N, M, K)

            A += B
            D1.multiply(A, H, D2)
            S2 += D1                                                    # Podmatrika S2 je sedaj gotova: S2 = P1 + P2
            S1 -= D1                                                    # Novo stanje S1: S1 = P4 - P2
            A -= B

            # P5
            ## Časovna zahtevnost: O(N*M) + O(M*K) + T(N, M, K) + 2*O(N*K) + O(N*M) + O(M*K)
            ## Prostorska zahtevnost: P(N, M, K)

            A += D
            E += H
            D1.multiply(A, E, D2)
            S1 += D1                                                    # Novo stanje S1: S1 = P4 - P2 + P5
            S4 += D1                                                    # Novo stanje S4: S4 = P1 - P3 + P5
            A -= D
            E -= H

            # P6
            ## Časovna zahtevnost: O(N*M) + O(M*K) + T(N, M, K) + O(N*K) + O(N*M) + O(M*K)
            ## Prostorska zahtevnost: P(N, M, K)

            B -= D
            G += H
            D1.multiply(B, G, D2)
            S1 += D1                                                    # Podmatrika S1 je sedaj gotova: S1 = P4 - P2 + P5 + P6
            B += D
            G -= H

            # P7
            ## Časovna zahtevnost: O(N*M) + O(M*K) + T(N, M, K) + O(N*K) + O(N*M) + O(M*K)
            ## Prostorska zahtevnost: P(N, M, K)

            A -= C
            E += F
            D1.multiply(A, E, D2)
            S4 -= D1                                                    # Podmatrika S4 je sedaj gotova: S4 = P1 - P3 + P5 - P7
            A += C
            E -= F


            # Poskrbimo še za lihe dimenzije in si pomagamo z delovnimi matrikami.

            if m % 2 != 0:
                for i in range(n):
                    for j in range(k):
                        self[i, j] += left[i, m - 1] * right[m - 1, j]                          # Časovna zahtevnost: O(n*k)
                # Če sta m in k lihe dimenzije:                                                   Prostorska zahtevnost: O(1)
                if k % 2 != 0:
                    self[0:n, k - 1].multiply(left, right[0:m, k - 1], work[0:n, k - 1])        # Časovna zahtevnost: O(n*m)
                    # Če so m, k in n lihe dimenzije:                                              Prostorska zahtevnost: O(1)
                    if n % 2 != 0:
                        self[n - 1, 0:k].multiply(left[n - 1, 0:m], right, work[n - 1, 0:k])    # Časovna zahtevnost: O(m*k)
                # Če sta m in n lihe, k pa sode dimenzije:                                         Prostorska zahtevnost: O(1)
                else:
                    if n % 2 != 0:
                        self[n-1, 0:k].multiply(left[n - 1, 0:m], right, work[n-1, 0:k])
            # Če je m sode dimenzije:
            # Čaovne in prostorske zahtevnosti so pri istih podproblemih identične prejšnjim.
            else:
                # Če je m sode in k lihe dimenzije:
                if k % 2 != 0:
                    self[0:n, k - 1].multiply(left, right[0:m, k - 1], work[0:n, k - 1])
                    # Če je m sode, k in n pa lihe dimenzije:
                    if n % 2 != 0:
                        self[n - 1, 0:k].multiply(left[n - 1, 0:m], right, work[n - 1, 0:k])
                # Če sta m in k sode, n pa lihe stopnje:
                else:
                    self[n - 1, 0:k].multiply(left[n - 1, 0:m], right, work[n - 1, 0:k])
