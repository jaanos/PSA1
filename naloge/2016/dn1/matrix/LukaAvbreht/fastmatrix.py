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
        levaStol = left.ncol()
        levaVrst = left.nrow()
        desnaStol = right.ncol()
        desnaVrst = right.nrow() ##to je enako kot levaStol
        #Predstavlajmo si da je matrika veliosti 2*n x 2*k
        AA = levaVrst % 2
        BB = desnaStol % 2
        ##Case1 oba sta sodostevilcna
        if AA == 0 and BB == 0:
            if levaVrst == 1 or desnaStol == 1:
                return self.multiply2(left,right)
            A = left[0:levaVrst//2,0:levaStol//2]
            B = left[0:levaVrst//2,levaStol//2:levaStol]
            C = left[levaVrst//2:levaVrst,0:levaStol//2]
            D = left[levaVrst//2:levaVrst,levaStol//2:levaStol]
            E = left[0:desnaVrst//2,0:desnaStol//2]
            F = left[0:desnaVrst//2,desnaStol//2:desnaStol]
            G = left[desnaVrst//2:desnaVrst,0:desnaStol//2]
            H = left[desnaVrst//2:desnaVrst,desnaStol//2:desnaStol]
            P1 = A * (F - H)     #Rekurzivni klic
            P2 = (A + B) * H     #Rekurzivni klic
            P3 = (C + D) * E     #Rekurzivni klic
            P4 = D * (G - E)     #Rekurzivni klic
            P5 = (A+B) * (E+H)   #Rekurzivni klic
            P6 = (B-D) * (G+H)   #Rekurzivni klic
            P7 = (A-C) * (E+F)   #Rekurzivni klic
            self[0:levaStol//2,0:desnaVrst//2] = (P4 + P5 + P6 - P2)
            self[levaStol//2:levaStol,0:desnaVrst//2] = (P3 + P4)
            self[0:levaStol//2,desnaVrst//2:desnaVrst] = (P1 + P2)
            self[levaStol//2:levaStol,desnaVrst//2:desnaVrst] = (P1 + P5 - P3 - P7)
            return self

    def multiply2(self, left, right):
        """To be used only when 1xN or Nx1"""
        assert left.ncol() == right.nrow(), \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        levaStol = left.ncol()
        levaVrst = left.nrow()
        desnaStol = right.ncol()
        #desnaVrst = right.nrow() #ta mora bit enaka k levaStolpci, kar ce ni itak vrnemo v prvi vrstici tko da je nepotrebo
        for i in range(levaVrst):
            trenvrst = []
            for j in range(desnaStol):
                tren = 0
                for k in range(levaStol):
                    tren += (left[i,k]*right[k,j])
                self[i,j] = tren
        return self