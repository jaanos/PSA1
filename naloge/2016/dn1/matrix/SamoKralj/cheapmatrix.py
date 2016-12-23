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

        clear(work)
        clear(self)
            
        if left.nrow() == 1:
            for k in range(right.ncol()):
                self[0,k] = skalarni_produkt(left[0,:], right[:, k])
        elif right.ncol() == 1:
            for k in range(left.nrow()):
                self[k, 0] = skalarni_produkt(left[k,:], right[:, 0])
        else:
            """
            Imamo matrike velikosti (2*n + 1) x (2*m + 1): 
            |A B x |   *   | E F a |
            |C D y |       | G H b |
            |u  v  |       | c  d  |

            Kjer so polja oznacena z malimi črkami vektorji ustreznih dolžin.
            Našo matriko bomo zmnožili tako, da bomo najprej zmnožili sod del
            in nato posebej obravnavali zadnje lihe vrstice in stolpce.
            """

            #Oznake za lepšo kodo
            visina_l = left.nrow()//2
            sirina_l = left.ncol()//2
            visina_r = right.nrow()//2
            sirina_r = right.ncol()//2

            A = left[:visina_l, :sirina_l]
            B = left[:visina_l, sirina_l:2*sirina_l]
            C = left[visina_l:2*visina_l, :sirina_l]
            D = left[visina_l:2*visina_l, sirina_l:2*sirina_l]

            E = right[:visina_r, :sirina_r]
            F = right[:visina_r, sirina_r : 2*sirina_r]
            G = right[visina_r : 2*visina_r, :sirina_r]
            H = right[visina_r : 2*visina_r, sirina_r : 2*sirina_r]

            WORK_1 = work[:visina_l, :sirina_r]
            WORK_2 = work[:visina_l, sirina_r:2*sirina_r]
            WORK_3 = work[visina_l:2*visina_l, :sirina_r]
            WORK_4 = work[visina_l:2*visina_l, sirina_r:2*sirina_r]

            S1 = self[:visina_l, :sirina_r]
            S2 = self[:visina_l, sirina_r:2*sirina_r]
            S3 = self[visina_l:2*visina_l, :sirina_r]
            S4 = self[visina_l:2*visina_l, sirina_r:2*sirina_r]

            F -= H
            WORK_1.multiply(A,F, WORK_4) #Matrika P1
            F += H

            A += B
            WORK_2.multiply(A, H, WORK_4) #Matrika P2
            A -= B

            S2 += WORK_1
            S2 += WORK_2

            #Na mestu S2 v matriki je sedaj prava vrednost.

            S4 += WORK_1
            #Sedaj lahko na matriko P1 pozabimo.
            
            C += D
            WORK_1.multiply(C, E, WORK_4) #Matrika P3
            C -= D

            A += D
            E += H
            S1.multiply(A, E, WORK_4) #Matrika P5
            A -= D
            E -= H

            A -= C
            E += F
            WORK_3.multiply(A, E, WORK_4) #Matrika P7
            A += C
            E -= F

            S4 -= WORK_3
            S4 -= WORK_1
            S4 += S1
            #Na mestu S4 je sedaj prava vrednost.

            S1 -= WORK_2 # S1 = P5 - P2

            """
            Trenutno Stanje:
            S1 = P5 - P2
            S2 = Prava vrednost
            S3 = Prazno
            S4 = Prava vrednost
            WORK_1 = P3
            WORK_2 = P2
            WORK_3 = P7
            WORK_4 = random
            """

            S3 += WORK_1
            #Na matriko P3 lahko sedaj pozabimo.

            G -= E
            WORK_1.multiply(D, G, WORK_4) #Matrika P4
            G += E

            S3 += WORK_1
            #Na mestu S3 je sedaj prava vrednost.

            S1 += WORK_1 # S1 = P5 - P2 + P4

            B -= D
            G += H
            WORK_1.multiply(B, G, WORK_4) #Matrika P6
            B += D
            G -= H

            S1 += WORK_1
            #Na mestu S1 je sedaj prava vrednost.

            if left.ncol() % 2 == 1:
                """
                V primeru, da ima leva matrika liho število stolpcev moramo
                vsaki podmatriki dodati še nek člen, kar je vidno iz izpeljave.

                X = | A B x | 
                    | C D y |
                    
                Y = | E F |
                    | G H |
                    | z w |

                Kjer so x,y in z,w podmatrike, ki imajo širino oz. višino 1.

                V produktu X*Y bo v zgornjem levem kotu člen:

                A*E + B*G + x * z

                A*E + B*G dobimo z strassenovim algoritmom za sodo število stolpcev.
                Člen x*z pa moramo dodati sami.

                Podoben razmislek tudi za ostale 3 podmatrike.
                """
                
                RR = right.nrow() - 1
                LC = left.ncol() - 1

                WORK_1.multiply(left[:visina_l,LC], right[RR, :sirina_r])
                S1 += WORK_1

                WORK_1.multiply(left[:visina_l, LC], right[RR, sirina_r:2*sirina_r])
                S2 += WORK_1

                WORK_1.multiply(left[visina_l:2*visina_l, LC], right[RR, :sirina_r])
                S3 += WORK_1

                WORK_1.multiply(left[visina_l:2*visina_l, LC], right[RR, sirina_r:2*sirina_r])
                S4 += WORK_1
            
            if left.nrow() % 2 == 1:
                """
                Ročno primnožimo še najnižjo vrstico, ki je smo jo pri
                delitvi na podmatrike izpustili.
                """
                LR = left.nrow() - 1
                for k in range(right.ncol()):
                    self[LR, k] = skalarni_produkt(left[LR, :], right[:, k])

            if right.ncol() % 2 == 1:
                """
                Primnožimo še zadnji stolpec.
                """
                RC = right.ncol() - 1
                for k in range(left.nrow()):
                    self[k, RC] = skalarni_produkt(left[k, :], right[:, RC])

def skalarni_produkt(u, v):
    """
    Izračuna skalarni produkt dveh vektorjev. Pri tem je u podan kot
    vrstica in v podan kot stolpec.
    """
    produkt = 0
    for i in range(u.ncol()):
        produkt += u[0, i] * v[i, 0]
    return produkt

def clear(matrix):
    """
    Funkcija, ki nam počisti matriko.

    Kot argument bo prejela matriko in jo nastavila na 0.
    """
    for i in range(matrix.nrow()):
        for j in range(matrix.ncol()):
            matrix[i,j] = 0
