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

        i = 0
        while (i < left.nrow()):
            j = 0
            while (j < right.ncol()):
                v = 0
                while (v < right.nrow()):
                    #rezultatu sestevamo ustrezne produkte elementov matrike left in right, da nastane skalarni produkt
                    self[i, j] = self[i, j] + left[i, v] * right[v, j]
                    v = v + 1
                j = j + 1
            i = i + 1

