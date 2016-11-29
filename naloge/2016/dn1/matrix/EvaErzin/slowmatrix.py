# -*- coding: utf-8 -*-
from matrix import AbstractMatrix

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

        for i in range(self.nrow()):
            for j in range(self.ncol()):
                sum = 0
                for k in range (left.ncol()):
                    sum += left[i, k] * right[k, j]
                self[i, j] = sum

X = SlowMatrix([[ 1,  2,  3,  4],
                  [ 5,  6,  7,  8],
                  [ 9, 10, 11, 12],
                  [13, 14, 15, 16],
                  [17, 18, 19, 20]])

Y = SlowMatrix([[ 1,  2,  3,  4,  5,  6],
                  [ 7,  8,  9, 10, 11, 12],
                  [13, 14, 15, 16, 17, 18],
                  [19, 20, 21, 22, 23, 24]])


