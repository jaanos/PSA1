# -*- coding: utf-8 -*-

__author__ = "Filip Koprivec"

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

        N = self.ncol()
        M = left.ncol()

        for row in range(self.nrow()):
            for col in range(N):
                su = 0
                for j in range(M):
                    su += left[row, j] * right[j, col]
                self[row, col] = su

                # Slower :(, even slower: using dot_product
                # self[row, col] = sum(map(lambda x: x[0]*x[1], ((left[row, j], right[j, col]) for j in range(M))))

        return self
