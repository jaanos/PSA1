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


        lv = left.nrow()
        ls = left.ncol()
        dv = ls
        ds = right.ncol()


        #za manjše matrike bomo uporabili navadno mnozenje, saj se Strassenov
        #algoritem ne splaca vec
        if lv <= 4 or ls <= 4 or ds <= 4:
            super().multiply(left,right)


        #lociti moramo primere glede na to ali sta stevili stolpcev in vrstic matrike lihi ali sodi
        elif lv % 2 == 0 and ls % 2 == 0 and ds % 2 == 0:
            A = left[0:(lv//2),0:(ls//2)]
            B = left[0:(lv//2),(ls//2):ls]
            C = left[(lv//2):lv,0:(ls//2)]
            D = left[(lv//2):lv,(ls//2):ls]

            E = right[0:(dv//2),0:(ds//2)]
            F = right[0:(dv//2),(ds//2):ds]
            G = right[(dv//2):dv,0:(ds//2)]
            H = right[(dv//2):dv,(ds//2):ds]

            P1 = A*(F - H)
            P2 = (A + B)*H
            P3 = (C + D)*E
            P4 = D*(G - E)
            P5 = (A + D)*(E + H)
            P6 = (B - D)*(G + H)
            P7 = (A - C)*(E + F)

            self[0:(lv//2),0:(ds//2)] = P4 + P5 + P6 - P2
            self[0:(lv//2),(ds//2):ds] = P1 + P2
            self[(lv//2):lv,0:(ds//2)] = P3 + P4
            self[(lv//2):lv,(ds//2):ds] = P1 + P5 - P3 - P7

        elif lv % 2 == 1 and ls % 2 == 1 and ds % 2 == 1:
            A11 = left[0:(lv-1),0:(ls-1)]
            a12 = left[0:(lv-1),ls-1:ls]
            a21 = left[lv-1:lv,0:ls-1]
            a22 = left[lv-1,ls-1]

            B11 = right[0:(dv-1),0:(ds-1)]
            b12 = right[0:(dv-1),ds-1:ds]
            b21 = right[dv-1:dv,0:ds-1]
            b22 = right[dv-1,ds-1]

            self[0:(lv-1),0:(ds-1)] = A11*B11 + a12*b21
            self[0:(lv-1),(ds-1):ds] = A11*b12 + a12*b22
            self[(lv-1):lv,0:(ds-1)] = a21*B11 + a22*b21
            self[(lv-1):lv,(ds-1):ds] = a21*b12 + a22*b22

        elif lv % 2 == 0 and ls % 2 == 1 and ds % 2 == 1:
            A11 = left[0:lv,0:(ls-1)]
            a12 = left[0:lv,ls-1:ls]

            B11 = right[0:(dv-1),0:(ds-1)]
            b12 = right[0:(dv-1),ds-1:ds]
            b21 = right[dv-1:dv,0:ds-1]
            b22 = right[dv-1,ds-1]

            self[0:lv,0:(ds-1)] = A11*B11 + a12*b21
            self[0:lv,(ds-1):ds] = A11*b12 + a12*b22

        elif lv % 2 == 0 and ls % 2 == 1 and ds % 2 == 0:
            A11 = left[0:lv,0:(ls-1)]
            a12 = left[0:lv,ls-1:ls]

            B11 = right[0:(dv-1),0:ds]
            b21 = right[dv-1:dv,0:ds]

            self[:,:] = A11*B11 + a12*b21

        elif lv % 2 == 0 and ls % 2 == 0 and ds % 2 == 1:
            A11 = left

            B11 = right[0:dv,0:(ds-1)]
            b12 = right[0:dv,(ds-1):ds]

            self[0:lv,0:(ds-1)] = A11*B11
            self[0:lv,(ds-1):ds] = A11*b12

        elif lv % 2 == 1 and ls % 2 == 0 and ds % 2 == 1:
            A11 = left[0:lv-1,0:ls]
            a21 = left[lv-1:lv,0:ls]

            B11 = right[0:dv,0:(ds-1)]
            b12 = right[0:dv,ds-1:ds]

            self[0:lv-1,0:ds-1] = A11*B11
            self[0:lv-1,ds-1:ds] = A11*b12
            self[lv-1:lv,0:ds-1] = a21*B11
            self[lv-1:lv,ds-1:ds] = a21*b12

        elif lv % 2 == 1 and ls % 2 == 1 and ds % 2 == 0:

            A11 = left[0:(lv-1),0:(ls-1)]
            a12 = left[0:(lv-1),ls-1:ls]
            a21 = left[lv-1:lv,0:ls-1]
            a22 = left[lv-1,ls-1]

            B11 = right[0:(dv-1),0:ds]
            b21 = right[dv-1:dv,0:ds]

            self[0:lv-1,0:ds] = A11*B11 + a12*b21
            self[lv-1:lv,0:ds] = a21*B11 + a22*b21

        elif lv % 2 == 1 and ls % 2 == 0 and ds % 2 == 0:

            A11 = left[0:(lv-1),0:ls]
            a21 = left[lv-1:lv,0:ls]

            B11 = right

            self[0:lv-1,0:ds] = A11*B11
            self[lv-1:lv,0:ds] = a21*B11









