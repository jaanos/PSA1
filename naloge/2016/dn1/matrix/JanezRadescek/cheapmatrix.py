# -*- coding: utf-8 -*-
from .slowmatrix import SlowMatrix

class CheapMatrix(SlowMatrix):
    """
    Matrika s prostorsko nepotratnim množenjem.
    """
    def multiply(self, left, right, work = None):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Kot neobvezen argument lahko podamo še delovno matriko.
        """
        assert left.ncol() == right.nrow(), \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        if work is None:
            work = self.__class__(nrow = self.nrow(), ncol = self.ncol())
        else:
            assert self.nrow() == work.nrow() and self.ncol() == work.ncol(), \
               "Dimenzije delovne matrike ne ustrezajo dimenzijam produkta!"





        aaa = self.nrow()
        bbb = self.ncol()
        ujemanje = left.ncol()
        work *= 0

        #če imamo množenje z vektorjem zmnožimo na običajen način
        if (aaa == 1) or (bbb == 1) or (ujemanje == 1):
            super(CheapMatrix, self).multiply(left,right)


        #poskrbimo če stranice matrik niso sode
        elif aaa%2 == 1:
            #self[:aaa-1,:] = self[:aaa-1,:].multiply(left[:aaa-1,:],right)
            #self[aaa-1,:] = self[aaa-1,:].multiply(left[aaa-1,:],right)
            self[:aaa-1,:].multiply(left[:aaa-1,:],  right, work[:aaa-1,:])
            self[aaa-1,:].multiply(left[aaa-1,:],  right, work[aaa-1,:])

        elif bbb%2 == 1:
            #self[:,:bbb-1] = self[:,:bbb-1].multiply(left, right[:,:bbb-1])
            #self[:,bbb-1] = self[:,bbb-1].multiply(left, right[:,bbb-1])

            self[:,:bbb-1].multiply(left, right[:,:bbb-1], work[:,:bbb-1])
            self[:,bbb-1].multiply(left, right[:,bbb-1], work[:,bbb-1])


        elif ujemanje%2 == 1:
            #self[:,:] = self.multiply(left[:,:ujemanje-1], right[:ujemanje-1,:]) + self.multiply(left[:,ujemanje-1], right[ujemanje-1,:])
            #self[:,:] = left[:,:ujemanje-1] * right[:ujemanje-1,:] + left[:,ujemanje-1] * right[ujemanje-1,:]
            self.multiply(left[:,:ujemanje-1], right[:ujemanje-1,:], work)
            self += super(CheapMatrix, self).multiply( left[:,ujemanje-1], right[ujemanje-1,:] )


        #če so sode
        else:
            a = aaa // 2
            b = bbb // 2
            c = ujemanje // 2

            #podmatrike
            L11 = left[:a,:c]
            L12 = left[:a,c:]
            L21 = left[a:,:c]
            L22 = left[a:,c:]

            R11 = right[:c,:b]
            R12 = right[:c,b:]
            R21 = right[c:,:b]
            R22 = right[c:,b:]

            S11 = self[:a,:b]
            S12 = self[:a,b:]
            S21 = self[a:,:b]
            S22 = self[a:,b:]

            W11 = work[:a,:b]
            W12 = work[:a,b:]
            W21 = work[a:,:b]
            W22 = work[a:,b:]

            #P1
            W12*=0
            R12-=R22
            W12.multiply(L11, R12, W22)
            R12+=R22
            S12+=W12
            S22+=W12

            #P2
            W12*=0
            L11+=L12
            W12.multiply(L11, R22,W22)
            L11-=L12
            S11-=W12
            S12+=W12

            #p3 c+d*e
            W21*=0
            L21+=L22
            W21.multiply(L21,R11,W22)
            L21-=L22
            S21+=W21
            S22-=W21

            #p4 d*g-e
            W11*=0
            R21-=R11
            W11.multiply(L22, R21,W12)
            R21+=R11
            S11+=W11
            S21+=W11

            #p5 a+d * e+h
            W11*=0
            L11+=L22
            R11+=R22
            W11.multiply(L11, R11,W12)
            L11-=L22
            R11-=R22
            S11+=W11
            S22+=W11

            #p6 b-d * g+h s11
            W11*=0
            L12-=L22
            R21+=R22
            W11.multiply(L12,R21,W12)
            L12+=L22
            R21-=R22
            S11+=W11

            #p7 a-c * e+f   -s22
            W22*=0
            L11-=L21
            R11+=R12
            W22.multiply(L11, R11,W21)
            L11+=L21
            R11-=R12
            S22-=W22





