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
        
        m, n = left.nrow(), right.ncol() #dimenzije produktne matrike matrike           
            

        #število vrstic in stolpcov leve in desne matrike
        ac = left.ncol()
        ar = left.nrow()
        bc = right.ncol()
        br = right.nrow()
        
        #zaustavitveni pogoj rekurzije; strassena ne izvajamo dalje če je vsaj
        #ena od komponent matrik enaka 1
        if ac == 1 or ar == 1 or bc == 1 or br == 1:            
            super().multiply(left, right)
            return self

        if(m <= 32 and n <=32):
            super().multiply(left, right)
            return self

        #velikosti podmatrik leve matrike            
        if ac%2 == 0:
            if ar%2 == 0:
                left_new_c = ac//2 #št. stolpcev leve podmatrike
                left_new_r = ar//2 #št. vrstic leve podmatrike
            else:
                left_new_c = ac//2
                left_new_r = (ar - 1)//2
        else:
            if ar%2 == 0:
                left_new_c = (ac - 1)//2
                left_new_r = ar//2
            else:
                left_new_c = (ac-1)//2
                left_new_r = (ar-1)//2

        #velikosti podmatrik desne matrike        
        if bc%2 == 0:
            if br%2 == 0:
                right_new_c = bc//2 #št. stolpcev leve podmatrike
                right_new_r = br//2 #št. vrstic leve podmatrike
            else:
                right_new_c = bc//2
                right_new_r = (br-1)//2
        else:
            if br%2 == 0:
                right_new_c = (bc-1)//2
                right_new_r = br//2
            else:
                right_new_c = (bc-1)//2
                right_new_r = (br-1)//2

        #inicializacija podmatrik

        #leva matrika
        A11 = left[0:left_new_r, 0:left_new_c]
        A12 = left[0:left_new_r, left_new_c:2*left_new_c]
        A21 = left[left_new_r:2*left_new_r, 0:left_new_c]
        A22 = left[left_new_r:2*left_new_r, left_new_c:2*left_new_c]

        #dimenzije teh niso enake 0 le če matrika ni soda
        a1 = left[0:2*left_new_r, 2*left_new_c:ac] # zadnji desni stolpec
        a2 = left[2*left_new_r:ar, 0:2*left_new_c] # spodnja vrstica
        a3 = left[2*left_new_r:ar, 2*left_new_c:ac] # spodnji desni elemnt

        #desna matrika
        B11 = right[0:right_new_r, 0:right_new_c]
        B12 = right[0:right_new_r, right_new_c:2*right_new_c]
        B21 = right[right_new_r:2*right_new_r, 0:right_new_c]
        B22 = right[right_new_r:2*right_new_r, right_new_c:2*right_new_c]

        #podobno kot pri matriki A
        b1 = right[0:2*right_new_r, 2*right_new_c:bc]
        b2 = right[2*right_new_r:br, 0:2*right_new_c]
        b3 = right[2*right_new_r:br, 2*right_new_c:bc]

        #ciljna matrika
        C11 = self[0:left_new_r, 0:right_new_c]
        C12 = self[0:left_new_r, right_new_c:2*right_new_c]
        C21 = self[left_new_r:2*left_new_r, 0:right_new_c]
        C22 = self[left_new_r:2*left_new_r, right_new_c:2*right_new_c]

        #podobno kot pri matriki A in B
        C1 = self[0:2*left_new_r, 2*right_new_c:n]
        C2 = self[2*left_new_r:m, 0:2*right_new_c]
        C3 = self[2*left_new_r:m, 2*right_new_c:n]

        #delovna matrika
        W11 = work[0:left_new_r, 0:right_new_c]
        W12 = work[0:left_new_r, right_new_c:2*right_new_c]
        W21 = work[left_new_r:2*left_new_r, 0:right_new_c]
        W22 = work[left_new_r:2*left_new_r, right_new_c:2*right_new_c]
        
        #Rekurzivno izračunamo matrike P1,..P7, pri tem pa pazimo da ne uporabljamo operatorja "+"
        #saj naredi novo kopijo matrike. Vsa odštevanja in prištevanja porabijo n*m časovne zahtevnosti
        #če sta n in m velikosti matrik


        #C12 = P1        
        B12 -= B22        
        C12.multiply(A11, B12, W11)
        B12 += B22        

        #W12 = P2
        A11 += A12
        W12.multiply(A11, B22, W11)
        A11 -= A12

        #C21 = P3
        A21 += A22
        C21.multiply(A21, B11, W11)
        A21 -= A22

        #W21 = P4
        B21 -= B11
        W21.multiply(A22, B21, W11)
        B21 += B11

        #W22 = P5
        A11 += A22
        B11 += B22
        W22.multiply(A11, B11, W11)
        A11 -= A22
        B11 -= B22

        #C11 = P6
        A12 -= A22
        B21 += B22
        C11.multiply(A12, B21, W11)
        A12 += A22
        B21 -= B22

        #C22 = P7
        A11 -= A21
        B11 += B12
        C22.multiply(A11, B11, W11)
        A11 += A21
        B11 -= B12

                

        
        #Izračun ciljne matrike; najprej izračunamo del C22 saj do zdaj drugi deli C matrike še niso pravilno izračunani
        #ampak so v njih shranjeni P1,P2,..

        #C22 = -P7(C22) P1(C12) - P3(C21) + P5(D22)
        C22 *=-1
        C22 += C12
        C22 -= C21
        C22 += W22

        #C11 = P6(C11) + P5(D22) + P4(D21) - P2(D12)
        C11 += W22
        C11 += W21
        C11 -= W12

        #C12 = P1(C12) + P2(D12)
        C12 += W12

        #C21 = P3(C21) + P4(D21)
        C21 += W21

        #poprava lihih stolpcev vrstic

        if ar%2 != 0:
            W2 = work[2*left_new_r:m, 0:2*right_new_c]

            W2.multiply(a2, right[0:2*right_new_r, 0:2*right_new_c])
            C2 += W2

            W2.multiply(a3, b2)
            C2 += W2
            
        if bc%2 != 0:
            W1 = work[0:2*left_new_r, 2*right_new_c]

            W1.multiply(left[0:2*left_new_r, 0:2*left_new_c], b1)
            C1 += W1

            W1.multiply(a1, b3)
            C1 += W1
            
        if ac%2 != 0:
            Wsub = work[0:2*left_new_r, 0:2*right_new_c]            
            Wsub.multiply(a1, b2)
            self[0:2*left_new_r, 0:2*right_new_c] += Wsub

        if ar%2 !=0 and bc%2 != 0:
            self[2*left_new_r, 2*right_new_c] = a2*b1 + a3*b3

        return self
                



      
        

