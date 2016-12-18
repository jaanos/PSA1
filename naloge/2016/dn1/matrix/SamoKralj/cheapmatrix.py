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

            WORK_1.multiply(A,F,WORK_4) #A*F
            WORK_2.multiply(A,H,WORK_3) #A*H
            WORK_1 -= WORK_2 # P1 = A*F - A*H
            WORK_3.multiply(B, H, WORK_4) #B*H
            WORK_3 += WORK_2 #P2

            S2[:,:] = WORK_1 #P1
            S2 += WORK_3 #P1 + P2

            WORK_4.multiply(A, E, S1) #A*E
            S3.multiply(D, E, S1) #D*E
            S4.multiply(D, H, S1) #D*H

            WORK_2 += WORK_4
            WORK_2 += S3
            WORK_2 += S4 #WORK_2 = A*E + A*H + D*E + D*H = P5
            S4[:,:] = WORK_1 #To je zadnjic ko bomo uporabili P1           

            WORK_4.multiply(C, E, S1) # C*E
            S3 += WORK_4 #S3 = D*E + C*E = P3

            S4 += WORK_2
            S4 -= S3
            S4 += WORK_4 # S4 = P1 + P5 - P3 + C*E (manjka še - A*E - A*F + C*F)

            WORK_4.multiply(A, E, S1)
            S4 -= WORK_4

            WORK_4.multiply(A,F, S1)
            S4 -= WORK_4

            WORK_4.multiply(C, F, S1)
            S4 += WORK_4 #S4 = P1 + P5 - P3 - P7

            """
            Trenutno stanje:
            S1 = ??
            S2 = Pravilna vrednost
            S3 = P3
            S4 = Pravilna vrednost
            WORK_1 = P1
            WORK_2 = P5
            WORK_3 = P2
            WORK_4 = C*F
            """

            WORK_1.multiply(D, G, S1)
            S3 += WORK_1

            WORK_4.multiply(D, E, S1)
            S3 -= WORK_4

            """
            Trenutno stanje:
            S1 = ??
            S2 = Pravilna vrednost
            S3 = Pravilna Vrednost
            S4 = Pravilna vrednost
            WORK_1 = D*G
            WORK_2 = P5
            WORK_3 = P2
            WORK_4 = D*E
            """

            S1[:,:] = WORK_1
            S1 -= WORK_4 #S1 = P4
            S1 += WORK_2 #S1 = P4 + P5
            S1 -= WORK_3 #S1 = P4 + P5 - P2
            S1 -= WORK_1 #S1 = P4 + P5 - P2 - D*G

            WORK_2.multiply(B,G, WORK_4)
            S1 += WORK_2

            WORK_2.multiply(B,H, WORK_4)
            S1 += WORK_2

            WORK_2.multiply(D, H, WORK_4)
            S1 -= WORK_2

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

