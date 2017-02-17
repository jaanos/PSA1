# -*- coding: utf-8 -*-
from .slowmatrix import SlowMatrix

import math

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

        self[0:left.nrow(),0:right.ncol()] = strassen(left,right) #rezultat poiscemo s strassenovim algoritmom


def zmnozi(left,right):
    """naivno zmnozi dve matriki"""
    work = FastMatrix(None,left.nrow(),right.ncol()) #ustvari si delovno matriko, kjer si shranjuje rezultate
    i = 0
    while (i < left.nrow()):
        j = 0
        while (j < right.ncol()):
            v = 0
            while (v < right.nrow()): #elementu delavne matrike pristeva potrebne zmnozke elementov leve in desne matrike
                                      #tako da nastane skalarni produkt
                work[i, j] = work[i, j] + left[i, v] * right[v, j]
                v = v + 1
            j = j + 1
        i = i + 1
    return work


def strassen(left,right):
    lv = left.nrow() #stevilo vrstic leve matrike
    ls = left.ncol() #stevilo stolpcev leve matrike = stevilo vrstic desne matrike
    ds = right.ncol() #stevilo stolpcev desne matrike
    work = FastMatrix(None, lv, ds) #ustvari si delovno matriko
    if (any([lv == 1, ls == 1, ds == 1])): #ce je katera od stranic matrik enaka 1, izvede naivno mnozenje.
        return zmnozi(left, right)

    elif (lv % 2 == 0 and ls % 2 == 0 and ds % 2 == 0):#ce so vse stranice matrik deljive z 2 naredimo:
        #matriki left in right razdelimo na 4 dele
        A11 = left[0:(lv / 2), 0:(ls / 2)]
        A12 = left[0:(lv / 2), (ls / 2):ls]
        A21 = left[(lv / 2):lv, 0:(ls / 2)]
        A22 = left[(lv / 2):lv, (ls / 2):ls]

        B11 = right[0:(ls / 2), 0:(ds / 2)]
        B12 = right[0:(ls / 2), (ds / 2):ds]
        B21 = right[(ls / 2):ls, 0:(ds / 2)]
        B22 = right[(ls / 2):ls, (ds / 2):ds]

        #izracunamo 7 mnozenj matrik
        M1 = (A11 + A22) * (B11 + B22)
        M2 = (A21 + A22) * (B11)
        M3 = (A11) * (B12 - B22)
        M4 = (A22) * (B21 - B11)
        M5 = (A11 + A12)* (B22)
        M6 = (A21 - A11) * (B11 + B12)
        M7 = (A12 - A22) * (B21 + B22)

        #delovno matriko nastavimo na ustrezne vrednosti
        work[0:(lv / 2), 0:(ds / 2)] = M1 + M4 - M5 + M7
        work[0:(lv / 2), (ds / 2):ds] = M3 + M5
        work[(lv / 2):lv, 0:(ds / 2)] = M2 + M4
        work[(lv / 2):lv, (ds / 2):ds] = M1 - M2 + M3 + M6
    elif (lv % 2 == 1):#ce stevilo vrstic leve matrike ni deljivo z 2 naredimo:
        # matriko left razdelimo na   [A11]
        #                             [A21]
        #kjer je A21 enovrsticna matrika
        A1 = left[0:(lv - 1), 0:ls]
        A2 = left[(lv - 1):lv, 0:ls]
        #zmnozimo A1 in right ter A2 in right
        A1B = A1 * right
        A2B = A2 * right
        #nastavimo zgornji del matrike work(razdeljena tako kot left) na A1B, spodnji pa na A2B
        work[0:(lv-1), 0:ds] = A1B
        work[(lv-1):lv, 0:ds] = A2B

    elif (ls % 2 == 1):#ce stevilo levih stolpcev ni deljivo z 2 naredimo:
        # matriko right razdelimo na   [B1]
        #                              [B2]
        # kjer je B21 enovrsticna matrika
        # matriko left razdelimo na   [[A11],[A21]]
        # kjer je A21 enostolpicna matrika
        A1 = left[0:lv, 0:(ls - 1)]
        A2 = left[0:lv, (ls - 1):ls]
        B1 = right[0:(ls - 1), 0:ds]
        B2 = right[(ls - 1):ls, 0:ds]
        #naredimo zmnozke A1*B1 in A2*B2
        A1B1 = A1*B1
        A2B2 = A2*B2
        #delovno matriko work nastavimo na sestevek A1B1+A2B2
        work[0:lv, 0:ds] = A1B1 + A2B2


    elif (ds % 2 == 1):#ce stevilo desnih stolpcev ni deljivo z 2 naredimo:
        # matriko right razdelimo na   [B1]
        #                              [B2]
        B1 = right[0:ls, 0:(ds - 1)]
        B2 = right[0:ls, (ds - 1):ds]
        #izvedemo mnozenje left*B1 in left*B2
        AB1 = zmnozi(left,B1)
        AB2 = zmnozi(left,B2)
        #zgornji del matrike work(razdeljena kot B) nastavimo na AB1, spodnji pa na AB2
        work[0:lv, 0:ds-1] = AB1
        work[0:lv,(ds-1):ds] = AB2
    return work