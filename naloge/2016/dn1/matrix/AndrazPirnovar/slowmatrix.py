# -*- coding: utf-8 -*-
#try:
#    from ..matrix import AbstractMatrix     #Spremenil zaradi SystemError na mojemu racunalniku
#except SystemError:
#    from matrix import AbstractMatrix

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
        #raise NotImplementedError("Naredi sam!")

        for i in range(left.nrow()):                        #Po vrsticah prve
            for j in range(right.ncol()):                   #Po stolpcih druge
                for k in range(left.ncol()):                #Po elementih i-te vrstice prve in j-tega stolpca druge
                    self[i,j] += left[i,k] * right[k,j]     #Sestevek zmnozka teh elementov
