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
        if levaVrst == 1 or desnaStol == 1:
            super().multiply(left,right)
            return self
        if AA == 0 and BB == 0:
            A = left[0:levaVrst//2,0:levaStol//2]
            B = left[0:levaVrst//2,levaStol//2:levaStol]
            C = left[levaVrst//2:levaVrst,0:levaStol//2]
            D = left[levaVrst//2:levaVrst,levaStol//2:levaStol]
            E = right[0:desnaVrst//2,0:desnaStol//2]
            F = right[0:desnaVrst//2,desnaStol//2:desnaStol]
            G = right[desnaVrst//2:desnaVrst,0:desnaStol//2]
            H = right[desnaVrst//2:desnaVrst,desnaStol//2:desnaStol]
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
            self[0:levaStol//2,0:desnaVrst//2] = (P4 + P5 + P6 - P2)
            self[levaStol//2:levaStol,0:desnaVrst//2] = (P3 + P4)
            self[0:levaStol//2,desnaVrst//2:desnaVrst] = (P1 + P2)
            self[levaStol//2:levaStol,desnaVrst//2:desnaVrst] = (P1 + P5 - P3 - P7)
            return self
        if AA == 0 and BB == 1:
            #primer ko je leva matrika sodo visokam desna pa liho siroka (Ma en stolpec vec desna)



            return self
        if AA == 1 and BB == 0:
            #Pol je leva matrika eno vrstico vec spodi


            return self
        if AA == 1 and BB == 1:
            #Pol je pa pr obeh ena vrstica Oz en stolpec vec

            return self

        #mogoce bi lahk sam pgledu dva primera pa popravu sam k je kej prevec in cee je oboje prevec sam naredu oboje, ce je to razumlivo