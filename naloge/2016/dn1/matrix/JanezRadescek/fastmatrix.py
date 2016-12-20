# -*- coding: utf-8 -*-
from .slowmatrix import SlowMatrix

class FastMatrix(SlowMatrix):
    """
    Matrika z množenjem s Strassenovim algoritmom.
    """
    def multiply(self, left, right):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Množenje izvede s Strassenovim algoritmom.
        """
        assert left.ncol() == right.nrow(), \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"


        a = self.nrow()
        b = self.ncol()
        ujemanje = left.ncol()

        #če imamo množenje z vektorjem zmnožimo na običajen način
        if (a == 1) or (b == 1) or (ujemanje == 1):
            super(FastMatrix, self).multiply(left,right)

        #poskrbimo če stranice niso sode

        elif a%2 == 1:
            self[:a,:] = self.multiply(left[:a,:],right)
            self[a,:] = self.multiply(left[a,:],right)

        elif b%2 == 1:
            self[:,:b] = self.multiply(left, right[:,:b])
            self[b,:] = self.multiply(left, right[:,b])

        elif c%2 == 1:
            self[:,:] = self.multiply(left[:,:ujemanje], right[:ujemanje,:]) + self.multiply(left[:,ujemanje], right[ujemanje,:])


        #če so sode

        else:
            pass