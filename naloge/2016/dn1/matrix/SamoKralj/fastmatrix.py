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
        if left.nrow() == 1:
            for k in range(right.ncol()):
                self[0,k] = skalarni_produkt(left[0,:], right[:, k])
        elif right.ncol() == 1:
            for k in range(left.nrow()):
                self[k, 0] = skalarni_produkt(left[k,:], right[:, 0])
        else:
            A, B, C, D = razdeli_levo_matriko(left)
            E, F, G, H = razdeli_desno_matriko(right)
            P1 = A*(F-H)
            P2 = (A+B)*H
            P3 = (C+D)*E
            P4 = D*(G-E)
            P5 = (A+D)*(E+H)
            P6 = (B-D)*(G+H)
            P7 = (A-C)*(E+F)
            """
            print(P1, "\n #######")
            print(P2, "\n #######")
            print(P3, "\n #######")
            print(P4, "\n #######")
            print(P5, "\n #######")
            print(P6, "\n #######")
            print(P7, "\n #######")
            """
            zgornji_levi = P4 + P5 + P6 - P2
            zgornji_desni = P1 + P2
            spodnji_levi = P3 + P4
            spodnji_desni = P1 + P5 - P3 - P7
            if left.ncol() % 2 == 1:
                lr2 = left.nrow()//2
                lc2 = left.ncol()//2
                lc = left.ncol() - 1
                rr2 = right.nrow()//2
                rc2 = right.ncol()//2
                rr = right.nrow() - 1
                zgornji_levi += left[:lr2, lc]*right[rr, :rc2]
                zgornji_desni += left[:lr2, lc] * right[rr, rc2:2*rc2]
                spodnji_levi += left[lr2:2*lr2, lc] * right[rr, :rc2]
                spodnji_desni += left[lr2:2*lr2, lc] * right[rr, rc2:2*rc2]
            """
            print(zgornji_levi, "\n #######%%%%%%")
            print(zgornji_desni, "\n #######%%%%%")
            print(spodnji_levi, "\n #######%%%%%%")
            print(spodnji_desni, "\n #######%%%%%")
            """
            self[:zgornji_levi.nrow(), :zgornji_levi.ncol()] = zgornji_levi
            self[:zgornji_desni.nrow(), zgornji_levi.ncol():zgornji_levi.ncol() + zgornji_desni.ncol()] = zgornji_desni
            self[zgornji_levi.nrow():zgornji_levi.nrow() + spodnji_levi.nrow(), :spodnji_levi.ncol()] = spodnji_levi
            self[zgornji_desni.nrow():zgornji_levi.nrow() + spodnji_desni.nrow(), spodnji_levi.ncol(): spodnji_levi.ncol() + spodnji_desni.ncol()] = spodnji_desni
            if left.nrow() % 2 == 1:
                for k in range(right.ncol()):
                    self[left.nrow() - 1, k] = skalarni_produkt(left[left.nrow() - 1, :], right[:, k])
            if right.ncol() % 2 == 1:
                for k in range(left.nrow()):
                    self[k, right.ncol() - 1] = skalarni_produkt(left[k, :], right[:, right.ncol() - 1])
            
            

def skalarni_produkt(u, v):
    produkt = 0
    for i in range(u.ncol()):
        produkt += u[0, i] * v[i, 0]
    return produkt
        
def razdeli_levo_matriko(M):
    row = M.nrow()//2
    col = M.ncol()//2
    A = M[:row, :col]
    B = M[:row, col:2*col]
    C = M[row:2*row, :col]
    D = M[row:2*row, col:2*col]
    """
    print("####")
    print(A)
    print("###")
    print(B)
    print("####")
    print(C)
    print("####")
    print(D)
    print("$$$$")
    """
    return A, B, C, D

def razdeli_desno_matriko(M):
    row = M.nrow()//2
    col = M.ncol()//2
    A = M[:row, :col]
    B = M[:row, col:2*col]
    C = M[row:2*row, :col]
    D = M[row:2*row, col:2*col]
    """
    print("####")
    print(A)
    print("###")
    print(B)
    print("####")
    print(C)
    print("####")
    print(D)
    print("$$$$")
    """
    return A, B, C, D

    
