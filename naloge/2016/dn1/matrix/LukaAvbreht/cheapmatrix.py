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
        levaVrst = left.nrow()
        ujemanje = left.ncol()
        desnaStol = right.ncol()
        AA = levaVrst % 2
        BB = desnaStol % 2
        CC = ujemanje % 2
        if levaVrst == 1 or desnaStol == 1 or ujemanje == 1:
            super().multiply(left,right)
            return self
        if CC == 0: #Primer ko je sirina leve matrike = visina desne sodo stevilo
            if BB == 1:
                #primer ko je leva matrika sodo visokam desna pa liho siroka (Ma en stolpec vec desna)
                work*=0
                self[0:levaVrst,0:(desnaStol-1)].multiply(left,right[0:ujemanje,0:(desnaStol-1)],work[0:levaVrst,0:(desnaStol-1)])  #tuki sam locis primer in je sam vazn da je work zravn da dela
                work*=0
                self[0:levaVrst,(desnaStol-1):desnaStol].multiply(left,right[0:ujemanje,(desnaStol-1):desnaStol],work[0:levaVrst,(desnaStol-1):desnaStol])
                return self
            if AA == 1:
                #Pol je leva matrika eno vrstico vec spodi
                work*=0
                self[0:(levaVrst-1),0:desnaStol].multiply(left[0:(levaVrst-1),0:ujemanje],right,work[0:(levaVrst-1),0:desnaStol])
                work*=0
                self[(levaVrst-1):levaVrst,0:desnaStol].multiply(left[(levaVrst-1):levaVrst,0:ujemanje],right,work[(levaVrst-1):levaVrst,0:desnaStol])
                return self
            #Priprava matrik (sekanje)
            A = left[0:levaVrst//2,0:ujemanje//2]
            B = left[0:levaVrst//2,ujemanje//2:ujemanje]
            C = left[levaVrst//2:levaVrst,0:ujemanje//2]
            D = left[levaVrst//2:levaVrst,ujemanje//2:ujemanje]
            E = right[0:ujemanje//2,0:desnaStol//2]
            F = right[0:ujemanje//2,desnaStol//2:desnaStol]
            G = right[ujemanje//2:ujemanje,0:desnaStol//2]
            H = right[ujemanje//2:ujemanje,desnaStol//2:desnaStol]
            #Priprava matrik na P1,P2,...,P7
            #dodatno delovno matriko bomo v zgornjem levem kotu uporabljali za rekurzijo ostale kvadrate pa zapolnili z
            #zvito izbranimi matrikami P1 do P7
            #Podmatrike med seboj odstevamo in pristevamo na mestu, da ne generiramo novih
            #V vsakem koraku poklicemo rekurzivni klic na manjših matrikah
            REKURZIVNA = work[0:(levaVrst//2),0:(desnaStol//2)]
            G-=E
            P4 = self[0:(levaVrst//2),0:(desnaStol//2)]
            P4.multiply(D,G,REKURZIVNA)  #P4
            G+=E

            A+=B
            P2 = self[0:(levaVrst//2),(desnaStol//2):desnaStol]
            P2.multiply(A,H,REKURZIVNA)  #P2
            A-=B

            C+=D
            P3 = self[(levaVrst//2):levaVrst,0:(desnaStol//2)]
            P3.multiply(C,E,REKURZIVNA)  #P3
            C-=D

            F-=H
            P1 = self[(levaVrst//2):levaVrst,(desnaStol//2):desnaStol]
            P1.multiply(A,F,REKURZIVNA)  #P1
            F+=H

            A+=D
            E+=H
            P5 = work[0:(levaVrst//2),(desnaStol//2):desnaStol]
            P5.multiply(A,E,REKURZIVNA)  #P5
            A-=D
            E-=H

            B-=D
            G+=H
            P6 = work[(levaVrst//2):levaVrst,0:(desnaStol//2)]
            P6.multiply(B,G,REKURZIVNA)  #P6
            B+=D
            G-=H

            A-=C
            E+=F
            P7 = work[(levaVrst//2):levaVrst,(desnaStol//2):desnaStol]
            P7.multiply(A,E,REKURZIVNA)  #P7
            A+=C
            E-=F

            #Po izracunanih matrikah pripravimo resitev
            REKURZIVNA*=0
            REKURZIVNA+=P1
            P3+=P4
            P1-=P3
            P1+=P4
            P4-=P2
            P2+=REKURZIVNA
            P4+=P5
            P4+=P6
            P1-=P7
            P1+=P5
            return self