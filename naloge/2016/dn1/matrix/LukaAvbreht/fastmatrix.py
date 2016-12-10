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
        ujemanje = left.ncol()
        levaVrst = left.nrow()  # = self.nrow()
        desnaStol = right.ncol()  # = self.ncol()
        #Predstavlajmo si da je matrika veliosti 2*n x 2*k
        AA = levaVrst % 2
        BB = desnaStol % 2
        CC = ujemanje % 2
        ##Case1 oba sta sodostevilcna
        if levaVrst == 1 or desnaStol == 1 or ujemanje == 1:
            super().multiply(left,right)
            return self
        if CC == 0: #Primer ko je sirina leve matrike = visina desne sodo stevilo
            if BB == 1:
                #primer ko je leva matrika sodo visokam desna pa liho siroka (Ma en stolpec vec desna)
                self[0:levaVrst,0:(desnaStol-1)] = left * right[0:ujemanje,0:(desnaStol-1)]
                self[0:levaVrst,(desnaStol-1):desnaStol] = left * right[0:ujemanje,(desnaStol-1):desnaStol]
                return self
            if AA == 1:
                #Pol je leva matrika eno vrstico vec spodi
                self[0:(levaVrst-1),0:desnaStol] = left[0:(levaVrst-1),0:ujemanje] * right
                self[(levaVrst-1):levaVrst,0:desnaStol] = left[(levaVrst-1):levaVrst,0:ujemanje] * right
                return self
            A = left[0:levaVrst//2,0:ujemanje//2]
            B = left[0:levaVrst//2,ujemanje//2:ujemanje]
            C = left[levaVrst//2:levaVrst,0:ujemanje//2]
            D = left[levaVrst//2:levaVrst,ujemanje//2:ujemanje]
            E = right[0:ujemanje//2,0:desnaStol//2]
            F = right[0:ujemanje//2,desnaStol//2:desnaStol]
            G = right[ujemanje//2:ujemanje,0:desnaStol//2]
            H = right[ujemanje//2:ujemanje,desnaStol//2:desnaStol]
            # for i,j in [(A,"A"),(B,"B"),(C,"C"),(D,"D"),(E,"E"),(F,"F"),(G,"G"),(H,"H")]:
            #     print(i,j)
            #     print("nova matrika")
            P1 = A * (F - H)     #Rekurzivni klic
            P2 = (A + B) * H     #Rekurzivni klic
            P3 = (C + D) * E     #Rekurzivni klic
            P4 = D * (G - E)     #Rekurzivni klic
            P5 = (A+D) * (E+H)   #Rekurzivni klic
            P6 = (B-D) * (G+H)   #Rekurzivni klic
            P7 = (A-C) * (E+F)   #Rekurzivni klic
            # for j in [P1,P2,P3,P4,P5,P6,P7]:
            #     print(j)
            #     print("jji")
            self[0:levaVrst//2,0:desnaStol//2] = (P4 + P5 + P6 - P2)
            self[levaVrst//2:levaVrst,0:desnaStol//2] = (P3 + P4)
            self[0:levaVrst//2,desnaStol//2:desnaStol] = (P1 + P2)
            self[levaVrst//2:levaVrst,desnaStol//2:desnaStol] = (P1 + P5 - P3 - P7)
            return self
        if CC == 1: #Primer ko je sirina leve matrike = visina desne liho stevilo
            if BB == 1:#primer ko je leva matrika sodo visokam desna pa liho siroka (Ma en stolpec vec desna)
                self[0:levaVrst,0:(desnaStol-1)] = left[0:levaVrst,0:(ujemanje-1)] * right[0:(ujemanje-1),0:(desnaStol-1)] +\
                                                   left[0:levaVrst,(ujemanje-1):ujemanje] * right[(ujemanje-1):ujemanje,0:(desnaStol-1)]
                self[0:levaVrst,(desnaStol-1):desnaStol] = left * right[0:(ujemanje),(desnaStol-1):desnaStol]
                return self
            if AA == 1:
                self[0:(levaVrst-1),0:desnaStol] = left[0:(levaVrst-1),0:(ujemanje-1)] * right[0:(ujemanje-1),0:desnaStol] +\
                                                   left[0:(levaVrst-1),(ujemanje-1):ujemanje] * right[(ujemanje-1):ujemanje,0:desnaStol]
                self[(levaVrst-1):levaVrst,0:desnaStol] = left[(levaVrst-1):levaVrst,0:ujemanje] * right
                return self
            else:
                AAA = left[0:levaVrst,0:(ujemanje-1)] * right[0:(ujemanje-1),0:desnaStol]
                BBB = left[0:levaVrst,(ujemanje-1):ujemanje] * right[(ujemanje-1):ujemanje,0:desnaStol]
                CCC = AAA + BBB
                self *= 0
                self += CCC
                return self