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
        # left  [  A  |  B   ]  0        [  E  |  F   ]  0   right
        #       [     |      ]           [     |      ]
        #       [------------]  c        [------------]  a
        #       [  C  |  D   ]           [  G  |  H   ]
        #       [     |      ]  d        [     |      ]  b
        #
        #       0     a      b           0     e      f
        #
        #
        # self  [  P  |  Q   ]  0        [  X  |  Y   ]  0   work
        #       [     |      ]           [     |      ]
        #       [------------]  c        [------------]  c
        #       [  R  |  S   ]           [  Z  |  W   ]
        #       [     |      ]  d        [     |      ]  d
        #
        #       0     e      f           0     e      f
        else:
            a = n//2
            b = n - (n % 2)
            c = m//2
            d = m - (m % 2)
            e = o//2
            f = o - (o % 2)
            
            A = left[0:c, 0:a]
            B = left[0:c, a:b]
            C = left[c:d, 0:a]
            D = left[c:d, a:b]
            E = right[0:a, 0:e]
            F = right[0:a, e:f]
            G = right[a:b, 0:e]
            H = right[a:b, e:f]
            
            X = work[0:c, 0:e]
            Y = work[0:c, e:f]
            Z = work[c:d, 0:e]
            W = work[c:d, e:f]
            
            P = self[0:c, 0:e]
            Q = self[0:c, e:f]
            R = self[c:d, 0:e]
            S = self[c:d, e:f]


            # P7 = (A - C) * (E + F)
            A -= C
            E += F
            # S = -P7
            S.multiply(A, E, work = Z)
            S *= -1
            A += C
            E -= F
            Z *= 0

            # P6 = (B - D) * (G + H)
            B -= D
            G += H
            # P = P6
            P.multiply(B, G, work = X)
            B += D
            G -= H
            X *= 0

            # P5 = (A + D) * (E + H)
            A += D
            E += H
            W.multiply(A, E, work = Z)
            A -= D
            E -= H
            # S = P5 - P7
            S += W
            # P = P5 + P6
            P += W
            Z *= 0
            W *= 0

            # P4 = D * (G - E)
            G -= E
            Y.multiply(D, G, work = Z)
            G += E
            # R = P4
            R += Y
            # P = P4 + P5 + P6
            P += Y
            Y *= 0
            Z *= 0

            # P3 = (C + D) * E
            C += D
            X.multiply(C, E, work = Z)
            C -= D
            # R = P3 + P4
            R += X
            # S = P5 - P3 - P7
            S -= X
            X *= 0
            Z *= 0

            # P2 = (A + B) * H
            A += B
            Z.multiply(A, H, work = X)
            A -= B
            # Q = P2
            Q += Z
            # P = P5 + P4 - P2 + P6
            P -= Z
            Z *= 0
            X *= 0

            # P1 = A * (F - H)
            F -= H
            W.multiply(A, F, work = Z)
            F += H
            # Q = P1 + P2
            Q += W
            # S = P1 + P5 - P3 - P7
            S += W
            W *= 0
            Z *= 0

            
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
