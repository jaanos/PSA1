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
        #Naivno množenje matrik
        for i in range(self.nrow()):
            for j in range(self.ncol()):
                vs = 0
                #Uporabimo vs, kej je hitreje kot da pri pri vsakem spreminjali self[i, j]
                for k in range(left.ncol()):
                        vs += left[i, k] * right[k, j]
                self[i, j] = vs

        return self
