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
        for i in range(left.nrow()):
            for j in range(right.ncol()):
                temp = 0
                for k in range(right.nrow()):
                    temp += left[i, k]*right[k, j]
                self[i, j] = temp
