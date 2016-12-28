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
        n=len(right[0])
        m=len(right)
        p=len(left)
        
        assert len(left[0]) == m, \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert len(self) == p and n == len(self[0]), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        if n==1 or m==1 or p==1:
            return SlowMatrix.multiply(self,left,right)
        

        l=min(n,m,p) #najvišja meja za stranico kvadrata
        
        else:
            if l%2==0: #sode kvadratne matrike istih stranic
                A=left[0:l/2, 0:l/2]
                B=left[0:l/2, l/2:l]
                C=left[l/2:l, 0:l/2]
                D=left[l/2:l, l/2:l]
                E=right[0:l/2, 0:l/2]
                F=right[0:l/2, l/2:l]
                G=right[l/2:l, 0:l/2]
                H=right[l/2:l, l/2:l]

                P1=FastMatrix.multiply(AbstractMatrix(A, A, F-G))
                P2=FastMatrix.multiply(AbstractMatrix(A, A+B, H))
                P3=FastMatrix.multiply(AbstractMatrix(A, C+D, E))
                P4=FastMatrix.multiply(AbstractMatrix(A, D, G-E))
                P5=FastMatrix.multiply(AbstractMatrix(A, A+D, E+H))
                P6=FastMatrix.multiply(AbstractMatrix(A, B-D, G+H))
                P7=FastMatrix.multiply(AbstractMatrix(A, A-C, E+F))
                
                return [[P4+P5+P6-P2, P1+P2],[P3+P4, P1+P5-P3-P7]]
            
            if l%2!=0:
                l+=-1
                A=left[0:l/2, 0:l/2]
                B=left[0:l/2, l/2:l]
                C=left[l/2:l, 0:l/2]
                D=left[l/2:l, l/2:l]
                E=right[0:l/2, 0:l/2]
                F=right[0:l/2, l/2:l]
                G=right[l/2:l, 0:l/2]
                H=right[l/2:l, l/2:l]

                P1=FastMatrix.multiply(AbstractMatrix(A, A, F-G))
                P2=FastMatrix.multiply(AbstractMatrix(A, A+B, H))
                P3=FastMatrix.multiply(AbstractMatrix(A, C+D, E))
                P4=FastMatrix.multiply(AbstractMatrix(A, D, G-E))
                P5=FastMatrix.multiply(AbstractMatrix(A, A+D, E+H))
                P6=FastMatrix.multiply(AbstractMatrix(A, B-D, G+H))
                P7=FastMatrix.multiply(AbstractMatrix(A, A-C, E+F))

                DM =[[P4+P5+P6-P2, P1+P2],[P3+P4, P1+P5-P3-P7]]#delovna matrika
                CM = AbstractMatrix([([0, ] * n), ]*k)#ciljna matrika
                for i in range[0:n-1]:
                    for j in range[0:n-1]:
                        #vzeli bomo element (i,j) matrike DM in prišteli, kar manjka    
                        CM[i,j]=DM[i,j]+ right[n-1,j]*left[i,n-1]
                for j=n-1:#zadnji stolpec
                    for i in range[0:n]:
                        x=0
                        for k in range[0:n]:
                            x += right[k,n]*left[i,k]
                        CM[i,j]=x
                for i=n-1:#zadnja vrstica
                    for j in range[0:n]:
                        x=0
                        for k in range[0:n]:
                            x += left[n-1, k]*right[k, j]
                        CM[i,j]=x
                return CM

                        


       
