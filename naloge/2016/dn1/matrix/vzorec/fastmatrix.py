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
               
        m = max(left.nrow(), right.ncol(), left.ncol())
        n = 0
        while m > 2**n:
            n += 1
        size = 2**n
        
        leftNew = FastMatrix(nrow=size, ncol=size)
        leftNew[0:left.nrow(), 0:left.ncol()] = left
        rightNew = FastMatrix(nrow=size, ncol=size)
        rightNew[0:right.nrow(), 0:right.ncol()] = right
        
        def Strassen(left, right, size):
            if size == 1:
                return left[0, 0] * right[0, 0]
                
            newsize = size//2

            A = left[0:newsize, 0:newsize]
            B = left[0:newsize, newsize:size]
            C = left[newsize:size, 0:newsize]
            D = left[newsize:size, newsize:size]
            E = right[0:newsize, 0:newsize]
            F = right[0:newsize, newsize:size]
            G = right[newsize:size, 0:newsize]
            H = right[newsize:size, newsize:size]
            P1 = Strassen(A, F-H, newsize)
            P2 = Strassen(A+B, H, newsize)
            P3 = Strassen(C+D, E, newsize)
            P4 = Strassen(D, G-E, newsize)
            P5 = Strassen(A+D, E+H, newsize)
            P6 = Strassen(B-D, G+H, newsize)
            P7 = Strassen(A-C, E+F, newsize)
            
            M = FastMatrix(nrow=size, ncol=size)
            M[0:newsize, 0:newsize] = P4+P5+P6-P2
            M[0:newsize, newsize:size] = P1+P2
            M[newsize:size, 0:newsize] = P3+P4
            M[newsize:size, newsize:size] = P1+P5-P3-P7
            
            return M
        
        K = Strassen(leftNew, rightNew, size)
        self[0:self.nrow(), 0:self.ncol()] = K[0:self.nrow(), 0:self.ncol()]
        
        
