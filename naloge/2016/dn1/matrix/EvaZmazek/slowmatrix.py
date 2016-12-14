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
        levaStol = left.ncol()
        levaVrst = left.nrow()
        desnaStol = right.ncol()
        # desnaVrst = right.nrow() #ta mora bit enaka k levaStolpci, kar ce ni itak vrnemo v prvi vrstici tko da je nepotrebo
        for i in range(levaVrst):
            trenvrst = []
            for j in range(desnaStol):
                tren = 0
                for k in range(levaStol):
                    tren += (left[i, k] * right[k, j])
                self[i, j] = tren
        return self
