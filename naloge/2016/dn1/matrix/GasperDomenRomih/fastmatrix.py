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


        m, n = left.nrow(), right.ncol()

        #število vrstic in stolpcov leve in desne matrike
        ac = left.ncol()
        ar = left.nrow()
        bc = right.ncol()
        br = right.nrow()


        if ac == 1 or ar == 1 or bc == 1 or br == 1:
            super().multiply(left, right)
            return self

        if(m <=32 and n <= 32):
            super().multiply(left, right)
            return self

        

        
        #zaustavitveni pogoj rekurzije; strassena ne izvajamo dalje če je vsaj
        #ena od komponent matrik enaka 1
        
        #velikosti podmatrik leve matrike            
        if ac%2 == 0:
            if ar%2 == 0:
                left_new_c = ac//2
                left_new_r = ar//2
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
                right_new_c = bc//2
                right_new_r = br//2
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
        A11 = left[0:left_new_r, 0:left_new_c]
        A12 = left[0:left_new_r, left_new_c:2*left_new_c]
        A21 = left[left_new_r:2*left_new_r, 0:left_new_c]
        A22 = left[left_new_r:2*left_new_r, left_new_c:2*left_new_c]
        a1 = left[0:2*left_new_r, 2*left_new_c:ac]
        a2 = left[2*left_new_r:ar, 0:2*left_new_c]
        a3 = left[2*left_new_r:ar, 2*left_new_c:ac]

        B11 = right[0:right_new_r, 0:right_new_c]
        B12 = right[0:right_new_r, right_new_c:2*right_new_c]
        B21 = right[right_new_r:2*right_new_r, 0:right_new_c]
        B22 = right[right_new_r:2*right_new_r, right_new_c:2*right_new_c]
        b1 = right[0:2*right_new_r, 2*right_new_c:bc]
        b2 = right[2*right_new_r:br, 0:2*right_new_c]
        b3 = right[2*right_new_r:br, 2*right_new_c:bc]

        #7 rekurzino izračunanih produktov
        P1 = A11 * (B12 - B22)
        P2 = (A11 + A12) * B22
        P3 = (A21 + A22) * B11
        P4 = A22* (B21 - B11)
        P5 = (A11 + A22) * (B11 + B22)
        P6 = (A12 - A22) * (B21 + B22)
        P7 = (A11 - A21) * (B11 + B12)            

        #glavni del matrike, ki smo ga reševali rekurzivno
        C11 = self[0:left_new_r, 0:right_new_c]            
        C12 = self[0:left_new_r, right_new_c:2*right_new_c]
        C21 = self[left_new_r:2*left_new_r, 0:right_new_c]
        C22 = self[left_new_r:2*left_new_r, right_new_c:2*right_new_c]

        #z for zanko ppopravimo elemente ciljne matrike, da se izgognemo nepotrebnemu seštevanju matrik
        #ter s tem porablanje spomina
        for i in range(left_new_r):
            for j in range(right_new_c):
                C11[i,j] = P4[i,j] + P5[i,j] + P6[i,j] - P2[i,j]
                C12[i,j] = P1[i,j] + P2[i,j]
                C21[i,j] = P3[i,j] + P4[i,j]
                C22[i,j] = P1[i,j] + P5[i,j] - P3[i,j] - P7[i,j]

       
        
        #poprava lihih stolpcev vrstic: če ni lihih stolpcev in vrstic
        #bodo te produtki enaki 0(več v poročilu)
        if ar%2 != 0:
            print()
            c2 = self.ijk(a2, right[0:2*right_new_r, 0:2*right_new_c]) + self.ijk(a3, b2)
            self[2*left_new_r:m, 0:2*right_new_c] = c2
        if bc%2 != 0:
            c1 = self.ijk(left[0:2*left_new_r, 0:2*left_new_c], b1) + self.ijk(a1, b3)
            self[0:2*left_new_r, 2*right_new_c:n] = c1
        if ac%2 != 0:
            self[0:2*left_new_r, 0:2*right_new_c] += self.ijk(a1, b2)

        if ar%2 !=0 and bc%2 != 0:
            c3 = self.ijk(a2,b1) + self.ijk(a3,b3)
            self[2*left_new_r:m, 2*right_new_c:n] = c3                 
        
        return self

    def ijk(self, left, right):
        C = FastMatrix(nrow = left.nrow(), ncol = right.ncol())
        for i in range(C.nrow()):
            for j in range(C.ncol()):
                row = left[i, 0:left.ncol()]
                colum = right[0:right.nrow(), j]  
                C[i,j] =  sum(row[0, k]*colum[k, 0] for k in range(row.ncol()))
        return C     
        
        
        
                    
        

    
    


                           
