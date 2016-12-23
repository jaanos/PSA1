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

        # Vsak element dobimo s skalarnim produktom ustrezne
        # vrstice prve matrike in stolpca druge matrike.
        for i in range(self.nrow()):
            for j in range(self.ncol()):
                self[i, j] = sum(left[i, k]*right[k, j] for k in range(left.ncol()))
