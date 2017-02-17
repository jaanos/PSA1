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

        lv = left.nrow()
        ls = left.ncol()
        ds = right.ncol()

        for i in range(lv):                         #izberemo vrstico v prvi matriki
            for j in range(ds):                     #izberemo stolpec v drugi matriki
                elt = 0
                for k in range(ls):                 #gremo po vseh eltih v izbrani vrstici/stolpcu
                    elt += left[i,k]*right[k,j]
                self[i,j] = elt                     #izracunani elt dodamo v ciljno matriko


