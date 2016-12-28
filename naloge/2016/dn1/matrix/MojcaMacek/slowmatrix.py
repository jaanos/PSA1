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

        
        
##        n=right.ncol()
##        m=right.nrow()
##        p=left.nrow()
        n=len(right[0])
        m=len(right)
        p=len(left)
        print(n,m,p)
        assert len(left[0]) == m, \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert len(self) == p and n == len(self[0]), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        for i in range (n):
            for j in range(m):
                x=0
                for k in range(p):
                    #x += right[k,i]*left[j,k]
                    x += right[k][i]*left[j][k]
                #self[i,j] = x
                self[j][i] = x
            
        return self
        
##        raise NotImplementedError("Naredi sam!")
A=[[1,2],[2,1]]
B=[[1,2,1],[2,3,2]]
C=[[1,1,1],[1,1,1]]
D=[[1,1],[1,1]]
print(SlowMatrix.multiply(C,A,B))
print(SlowMatrix.multiply(D,A,B))

