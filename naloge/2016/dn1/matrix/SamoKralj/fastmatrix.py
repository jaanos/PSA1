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

        """
        Če je število vrstic leve matrike enako 1 oziroma število stolpcev
        desne matrike enako 1, potem ne moremo matrike več deliti in samo
        zmnožimo matriki.
        """

        if left.nrow() == 1:
            for k in range(right.ncol()):
                self[0,k] = skalarni_produkt(left[0,:], right[:, k])
        elif right.ncol() == 1:
            for k in range(left.nrow()):
                self[k, 0] = skalarni_produkt(left[k,:], right[:, 0])
        else:
            A, B, C, D = razdeli_matriko(left)
            E, F, G, H = razdeli_matriko(right)
            P1 = A*(F-H)
            P2 = (A+B)*H
            P3 = (C+D)*E
            P4 = D*(G-E)
            P5 = (A+D)*(E+H)
            P6 = (B-D)*(G+H)
            P7 = (A-C)*(E+F)

            zgornji_levi = P4 + P5 + P6 - P2
            zgornji_desni = P1 + P2
            spodnji_levi = P3 + P4
            spodnji_desni = P1 + P5 - P3 - P7

            #Oznaka dolžin za bolj pregledno kodo.
            LR2 = left.nrow()//2
            LC2 = left.ncol()//2
            LC = left.ncol() - 1
            LR = left.nrow() - 1
            RR2 = right.nrow()//2
            RC2 = right.ncol()//2
            RR = right.nrow() - 1
            RC = right.ncol() - 1
            
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
                zgornji_levi += left[:LR2, LC]*right[RR, :RC2]
                zgornji_desni += left[:LR2, LC] * right[RR, RC2:2*RC2]
                spodnji_levi += left[LR2:2*LR2, LC] * right[RR, :RC2]
                spodnji_desni += left[LR2:2*LR2, LC] * right[RR, RC2:2*RC2]

            self[:LR2, :RC2] = zgornji_levi
            self[:LR2, RC2:2*RC2] = zgornji_desni
            self[LR2:2*LR2, :RC2] = spodnji_levi
            self[LR2:2*LR2, RC2:2*RC2] = spodnji_desni
            
            if left.nrow() % 2 == 1:
                """
                Ročno primnožimo še najnižjo vrstico, ki je smo jo pri
                delitvi na podmatrike izpustili.
                """
                for k in range(right.ncol()):
                    self[LR, k] = skalarni_produkt(left[LR, :], right[:, k])
            if right.ncol() % 2 == 1:
                """
                Primnožimo še zadnji stolpec.
                """
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
        
def razdeli_matriko(M):
    """
    Razdeli matriko na 4 podmatrike enake velikosti in sicer tako, da ignorira
    liho število vrstic oziroma stolpcev. Tako bo matriko
    velikosti (2*n + 1) * (2*m + 1) razdelil na 4 podmatrike
    velikosti n*m.
    """
    row = M.nrow()//2
    col = M.ncol()//2
    A = M[:row, :col]
    B = M[:row, col:2*col]
    C = M[row:2*row, :col]
    D = M[row:2*row, col:2*col]
    return A, B, C, D

    
