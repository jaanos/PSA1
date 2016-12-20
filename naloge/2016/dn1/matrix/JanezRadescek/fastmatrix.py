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


        aaa = self.nrow()
        bbb = self.ncol()
        ujemanje = left.ncol()

        #če imamo množenje z vektorjem zmnožimo na običajen način
        if (aaa == 1) or (bbb == 1) or (ujemanje == 1):
            super(FastMatrix, self).multiply(left,right)

        #poskrbimo če stranice matrik niso sode

        elif aaa%2 == 1:
            self[:aaa,:] = self.multiply(left[:aaa,:],right)
            self[aaa,:] = self.multiply(left[aaa,:],right)

        elif bbb%2 == 1:
            self[:,:bbb] = self.multiply(left, right[:,:bbb])
            self[bbb,:] = self.multiply(left, right[:,bbb])

        elif ujemanje%2 == 1:
            self[:,:] = self.multiply(left[:,:ujemanje], right[:ujemanje,:]) + self.multiply(left[:,ujemanje], right[ujemanje,:])


        #če so sode


        else:
            a = aaa / 2
            b = bbb / 2
            c = ujemanje / 2

            #podmatrike
            A = left[:a,:c]
            B = left[:a,c:]
            C = left[a:,:c]
            D = left[a:,c:]

            E = right[:a,:c]
            F = right[:a,c:]
            G = right[a:,:c]
            H = right[a:,c:]

            #7 množenj
            p1 = self.multiply(A, F - H)
            p2 = self.multiply(A+B,H)
            p3 = self.multiply(C+D,E)
            p4 = self.multiply(D,G-E)
            p5 = self.multiply(A+D,E+H)
            p6 = self.multiply(B-D,G+H)
            p7 = self.multiply(A-C,E+F)

            #seštevanje
            self[:a,:b] = p4 + p5 + p6 -p2
            self[:a,b:] = p1 + p2
            self[a:,:b] = p3 + p4
            self[a:,b:] = p1 + p5 - p3 -p7

