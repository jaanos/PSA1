# -*- coding: utf-8 -*-
from ..matrix import AbstractMatrix

class SlowMatrix(AbstractMatrix):
    """
    Matrika z naivnim množenjem.
    """
    def nicelna_matrika(self,a,b):
        c=b*[0]
        d=[c for i in range(a)]
        return SlowMatrix(d,a,b)
    def slabo_mnozenje(self,druga):
        if self.ncol()!=druga.nrow():
            return "ni mogoce"
        else:
            vrstice1=self.nrow()
            stolpci1=self.ncol()
            vrstice2=druga.nrow()
            stolpci2=druga.ncol()
            nula=self.nicelna_matrika(vrstice1,stolpci2)
            for i in range(vrstice1):
                for j in range(stolpci2):
                    k=0
                    for x in range(stolpci1):                    
                        k+=self[i,x]*druga[x,j]
                    nula[i,j]=k
            return nula
    def multiply(self, left, right):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Množenje izvede z izračunom skalarnih produktov
        vrstic prve in stolpcev druge matrike.
        """
        assert left.ncol() == right.nrow(), \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        #raise NotImplementedError("Naredi sam!")
        self[:left.nrow(),:right.ncol()]=left.slabo_mnozenje(right)
