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
            
        if left.nrow() == 1:
            for k in range(right.ncol()):
                self[0, k] = skalarni_produkt(left[0,:], right[:, k])
        elif right.ncol() == 1:
            for k in range(left.nrow()):
                self[k, 0] = skalarni_produkt(left[k,:], right[0, k])
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

            print(A,B,C,D,E,F,G,H)
            print("#####")
            print(WORK_1, WORK_2, WORK_3, WORK_4)
            print(self)

            WORK_1.multiply(A,F,WORK_4) #A*F
            WORK_2.multiply(A,H,WORK_3) #A*H
            WORK_1 -= WORK_2 # P1 = A*F - A*H
            clear(WORK_3)
            WORK_3.multiply(B, H, WORK_4) #B*H
            WORK_3 += WORK_2 #P2

            print(S1, S2, S3, S4, WORK_1, WORK_2, WORK_3, WORK_4)
            print(self)

            S2[:,:] = WORK_1 #P1
            S2 += WORK_3 #P1 + P2  --P2 sedaj lahko pozabimo

            print(S1, S2, S3, S4, WORK_1, WORK_2, WORK_3, WORK_4)
            print(self)
            clear(WORK_3)
            WORK_3.multiply(A, E, S1) #A*E
            S3.multiply(D, E, S1) #D*E
            WORK_4.multiply(D, H, S1) #D*H

            print(S1, S2, S3, S4, WORK_1, WORK_2, WORK_3, WORK_4)
            print(self)
            S4[:,:] = WORK_1 #To je zadnjic ko bomo uporabili P1
            clear(WORK_1)
            WORK_1[:,:] = WORK_3
            WORK_1 += WORK_2
            WORK_1 += S3
            WORK_1 += WORK_4 #Na mestu WORK_1 je sedaj shranjena matrika P5

            print(S1, S2, S3, S4, WORK_1, WORK_2, WORK_3, WORK_4)
            print(self)            
            clear(WORK_2)
            WORK_2.multiply(C, E, S1) # C*E
            S3 += WORK_2 # C*E + D*E = P3, Na polju S3 imamo sedaj P3 matriko

            print(S1, S2, S3, S4, WORK_1, WORK_2, WORK_3, WORK_4)
            print(self)
            WORK_3 -= WORK_2 #WORK_3 = A*E - C*E
            clear(WORK_2)
            WORK_2.multiply(A, F, S1)
            WORK_3 += WORK_2 #WORK_3 = A*E - C*E + A*F

            print(S1, S2, S3, S4, WORK_1, WORK_2, WORK_3, WORK_4)
            print(self)
            clear(WORK_2)
            WORK_2.multiply(C,F, S1)
            WORK_3 -= WORK_2 # WORK_3 = A*E - C*E + A*F - C*F = P7

            print(S1, S2, S3, S4, WORK_1, WORK_2, WORK_3, WORK_4)
            print(self)
            S4 += WORK_1
            S4 -= S3
            S4 -= WORK_3

            print("####", S4)

            clear(WORK_2)
            WORK_2.multiply(D, G, S1) # D*G
            clear(WORK_4)
            WORK_4.multiply(D, E, S1) # D*E
            WORK_2 -= WORK_4 # D*G - D*E = P4

            print(S1, S2, S3, S4, WORK_1, WORK_2, WORK_3, WORK_4)
            print(self)
            S3 += WORK_2 #Sedaj moramo urediti le še polje S1 = P4 + P5 + P6 + P7

            clear(S1)
            S1 += WORK_2
            S1 += WORK_3
            S1 += WORK_1 # S1 = P4 + P5 + P7

            print(S1, S2, S3, S4, WORK_1, WORK_2, WORK_3, WORK_4)
            print(self)
            #Na mestu S1 moramo sedaj le še prišteti P6 = B*G + B*H - D*G - D*H
            clear(WORK_1)
            WORK_1.multiply(B, G, WORK_4)
            S1 += WORK_1

            clear(WORK_1)
            WORK_1.multiply(B, H, WORK_4)
            S1 += WORK_1
            
            clear(WORK_1)
            WORK_1.multiply(D,G, WORK_4)
            S1 -= WORK_1

            clear(WORK_1)
            WORK_1.multiply(D, H, WORK_4)
            S1 -= WORK_1 

            print(S1, S2, S3, S4, WORK_1, WORK_2, WORK_3, WORK_4)
            print(self)            
            
            

            
            

            
            




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
    for i in range(matrix.nrow()):
        for j in range(matrix.ncol()):
            matrix[i,j] = 0

