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
            #self[:aaa-1,:] = self[:aaa-1,:].multiply(left[:aaa-1,:],right)
            #self[aaa-1,:] = self[aaa-1,:].multiply(left[aaa-1,:],right)

            self[:aaa-1,:] = left[:aaa-1,:] * right
            self[aaa-1,:] = left[aaa-1,:] * right

        elif bbb%2 == 1:
            #self[:,:bbb-1] = self[:,:bbb-1].multiply(left, right[:,:bbb-1])
            #self[:,bbb-1] = self[:,bbb-1].multiply(left, right[:,bbb-1])

            self[:,:bbb-1] = left * right[:,:bbb-1]
            self[:,bbb-1] = left * right[:,bbb-1]


        elif ujemanje%2 == 1:
            #self[:,:] = self.multiply(left[:,:ujemanje-1], right[:ujemanje-1,:]) + self.multiply(left[:,ujemanje-1], right[ujemanje-1,:])
            self[:,:] = left[:,:ujemanje-1] * right[:ujemanje-1,:] + left[:,ujemanje-1] * right[ujemanje-1,:]

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

            E = right[:c,:b]
            F = right[:c,b:]
            G = right[c:,:b]
            H = right[c:,b:]

            #7 množenj
            p1 = A * (F - H)
            p2 = (A + B) * H
            p3 = (C + D) *E
            p4 = D * (G - E)
            p5 = (A + D) * (E + H)
            p6 = (B - D) * (G + H)
            p7 = (A - C) * (E + F)

            #seštevanje
            self[:a,:b] = p4 + p5 + p6 -p2
            self[:a,b:] = p1 + p2
            self[a:,:b] = p3 + p4
            self[a:,b:] = p1 + p5 - p3 -p7

