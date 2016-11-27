# -*- coding: utf-8 -*-

__author__ = "Filip Koprivec"

from ..matrix import AbstractMatrix


class SlowMatrix(AbstractMatrix):
    """
    Matrika z naivnim množenjem.
    """

    @staticmethod
    def dot_product(v1, v2):
        # return sum(p*q for p, q in zip(v1, v2)) or is it not iterable ?
        return sum(v1[0, j] * v2[j, 0] for j in range(v1.ncol()))

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
        for row in range(self.nrow()):
            for col in range(self.ncol()):
                self[row, col] = self.dot_product(left[row, 0:left.ncol()], right[0:right.nrow(), col])

        return self
