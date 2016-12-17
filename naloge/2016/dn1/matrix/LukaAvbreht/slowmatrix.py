# -*- coding: utf-8 -*-
from .. matrix import AbstractMatrix
#import se ne izvede (SystemError: Parent module '' not loaded, cannot perform relative import)
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
        self *= 0
        for i in range(levaVrst):
            for j in range(desnaStol):
                for k in range(levaStol):
                    self[i,j] += (left[i,k]*right[k,j])
        return self


