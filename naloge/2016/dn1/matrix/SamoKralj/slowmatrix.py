# -*- coding: utf-8 -*-
from ..matrix import AbstractMatrix

class SlowMatrix(AbstractMatrix):
    """
    Matrika z naivnim množenjem.
    """
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
        dolzina_vrstice = left.ncol()
        for vrstica in range(left.nrow()):
            for stolpec in range(right.ncol()):
                self[vrstica, stolpec] = skalarni_produkt(left[vrstica, :], right[:,stolpec])
                
def skalarni_produkt(u, v):
    produkt = 0
    for i in range(u.ncol()):
        produkt += u[0, i] * v[i, 0]
    return produkt
    
