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
        #množimo matriki velikosti m x k in k x n
        m = left.nrow()
        n = right.ncol()
        k = left.ncol()
        for i in range(m):
            for j in range(n):
                temp = 0
                for l in range(k):
                    temp += left[i,l] * right[l,j]
                self[i,j] = temp
